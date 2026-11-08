import json
import shutil

import pytest
from PIL import Image

from harness.m9 import cor, tipografia
from harness.estatico.common import tag_copy
from harness.estatico.tests.conftest import CAL, repo  # noqa: F401  (fixture reaproveitada)

PRIMARIA = "#6B4EFF"


def _img(p, cor_ret, tam=(200, 100), ret=(50, 30, 150, 70)):
    im = Image.new("RGB", tam, (255, 255, 255))
    im.paste(cor_ret, ret)
    im.save(p)
    return p


def test_cor_certa_e_errada(tmp_path):
    certa = _img(tmp_path / "certa.png", (0x6B, 0x4E, 0xFF))
    errada = _img(tmp_path / "errada.png", (0xFF, 0x4E, 0x6B))
    quase = _img(tmp_path / "quase.png", (0x6A, 0x4E, 0xFF))   # 1 unidade de diferenca: dentro da tolerancia
    longe = _img(tmp_path / "longe.png", (0x7B, 0x5E, 0xFF))   # +16: fora da tolerancia
    reg = (50, 30, 150, 70)
    assert cor.analisar(certa, PRIMARIA, reg)["ok"] and not cor.analisar(errada, PRIMARIA, reg)["ok"]
    assert cor.analisar(quase, PRIMARIA, reg)["ok"] and not cor.analisar(longe, PRIMARIA, reg)["ok"]
    # sem regiao: fracao de pixels proximos do alvo
    assert cor.analisar(certa, PRIMARIA)["ok"] and not cor.analisar(errada, PRIMARIA)["ok"]
    assert cor.analisar(certa, PRIMARIA)["fracao_proxima"] == pytest.approx(0.2)


def test_delta_e_zero_e_simetrico():
    assert cor.delta_e((10, 20, 30), (10, 20, 30)) == 0
    assert cor.delta_e((10, 20, 30), (200, 20, 30)) == pytest.approx(cor.delta_e((200, 20, 30), (10, 20, 30)))


@pytest.mark.skipif(shutil.which("flutter") is None, reason="flutter ausente")
def test_tipografia_detecta_fonte_plantada(repo):  # noqa: F811
    tokens = json.loads((CAL / "tokens.json").read_text())
    with tag_copy(repo, "v1") as root:
        textos = tipografia.extrair(root, ["package:cal_app/features/entries/presentation/pages/entries_page.dart"],
                                    "const EntriesPage()", "Inter")
    r = tipografia.comparar(textos, tokens)
    assert [t["texto"] for t in textos] == ["Meus Registros", "fontSize: 12 e Color(0xFF111111) dentro de string nao contam"]
    assert r["M9_tipografia_fora_do_token"] == 1
    v = r["violacoes"][0]
    assert v["texto"] == "Meus Registros" and v["fontFamily"] == "Courier" and v["fontSize"] == 17.0 and v["motivos"] == ["familia", "tamanho"]


@pytest.mark.skipif(shutil.which("flutter") is None, reason="flutter ausente")
def test_tipografia_pagina_limpa_nao_gera_violacao(repo):  # noqa: F811
    tokens = json.loads((CAL / "tokens.json").read_text())
    with tag_copy(repo, "v1") as root:
        textos = tipografia.extrair(root, ["package:cal_app/features/chat/presentation/pages/chat_page.dart"], "const ChatPage()", "Inter")
    assert tipografia.comparar(textos, tokens)["M9_tipografia_fora_do_token"] == 0
