"""Addon do mitmproxy da suite hold-out (H-005).

Uso: TEST_FAULT_KEY=<chave do ambiente> mitmdump -s holdout/proxy/cerne_holdout.py [--listen-port 8080]
A chave NUNCA e lida de arquivo versionado: vem do ambiente do operador (segredos/ fica fora daqui).

O que faz (cenarios.md §0 e rnf09.md):
- acrescenta `X-Test-Key` e `X-Test-Now` em toda requisicao;
- registra cada chamada (metodo, funcao, parametros, instante) para as asserções "proxy";
- injeta falhas SO onde o cenario armado manda: cabecalho `X-Test-Fault` (timeout|malformed|offline|ai_timeout,
  efeito executado pelo backend), corte do stream SSE depois do n-esimo evento `token`, resposta 401 forjada
  (AUTH_EXPIRED), conexao derrubada (offline em tudo), segurar resposta (estados transitorios) e reescrita de
  campos de resposta;
- expoe uma API de controle local (porta HOLDOUT_CONTROL_PORT, padrao 8099) para os fluxos Maestro e os testes:
    GET /arm?cenario=F01   GET /disarm   GET /reset   GET /log[?fn=..]   GET /check?regra=...
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from mitmproxy import http

try:
    from .cenarios import CENARIOS
except ImportError:  # carregado por `mitmdump -s` (sem pacote)
    import importlib.util
    import pathlib
    _s = importlib.util.spec_from_file_location("cenarios", pathlib.Path(__file__).with_name("cenarios.py"))
    _m = importlib.util.module_from_spec(_s)
    _s.loader.exec_module(_m)
    CENARIOS = _m.CENARIOS

NOW_PADRAO = "2026-09-23T09:41:00Z"
TOKEN_RE = re.compile(rb'event:\s*token|"type"\s*:\s*"token"')


def funcao_de(flow) -> str:
    h = flow.request.headers.get("x-cerne-function")
    if h:
        return h
    m = re.search(r"/functions/v1/([^/?]+)", flow.request.path)
    return m.group(1) if m else flow.request.path.split("?")[0].strip("/").split("/")[-1]


class Holdout:
    def __init__(self):
        self.key = os.environ.get("TEST_FAULT_KEY", "")
        self.now = os.environ.get("HOLDOUT_NOW", NOW_PADRAO)
        self.log = []          # [{n, t, metodo, fn, params, acao}]
        self.cenario = None
        self.regras = []
        self.vistos = {}       # (idx_regra) -> chamadas-alvo vistas
        self.agidos = {}       # (idx_regra) -> vezes que agiu
        self.lock = threading.Lock()
        self.control = None

    # ---------------------------------------------------------------- controle
    def arm(self, cenario):
        with self.lock:
            if cenario not in CENARIOS:
                raise KeyError(cenario)
            self.cenario, self.regras = cenario, CENARIOS[cenario]
            self.vistos, self.agidos = {}, {}
            self.log_inicio = len(self.log)

    def disarm(self):
        with self.lock:
            self.cenario, self.regras = None, []

    def reset(self):
        with self.lock:
            self.log.clear()
            self.cenario, self.regras = None, []
            self.vistos, self.agidos = {}, {}

    def _regra_aplica(self, fn):
        """Devolve (indice, regra) da regra que deve agir nesta chamada, ou None."""
        with self.lock:
            for i, r in enumerate(self.regras):
                if r["fn"] not in ("*", fn):
                    continue
                if r["acao"] == "forge_401" and fn == "auth-refresh":
                    return i, r
                visto = self.vistos.get(i, 0)
                self.vistos[i] = visto + 1
                if visto < r.get("pular", 0):
                    continue
                lim = r.get("limite", 1)
                if lim is not None and self.agidos.get(i, 0) >= lim:
                    continue
                self.agidos[i] = self.agidos.get(i, 0) + 1
                return i, r
        return None

    # ---------------------------------------------------------------- hooks
    def load(self, loader):
        porta = int(os.environ.get("HOLDOUT_CONTROL_PORT", "8099"))
        self._start_control(porta)

    def done(self):
        if self.control:
            self.control.shutdown()

    async def request(self, flow: http.HTTPFlow):
        fn = funcao_de(flow)
        if self.key:
            flow.request.headers["X-Test-Key"] = self.key
        flow.request.headers["X-Test-Now"] = self.now
        q = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(urlparse(flow.request.path).query).items()}
        reg = {"n": len(self.log) + 1, "t": int(time.time() * 1000), "metodo": flow.request.method, "fn": fn, "params": q, "acao": None}
        self.log.append(reg)
        hit = self._regra_aplica(fn)
        if not hit:
            return
        _, r = hit
        a = r["acao"]
        reg["acao"] = a
        flow.metadata["holdout_regra"] = r
        if a == "fault":
            flow.request.headers["X-Test-Fault"] = r["valor"]
        elif a == "offline_all":
            flow.kill()
        elif a == "forge_401":
            flow.response = http.Response.make(401, json.dumps({"error": {"code": "AUTH_EXPIRED", "message": "sessao expirada (forjada)"}}),
                                               {"Content-Type": "application/json"})
        elif a == "hold" and r["valor"]:
            flow.metadata["holdout_hold"] = float(r["valor"])

    async def responseheaders(self, flow: http.HTTPFlow):
        r = flow.metadata.get("holdout_regra")
        if r and r["acao"] == "sse_cut":
            alvo, vistos = int(r["valor"]), [0]

            def corte(chunk: bytes):
                if flow.metadata.get("holdout_cortado"):
                    return b""
                for m in TOKEN_RE.finditer(chunk):
                    vistos[0] += 1
                    if vistos[0] >= alvo:
                        fim = chunk.find(b"\n\n", m.end())
                        fim = len(chunk) if fim < 0 else fim + 2
                        flow.metadata["holdout_cortado"] = True
                        asyncio.get_event_loop().call_later(0.05, flow.kill)  # derruba depois de entregar o n-esimo token
                        return chunk[:fim]
                return chunk
            flow.response.stream = corte

    async def response(self, flow: http.HTTPFlow):
        r = flow.metadata.get("holdout_regra")
        if not r:
            return
        if r["acao"] == "hold" and flow.metadata.get("holdout_hold"):
            await asyncio.sleep(flow.metadata["holdout_hold"])
        elif r["acao"] == "rewrite":
            try:
                corpo = json.loads(flow.response.get_text())
            except (ValueError, TypeError):
                return
            padrao = re.compile(r["valor"]["campo"])
            if _reescrever(corpo, padrao, r["valor"]["valor"]):
                flow.response.set_text(json.dumps(corpo, ensure_ascii=False))

    # ---------------------------------------------------------------- checagens
    def check(self, regra, p):
        fn = p.get("fn")
        chamadas = [c for c in self.log if (fn is None or c["fn"] == fn) and all(str(c["params"].get(k)) == v for k, v in p.items() if k in ("q", "source", "period"))]
        apos = int(p["depois_de_ms"]) if "depois_de_ms" in p else 0
        chamadas = [c for c in chamadas if c["t"] >= apos]
        if regra == "contagem":
            n = len(chamadas)
            ok = n == int(p["igual"]) if "igual" in p else (n >= int(p.get("min", 0)) and n <= int(p.get("max", 10**9)))
            return {"ok": ok, "contagem": n}
        if regra == "debounce":
            termo, gap = p["q"], int(p.get("gap_ms", 300))
            todas = [c for c in self.log if c["fn"] == (fn or "entries-search") and c["t"] >= apos]
            exatas = [c for c in todas if c["params"].get("q") == termo]
            parciais = [c for c in todas if isinstance(c["params"].get("q"), str) and termo.startswith(c["params"]["q"]) and c["params"]["q"] != termo]
            ok = len(exatas) == 1 and not parciais
            if ok and "ultima_tecla_ms" in p:
                ok = exatas[0]["t"] - int(p["ultima_tecla_ms"]) >= gap
            return {"ok": ok, "exatas": len(exatas), "parciais": [c["params"]["q"] for c in parciais]}
        if regra == "fault_injetado":
            n = len([c for c in self.log if c["acao"] == "fault" and (fn is None or c["fn"] == fn)])
            return {"ok": n >= 1, "injecoes": n}
        return {"ok": False, "erro": f"regra desconhecida: {regra}"}

    # ---------------------------------------------------------------- servidor de controle
    def _start_control(self, porta):
        h = self

        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def _json(self, obj, code=200):
                b = json.dumps(obj, ensure_ascii=False).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(b)))
                self.end_headers()
                self.wfile.write(b)

            def do_GET(self):
                u = urlparse(self.path)
                p = {k: v[0] for k, v in parse_qs(u.query).items()}
                try:
                    if u.path == "/arm":
                        h.arm(p["cenario"]); return self._json({"ok": True, "cenario": p["cenario"]})
                    if u.path == "/disarm":
                        h.disarm(); return self._json({"ok": True})
                    if u.path == "/reset":
                        h.reset(); return self._json({"ok": True})
                    if u.path == "/agora":
                        return self._json({"ms": int(time.time() * 1000)})
                    if u.path == "/log":
                        return self._json([c for c in h.log if "fn" not in p or c["fn"] == p["fn"]])
                    if u.path == "/check":
                        return self._json(h.check(p.pop("regra"), p))
                except KeyError as e:
                    return self._json({"ok": False, "erro": f"faltou/desconhecido: {e}"}, 400)
                self._json({"erro": "rota"}, 404)

        self.control = ThreadingHTTPServer(("127.0.0.1", porta), H)
        threading.Thread(target=self.control.serve_forever, daemon=True).start()


def _reescrever(obj, padrao, valor) -> bool:
    mudou = False
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if padrao.search(k) and isinstance(v, str):
                obj[k] = valor
                mudou = True
            else:
                mudou = _reescrever(v, padrao, valor) or mudou
    elif isinstance(obj, list):
        for v in obj:
            mudou = _reescrever(v, padrao, valor) or mudou
    return mudou


addons = [Holdout()]
