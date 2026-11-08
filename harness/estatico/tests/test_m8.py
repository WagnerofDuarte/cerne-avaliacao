import shutil

import pytest

from harness.estatico import m8_cobertura as m8
from harness.estatico.common import tag_copy

pytestmark = pytest.mark.skipif(shutil.which("flutter") is None, reason="flutter ausente")


def test_parse_lcov():
    t = "SF:lib/a/domain/x.dart\nDA:1,3\nDA:2,0\nend_of_record\nSF:lib/a/data/y.dart\nDA:1,1\nend_of_record\n"
    d = m8.so_dominio(m8.parse_lcov(t))
    assert list(d) == ["lib/a/domain/x.dart"] and d["lib/a/domain/x.dart"] == (2, 1, [2])


@pytest.mark.parametrize("tag", ["v1", "v2"])
def test_m8_calibracao(repo, gab, tag):
    g = gab["m8"][tag]
    with tag_copy(repo, tag) as root:
        r = m8.medir(root)
    assert r["testes_falharam"] is g["testes_falharam"]
    assert (r["linhas_executaveis"], r["linhas_cobertas"]) == (g["linhas_executaveis"], g["linhas_cobertas"])
    assert abs(r["M8"] - g["M8"]) < 1e-6
    nc = {f: v["nao_cobertas"] for f, v in r["por_arquivo"].items() if v["nao_cobertas"]}
    esperado = dict(gab["m8"]["v1"]["nao_cobertas"])
    esperado.update(g.get("nao_cobertas_adicional", {}))
    assert nc == esperado
    # invariantes conferidos a mao
    assert r["por_arquivo"]["lib/features/entries/domain/usecases/validate_entry.dart"]["nao_cobertas"] == []
    assert r["por_arquivo"]["lib/features/entries/domain/usecases/classify_entry.dart"]["nao_cobertas"] == [24]


def test_m8_nao_deixa_lixo_no_repo(repo):
    antes = shutil.which("git")
    with tag_copy(repo, "v1") as root:
        m8.medir(root)
    import subprocess
    assert subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True).stdout == ""
