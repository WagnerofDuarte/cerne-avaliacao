import shutil

import pytest

from harness.estatico import m12_complexidade as m12
from harness.estatico.common import tag_copy

pytestmark = pytest.mark.skipif(shutil.which("dart") is None, reason="dart ausente")


def _esperado(g, tag):
    ms = list(g["v1"]) + (list(g["v2_adiciona"]) if tag == "v2" else [])
    return sorted((m["arquivo"], m["linha"], m["metodo"], m["cc"]) for m in ms)


@pytest.mark.parametrize("tag", ["v1", "v2"])
def test_m12_calibracao(repo, gab, tag):
    g = gab["m12"]
    with tag_copy(repo, tag) as root:
        r = m12.rodar(root)
    got = sorted((m["arquivo"], m["linha"], m["metodo"], m["cc"]) for m in r["detalhe"])
    assert got == _esperado(g, tag)
    resumo = g[f"{tag}_resumo"]
    assert (r["metodos"], r["soma"], r["M12_acima"]) == (resumo["metodos"], resumo["soma"], resumo["acima_de_10"])
    assert abs(r["M12_media"] - resumo["media"]) < 1e-3
