import json
import shutil
import tempfile
from pathlib import Path

from holdout.maestro import verificar


def test_suite_completa_e_textos_do_prototipo():
    r = verificar.verificar()
    assert r["ok"], json.dumps(r, ensure_ascii=False, indent=1)
    assert r["n_fluxos"] == {"cenarios": 25, "falhas": 15, "estados": 31}
    assert set(r["excecoes_usadas"]) == {"Conversa sobre o dia no trabalho", "Conversa sobre o sono"}


def test_texto_inventado_e_pego(tmp_path, monkeypatch):
    (tmp_path / "X.yaml").write_text('appId: ${APP_ID}\n---\n- tapOn: "Texto que nao existe em lugar nenhum xyz"\n')
    monkeypatch.setattr(verificar, "AQUI", tmp_path)
    (tmp_path / "_comum").mkdir()
    r = verificar.verificar()
    assert "Texto que nao existe em lugar nenhum xyz" in r["texto_fora_do_prototipo"] and not r["ok"]


def test_manifesto_aponta_arquivos_existentes():
    man = json.loads((verificar.RAIZ / "suite.json").read_text())
    for grupo in ("cenarios", "falhas", "estados"):
        for cid, d in man[grupo].items():
            assert (verificar.RAIZ / d["flow"]).exists(), cid
    # todo cenario de proxy citado existe na tabela do addon
    from holdout.proxy.cenarios import CENARIOS
    usados = {d["proxy"] for g in ("cenarios", "falhas", "estados") for d in man[g].values() if d["proxy"]}
    assert usados <= set(CENARIOS), usados - set(CENARIOS)
