from harness.estatico import m4_artefatos, m13_regressao
from harness.estatico.common import tree_files


def test_m4_speckit(repo, gab):
    for tag in ("v1", "v2"):
        r = m4_artefatos.analisar_lista(tree_files(repo, tag), m4_artefatos.SPECKIT)["M4"]
        assert r == gab["m4"][tag], tag


def test_m4_decoys_nao_contam(repo):
    r = m4_artefatos.analisar_lista(tree_files(repo, "v2"), m4_artefatos.SPECKIT)["arquivos"]
    todos = {f for v in r.values() for f in v}
    assert "specs/001-entries/notes.txt" not in todos
    assert not any(f.startswith("lib/") or f.startswith("test/") for f in todos)


def test_m4_bmad_sintetico():
    files = ["_bmad-output/planning-artifacts/prd.md", "_bmad-output/planning-artifacts/architecture.md",
             "_bmad-output/planning-artifacts/epics.md", "_bmad-output/implementation-artifacts/sprint-status.yaml",
             "_bmad-output/implementation-artifacts/1-1-login.md", "lib/main.dart", "README.md"]
    r = m4_artefatos.analisar_lista(files, m4_artefatos.BMAD_PADRAO)["M4"]
    assert r["prd"] == 1 and r["arquitetura"] == 1 and r["total"] == 5


def test_m13_logica_sintetica():
    ant = {"a": "success", "b": "success", "c": "success", "d": "failure"}
    atu = {"a": "success", "b": "failure", "d": "success", "e": "success"}
    r = m13_regressao.comparar(ant, atu)
    assert r["regressoes"] == ["b"] and r["apagados"] == ["c"]
    assert r["M13"] == round(2 / 3, 6) and r["M13_sem_apagados"] == round(1 / 3, 6) and r["M13_seguranca"] == round(1 / 3, 6)


def test_m13_calibracao(repo, gab):
    g = gab["m13"]
    ant = m13_regressao.rodar_tag(repo, "v1")
    atu = m13_regressao.rodar_tag(repo, "v2")
    assert sorted(t for t, r in ant.items() if r == "success") == sorted(g["testes_v1_aprovados"])
    r = m13_regressao.comparar(ant, atu)
    assert r["regressoes"] == g["passa_em_v1_falha_em_v2"] and r["apagados"] == g["apagado_em_v2"]
    assert (r["M13"], r["M13_sem_apagados"], r["M13_apagados"], r["M13_seguranca"]) == (g["M13"], g["M13_sem_apagados"], g["M13_apagados"], g["M13_seguranca"])
