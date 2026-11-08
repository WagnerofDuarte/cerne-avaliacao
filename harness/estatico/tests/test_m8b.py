import shutil

import pytest

from harness.estatico import m8b_mutacao as m8b
from harness.estatico.common import tag_copy

pytestmark = pytest.mark.skipif(shutil.which("flutter") is None, reason="flutter ausente")


def test_enumerar_ignora_comentario_string_import_generico():
    src = ("import 'a.dart'; // x == y\nList<int> f(a, b) { var s = 'a == b && true'; return a == b && a <= b ? true : false; }\n"
           "g() => a > b;\n")
    ops = [(de, para, ln) for _, de, para, ln in m8b.enumerar(src)]
    assert ops == [("==", "!=", 2), ("&&", "||", 2), ("<=", "<", 2), ("true", "false", 2), ("false", "true", 2), (">", ">=", 3)] or \
        sorted(ops) == sorted([("==", "!=", 2), ("&&", "||", 2), ("<=", "<", 2), ("true", "false", 2), ("false", "true", 2), (">", ">=", 3)])


def test_m8b_acha_o_mutante_plantado(repo, gab):
    g = gab["m8b"]["v1"]
    with tag_copy(repo, "v1") as root:
        r = m8b.medir(root)
    assert (len(r["mutantes"]), r["mortos"], r["sobreviventes"], r["erros_compilacao"]) == (g["total"], g["mortos"], g["n_sobreviventes"], 0)
    assert abs(r["M8b_mutation"] - g["M8b_mutation"]) < 1e-6
    p = g["plantado"]
    assert any(m["arquivo"] == p["arquivo"] and m["linha"] == p["linha"] and m["de"] == p["de"] and m["para"] == p["para"]
               and m["estado"] == p["estado"] for m in r["mutantes"])
    viv = sorted((m["arquivo"], m["linha"]) for m in r["mutantes"] if m["estado"] == "sobrevivente")
    assert viv == sorted((a, l) for a, l, _ in g["lista_sobreviventes"])
