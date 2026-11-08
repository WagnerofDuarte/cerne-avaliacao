from harness.estatico import m6_aderencia as m6


def test_m6_calibracao(repo, gab, sintetico):
    g = gab["m6"]
    contrato = m6.carregar_contrato(sintetico / "openapi.yaml", sintetico / "error-taxonomy.md", sintetico / "README.md")
    r = m6.analisar(repo, g["unidade"]["tag_anterior"], g["unidade"]["tag"], g["unidade"]["unidade"], contrato)
    assert r["M6_tasks"] == g["m6_tasks"]
    assert r["M6_citados_nao_alterados"] == g["citados_nao_alterados"]
    assert r["M6_alterados_nao_citados"] == g["alterados_nao_citados"]
    assert r["M6_inexist_arq"] == g["inexist_arq"]
    assert r["M6_inexist_pkg"] == g["inexist_pkg"]
    assert r["M6_inexist_backend"] == g["inexist_backend"]
    assert r["contagens"]["inexist_backend"] == g["inexist_backend_total"]


def test_tasks_pct():
    assert m6.tasks_pct(["- [x] a\n- [ ] b\n  - [X] c\n- nada"]) == 2 / 3
    assert m6.tasks_pct(["sem checkbox"]) is None


def test_norm_rota():
    assert m6.norm_rota("/entries/:id") == m6.norm_rota("/entries/{entryId}") == "/entries/{}"
