"""As quatro skills de ponta a ponta sobre o repositorio de calibracao, com avaliador SIMULADO (sem rede, sem chave)."""
import csv
import json
import re
import shutil
from pathlib import Path

import pytest
from PIL import Image

from harness.avaliador import anonimizar, avaliar_ciclo, avaliar_rf, csvio, julgar, julgar_rf, validar_juiz
from harness.avaliador.cliente import ClienteSimulado
from harness.estatico.tests.conftest import CAL

pytestmark = pytest.mark.skipif(shutil.which("flutter") is None or shutil.which("dart") is None, reason="flutter/dart ausentes")
CONTRATO = CAL / "backend-sintetico"


def _div(desc, ev, doc, causa):
    return {"description": desc, "evidence": ev, "documented": doc, "cause": causa}


A = _div("audit_entry added without being in the plan", ["lib/features/entries/domain/usecases/audit_entry.dart:4"], False, "ctx")
B = _div("timeline card added", ["lib/features/timeline/presentation/pages/timeline_card.dart:8"], True, "prd")
A2 = _div("audit entry imports data model", ["lib/features/entries/domain/usecases/audit_entry.dart:10"], False, "ctx")   # mesma divergencia (+-10 linhas)
C = _div("export not implemented", [], False, "inc")


@pytest.fixture(scope="module")
def saida(tmp_path_factory):
    return csvio.pasta_saida(tmp_path_factory.mktemp("avaliacao") / "saida")


@pytest.fixture(scope="module")
def imagens(tmp_path_factory):
    d = tmp_path_factory.mktemp("img")
    for n, cor in (("ref", (255, 255, 255)), ("cand", (250, 250, 250))):
        Image.new("RGB", (390, 844), cor).save(d / f"{n}.png")
    return d


def test_avaliar_rf_linha_v2_bate_com_o_gabarito(repo, gab, saida):
    r1, _ = avaliar_rf.linha_estatica(repo, "A", "F000", "v1", None, None, None)
    r2, _ = avaliar_rf.linha_estatica(repo, "A", "RF01", "v2", "v1", "specs/001-entries", CONTRATO)
    csvio.gravar(saida / "rf.csv", csvio.RF, [r1, r2], ("ciclo", "id_rf"))
    lin = {r["id_rf"]: r for r in csv.DictReader(open(saida / "rf.csv"))}
    g = gab
    v = lin["RF01"]
    assert list(csv.DictReader(open(saida / "rf.csv")))[0].keys() == set(csvio.RF) or list(csv.DictReader(open(saida / "rf.csv")))[0].keys() >= set(csvio.RF)
    assert int(v["M4"]) == g["m4"]["v2"]["total"] and float(v["M6_tasks"]) == g["m6"]["m6_tasks"]
    assert (int(v["M6_citados_nao_alterados"]), int(v["M6_alterados_nao_citados"]), int(v["M6_inexist_arq"]), int(v["M6_inexist_pkg"]), int(v["M6_inexist_backend"])) == (2, 3, 1, 1, 4)
    assert int(v["M7"]) == 3 and int(v["M7_novas"]) == g["m7"]["m7_novas_v2"] and int(v["M9_hardcodes"]) == 4 and int(v["M10_assinaturas"]) == 2
    assert abs(float(v["M8"]) - g["m8"]["v2"]["M8"]) < 1e-6
    assert abs(float(v["M12_media"]) - 3.1) < 1e-3 and int(v["M12_acima"]) == 1
    assert (float(v["M13"]), float(v["M13_sem_apagados"]), int(v["M13_apagados"]), float(v["M13_seguranca"])) == (0.2, 0.1, 1, 0.8)
    assert int(lin["F000"]["M4"]) == g["m4"]["v1"]["total"] and lin["F000"]["M6_tasks"] == ""   # primeira unidade: sem tag anterior


def test_julgar_rf_voto_majoritario_anonimizacao_e_log(repo, saida):
    cli = ClienteSimulado({"RF01": [{"divergences": [A, B, C]}, {"divergences": [A2]}, {"divergences": [A, C]}]})
    res, prompt = julgar_rf.julgar_unidade(repo, "A", "RF01", "v2", "v1", "specs/001-entries", saida, cli)
    # A em 3 execucoes, C em 2 (sem evidencia: mesma descricao), B so em 1 -> 2 divergencias, ambas nao documentadas
    assert not res["sem_maioria"] and res["voto"]["M6_div_nao_doc"] == 2 and len(res["voto"]["divergences"]) == 2
    assert len(cli.chamadas) == 3
    # cegamento: nada que identifique metodologia/ciclo/tag/data foi enviado
    for proibido in (r"spec[ -]?kit", r"\.specify", r"specs/", r"bmad", r"cicloA", r"\bv[12]\b.*tag", r"\d{4}-\d{2}-\d{2}"):
        assert not re.search(proibido, prompt, re.I), proibido
    assert "plan-docs/unit-001/plan.md" in prompt
    linhas = [json.loads(l) for l in open(saida / "julgamentos.jsonl")]
    assert len(linhas) == 3 and {l["execucao"] for l in linhas} == {1, 2, 3}
    for l in linhas:
        assert l["modelo_avaliador"] == "gpt-5.5-2026-04-23" and l["reasoning_effort"] == "medium" and l["metrica"] == "M6"
        assert l["ciclo_anon"] in ("X", "Y") and l["hash_prompt"] == julgar.hash_prompt("M6") and l["voto_final"]["M6_div_nao_doc"] == 2
    rf = {r["id_rf"]: r for r in csv.DictReader(open(saida / "rf.csv"))}
    assert rf["RF01"]["M6_div_nao_doc"] == "2"


def test_avaliar_ciclo_ciclo_csv_estados_e_m14(repo, saida, imagens, tmp_path):
    estados = [{"estado_id": "home", "cor_ok": True, "tipografia_ok": True, "screenshot": str(imagens / "cand.png"), "referencia": str(imagens / "ref.png")},
               {"estado_id": "menu", "cor_ok": True, "tipografia_ok": False, "screenshot": str(imagens / "cand.png"), "referencia": str(imagens / "ref.png")},
               {"estado_id": "excluir", "alcancavel": False}]
    cli = ClienteSimulado({"home": {"spacing_ok": True, "deviations": []}, "menu": {"spacing_ok": False, "deviations": []},
                           "D4": {"implemented": "yes", "evidence": ["lib/features/timeline/domain/usecases/build_timeline.dart:5"], "justification": "ok"}})
    ls = avaliar_ciclo.estados_m9("A", estados, saida, cli)
    assert [l["score"] for l in ls] == [3, 1, 0]
    r14 = avaliar_ciclo.m14(repo, "A", "v2", ".specify/memory/constitution.md", "specs/001-entries/plan.md", saida, cli)
    assert r14["M14"] == 0.5 and r14["selecionadas"] == 6 and [d["via"] for d in r14["decisoes"]].count("juiz") == 1
    dados = avaliar_ciclo.agregar_processo(CAL / "dados-sinteticos", "A")
    esperado = {"M1_instalacao_h": 600 / 3600, "M1_sessao_h": 0.5, "M1_total_h": 600 / 3600 + 0.5, "M1_calendario_h": 3.0, "M2_total_h": 1.5, "M2_plan_h": 0.0,
                "M2_espec_h": 3000 / 3600, "M2_impl_h": 2000 / 3600, "M2_valid_h": 0.0, "M3_tokens_total": 1900, "M3_sub_tokens_total": 45, "M3_tokens_espec": 1150,
                "M3_tokens_impl": 750, "M3_tokens_valid": 0, "M3_custo_usd": 2.0, "M3_razao_in_out": 2.0, "M3_frac_cache_read": round(1000 / 1700, 6), "M5_total": 2, "M5b_total": 1}
    for k, v in esperado.items():
        assert dados[k] == pytest.approx(v), k


def test_ciclo_csv_com_esquema_c002(repo, saida, tmp_path):
    cli = ClienteSimulado({"D4": {"implemented": "no", "evidence": [], "justification": "x"}})
    import sys
    argv = ["x", "--repo", str(repo), "--ciclo", "A", "--tag-final", "v2", "--tag-rf01", "v1", "--ref-feature", "entries", "--constitution",
            ".specify/memory/constitution.md", "--plan-f000", "specs/001-entries/plan.md", "--saida", str(saida), "--dados", str(CAL / "dados-sinteticos"),
            "--simulado", str(tmp_path / "sim.json")]
    (tmp_path / "sim.json").write_text(json.dumps({"D4": {"implemented": "yes", "evidence": [], "justification": "ok"}}))
    old, sys.argv = sys.argv, argv
    try:
        avaliar_ciclo.main()
    finally:
        sys.argv = old
    linha = list(csv.DictReader(open(saida / "ciclo.csv")))[0]
    assert list(linha.keys()) == csvio.CICLO
    assert linha["M4_total"] == "10" and linha["M15_divergencias"] == "7" and linha["M14"] == "0.5" and linha["M5_total"] == "2"


def test_validar_juiz_amostra_cega_e_kappa(saida, tmp_path):
    r = validar_juiz.sortear(saida / "julgamentos.jsonl", saida, {}, minimo=20)
    assert r["n_amostra"] >= 3 and r["avisos"]
    cega = json.loads((saida / "amostra-cega.json").read_text())
    texto = json.dumps(cega)
    assert all(set(c) == {"amostra_id", "metrica", "material"} for c in cega)        # sem voto, sem ciclo, sem item_id
    assert "voto" not in texto and "ciclo" not in texto and "item_id" not in texto
    chave = {c["amostra_id"]: c for c in json.loads((saida / "amostra-chave.json").read_text())}
    # humano concorda com o avaliador em tudo, exceto 1 (se houver >= 2 itens da metrica)
    with open(tmp_path / "cls.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["amostra_id", "classificacao_humana"])
        for sid, c in chave.items():
            w.writerow([sid, c["voto_avaliador"]])
    res = validar_juiz.calcular(saida, tmp_path / "cls.csv")
    assert all(v["kappa"] == 1.0 and not v["exploratoria"] for v in res.values())
    assert {r["metrica"] for r in csv.DictReader(open(saida / "validacao.csv"))} >= {"M6", "M9", "M14"}
    assert list(csv.DictReader(open(saida / "validacao.csv")))[0].keys() == set(csvio.VALIDACAO)


def test_kappa_valores_conhecidos():
    assert validar_juiz.kappa([("a", "a"), ("b", "b"), ("a", "a"), ("b", "b")]) == 1.0
    assert validar_juiz.kappa([("a", "b"), ("b", "a"), ("a", "b"), ("b", "a")]) == -1.0
    k = validar_juiz.kappa([("a", "a")] * 6 + [("b", "b")] * 2 + [("a", "b")] + [("b", "a")])
    assert abs(k - 0.523810) < 1e-5


def test_voto_m6_desempate_vai_para_amostra_humana():
    x = {"divergences": [_div("d", ["a.dart:1"], True, "ctx")]}
    y = {"divergences": [_div("d", ["a.dart:2"], False, "ctx")]}
    _, empate = julgar.voto_m6([x, y])
    assert empate is True


def test_saida_nunca_em_dados(tmp_path):
    with pytest.raises(SystemExit):
        csvio.pasta_saida(tmp_path / "dados" / "cicloA")


def test_anonimizacao_lista():
    t = "Spec Kit usa .specify/memory e specs/003-captura/plan.md; BMAD e bmm; ciclo em 2026-10-05 tag cicloA/rf03-done"
    a = anonimizar.anonimizar(t)
    for p in ("Spec Kit", ".specify", "specs/", "BMAD", "bmm", "2026-10-05", "cicloA"):
        assert p.lower() not in a.lower(), (p, a)
    assert "plan-docs/unit-003/plan.md" in a
    assert anonimizar.mapa_para("A", "RF01") != anonimizar.mapa_para("B", "RF01")
