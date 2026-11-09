"""Clientes do avaliador. REAL: OpenAI Responses API, modelo `gpt-5.5-2026-04-23`, `reasoning.effort = "medium"`,
explicito em toda chamada; chave SO de OPENAI_API_KEY (nunca de arquivo). SIMULADO: respostas canned (testes e
calibracao); a chamada real fica para o Wagner (nao verificada nesta sessao)."""
from __future__ import annotations

import base64
import json
import os
import subprocess
import threading
import urllib.request
from pathlib import Path

MODELO = "gpt-5.5-2026-04-23"
EFFORT = "medium"
URL = "https://api.openai.com/v1/responses"


class ClienteReal:
    modelo, effort = MODELO, EFFORT

    def __init__(self, chave=None, timeout=300):
        self.chave = chave or os.environ.get("OPENAI_API_KEY")
        if not self.chave:
            raise RuntimeError("OPENAI_API_KEY ausente no ambiente (a chamada real e do Wagner; use --simulado)")
        self.timeout = timeout

    def parametros(self):
        return {"model": MODELO, "reasoning": {"effort": EFFORT}, "demais": "padrao do fornecedor"}

    def chamar(self, prompt, schema_nome, schema, imagens=(), item_id=None):
        conteudo = [{"type": "input_text", "text": prompt}]
        for img in imagens:
            b64 = base64.b64encode(Path(img).read_bytes()).decode()
            conteudo.append({"type": "input_image", "image_url": f"data:image/png;base64,{b64}"})
        corpo = {"model": MODELO, "reasoning": {"effort": EFFORT}, "input": [{"role": "user", "content": conteudo}],
                 "text": {"format": {"type": "json_schema", "name": schema_nome, "schema": schema, "strict": True}}}
        req = urllib.request.Request(URL, data=json.dumps(corpo).encode(), method="POST",
                                     headers={"Authorization": f"Bearer {self.chave}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            resp = json.loads(r.read())
        texto = "".join(c.get("text", "") for o in resp.get("output", []) if o.get("type") == "message" for c in o.get("content", []))
        return json.loads(texto)


SISTEMA_CLAUDE = ("You are an impartial evaluator. Follow the rubric in the user message exactly. "
                  "Answer ONLY with the JSON object required by the schema.")


class ClienteClaude:
    """D-099: avaliador Claude via `claude -p` (modo sem tela), no lugar do gpt-5.5 (sem chave OpenAI no prazo).
    Isolamento: diretorio neutro, sem ferramentas, sem skills/slash commands, sem MCP, sem CLAUDE.md
    (`--setting-sources ""`), sem persistencia de sessao. O ID canonico do modelo vem de `modelUsage` e e guardado.
    So texto (M9 por imagem nao e avaliada: D-100)."""
    effort = "padrao"

    def __init__(self, modelo="claude-opus-5-5", timeout=900, cwd="/tmp/juiz-claude"):
        self.modelo, self.timeout, self.cwd = modelo, timeout, cwd
        Path(cwd).mkdir(parents=True, exist_ok=True)
        self.modelos_observados, self.custo_usd, self.chamadas = set(), 0.0, 0
        self._lock = threading.Lock()

    def parametros(self):
        return {"model": self.modelo, "via": "claude -p --output-format json --json-schema", "tools": "nenhuma",
                "setting_sources": "vazio", "slash_commands": "desligados", "mcp": "estrito/nenhum", "persistencia": "desligada",
                "system_prompt": SISTEMA_CLAUDE, "demais": "padrao do fornecedor",
                "modelos_observados": sorted(self.modelos_observados)}

    def chamar(self, prompt, schema_nome, schema, imagens=(), item_id=None):
        if imagens:
            raise NotImplementedError("avaliador Claude so recebe texto (D-100: M9 por imagem nao avaliada)")
        cmd = ["claude", "-p", "--model", self.modelo, "--output-format", "json", "--json-schema", json.dumps(schema),
               "--tools", "", "--disable-slash-commands", "--strict-mcp-config", "--setting-sources", "",
               "--no-session-persistence", "--system-prompt", SISTEMA_CLAUDE]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=self.cwd, timeout=self.timeout)
        d = json.loads(r.stdout)
        with self._lock:
            self.chamadas += 1
            self.custo_usd += float(d.get("total_cost_usd") or 0)
            self.modelos_observados.update((d.get("modelUsage") or {}).keys())
        if d.get("is_error"):
            raise RuntimeError(str(d.get("result"))[:300])
        if d.get("structured_output") is not None:
            return d["structured_output"]
        return json.loads(d["result"])


class ClienteSimulado:
    """`respostas`: {item_id: [saida_exec1, saida_exec2, saida_exec3]} (ou uma so, repetida). Sem rede."""
    modelo, effort = MODELO, EFFORT

    def __init__(self, respostas, padrao=None):
        self.respostas, self.padrao, self.cont, self.chamadas, self.prompts = respostas, padrao, {}, [], []

    def parametros(self):
        return {"model": MODELO, "reasoning": {"effort": EFFORT}, "demais": "SIMULADO"}

    def chamar(self, prompt, schema_nome, schema, imagens=(), item_id=None):
        self.chamadas.append(item_id)
        self.prompts.append(prompt)
        n = self.cont.get(item_id, 0)
        self.cont[item_id] = n + 1
        lista = self.respostas.get(item_id, self.padrao)
        if lista is None:
            raise KeyError(f"sem resposta simulada para {item_id}")
        if isinstance(lista, dict):
            return lista
        return lista[n % len(lista)]
