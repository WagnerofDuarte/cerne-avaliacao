"""Addon contra servidor FALSO, passando por um mitmdump real (porta efemera)."""
import json
import os
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from holdout.proxy.tests import fake_backend

MITM = shutil.which("mitmdump") or "/root/tools/venv/bin/mitmdump"
ADDON = Path(__file__).resolve().parents[1] / "cerne_holdout.py"
pytestmark = pytest.mark.skipif(not Path(MITM).exists(), reason="mitmdump ausente")


def _porta():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p


@pytest.fixture(scope="module")
def ambiente():
    for k in ("no_proxy", "NO_PROXY"):
        os.environ[k] = ""  # o urllib nao deve contornar o proxy para 127.0.0.1
    back = fake_backend.iniciar()
    pp, pc = _porta(), _porta()
    env = dict(os.environ, TEST_FAULT_KEY="chave-de-teste-falsa", HOLDOUT_CONTROL_PORT=str(pc))
    proc = subprocess.Popen([MITM, "-s", str(ADDON), "--listen-host", "127.0.0.1", "--listen-port", str(pp), "-q"], env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{pc}/agora", timeout=0.5)
            break
        except Exception:
            time.sleep(0.1)
    else:
        proc.kill(); pytest.fail("addon nao subiu")
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": f"http://127.0.0.1:{pp}"}))
    base = f"http://127.0.0.1:{back.server_address[1]}/functions/v1"
    ctl = lambda p: json.loads(urllib.request.urlopen(f"http://127.0.0.1:{pc}{p}", timeout=5).read())
    yield {"opener": opener, "base": base, "ctl": ctl}
    proc.terminate(); proc.wait(timeout=10); back.shutdown()


def _get(a, fn, q="", metodo="GET", timeout=10):
    req = urllib.request.Request(f"{a['base']}/{fn}{q}", method=metodo, data=b"{}" if metodo == "POST" else None)
    try:
        r = a["opener"].open(req, timeout=timeout)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_cabecalhos_em_toda_chamada(ambiente):
    a = ambiente; a["ctl"]("/reset"); fake_backend.Fake.recebidos.clear()
    assert _get(a, "entries-list")[0] == 200
    h = fake_backend.Fake.recebidos[-1]["headers"]
    assert h["x-test-key"] == "chave-de-teste-falsa" and h["x-test-now"] == "2026-09-23T09:41:00Z" and "x-test-fault" not in h


@pytest.mark.parametrize("cen,fn,fault", [("F01", "entries-create", "timeout"), ("F02", "entries-create", "malformed"), ("F03", "entries-create", "offline"),
                                           ("F07", "media-ocr", "timeout"), ("F11", "export-summary-create", "malformed"), ("F15", "chat-insight-create", "offline")])
def test_falha_so_na_chamada_alvo_e_recupera(ambiente, cen, fn, fault):
    a = ambiente; a["ctl"]("/reset"); fake_backend.Fake.recebidos.clear()
    a["ctl"](f"/arm?cenario={cen}")
    _get(a, "entries-list")  # outra funcao: intocada
    assert "x-test-fault" not in fake_backend.Fake.recebidos[-1]["headers"]
    code, body = _get(a, fn, metodo="POST")
    assert fake_backend.Fake.recebidos[-1]["headers"]["x-test-fault"] == fault and code == 504
    code, _ = _get(a, fn, metodo="POST")  # recuperacao: so a 1a chamada leva a falha
    assert "x-test-fault" not in fake_backend.Fake.recebidos[-1]["headers"] and code == 200
    assert a["ctl"]("/check?regra=fault_injetado&fn=" + fn)["injecoes"] == 1


def test_cenario_de_segunda_chamada_h04_1(ambiente):
    a = ambiente; a["ctl"]("/reset"); fake_backend.Fake.recebidos.clear(); a["ctl"]("/arm?cenario=H04-1")
    _get(a, "chat-messages-send", metodo="POST")
    assert "x-test-fault" not in fake_backend.Fake.recebidos[-1]["headers"]
    _get(a, "chat-messages-send", metodo="POST")
    assert fake_backend.Fake.recebidos[-1]["headers"]["x-test-fault"] == "ai_timeout"


def test_corte_do_sse_apos_3_tokens(ambiente):
    a = ambiente; a["ctl"]("/reset"); a["ctl"]("/arm?cenario=H04-2")
    corpo = b""
    try:
        r = a["opener"].open(urllib.request.Request(f"{a['base']}/chat-messages-send", method="POST", data=b"{}"), timeout=10)
        while True:
            c = r.read(64)
            if not c:
                break
            corpo += c
    except Exception:
        pass  # conexao derrubada: esperado
    assert corpo.count(b"event: token") == 3 and b"event: done" not in corpo


def test_sem_corte_sem_cenario(ambiente):
    a = ambiente; a["ctl"]("/reset")
    code, corpo = _get(a, "chat-messages-send", metodo="POST")
    assert corpo.count(b"event: token") == 6 and b"event: done" in corpo


def test_401_forjado_e_offline_all(ambiente):
    a = ambiente; a["ctl"]("/reset"); a["ctl"]("/arm?cenario=H07-1")
    code, body = _get(a, "entries-list")
    assert code == 401 and json.loads(body)["error"]["code"] == "AUTH_EXPIRED"
    assert _get(a, "auth-refresh", metodo="POST")[0] == 401
    a["ctl"]("/disarm")
    assert _get(a, "entries-list")[0] == 200
    a["ctl"]("/arm?cenario=H06-3")
    with pytest.raises(Exception):
        _get(a, "entries-list", timeout=5)
    a["ctl"]("/disarm")
    assert _get(a, "entries-list")[0] == 200


def test_reescrita_de_resposta(ambiente):
    a = ambiente
    for cen, esperado in (("H09-3a", "x" * 4000), ("H09-3b", "")):
        a["ctl"]("/reset"); a["ctl"](f"/arm?cenario={cen}")
        assert json.loads(_get(a, "dashboard-narrative-get")[1])["narrative"] == esperado
    a["ctl"]("/reset"); a["ctl"]("/arm?cenario=exp_processing")
    assert json.loads(_get(a, "export-status-get")[1])["status"] == "processing"
    assert json.loads(_get(a, "export-status-get")[1])["status"] == "done"  # so a 1a


def test_contagem_e_debounce(ambiente):
    a = ambiente; a["ctl"]("/reset")
    # digitacao rapida: so a consulta final deve existir (simulamos o app correto e o errado)
    t_tecla = a["ctl"]("/agora")["ms"]
    time.sleep(0.35)
    _get(a, "entries-search", "?q=ansiedade")
    assert a["ctl"](f"/check?regra=debounce&q=ansiedade&gap_ms=300&ultima_tecla_ms={t_tecla}")["ok"]
    assert a["ctl"]("/check?regra=contagem&fn=entries-search&q=ansiedade&igual=1")["ok"]
    _get(a, "entries-search", "?q=ansie")   # app errado: consulta parcial
    r = a["ctl"](f"/check?regra=debounce&q=ansiedade&gap_ms=300&ultima_tecla_ms={t_tecla}")
    assert not r["ok"] and r["parciais"] == ["ansie"]
