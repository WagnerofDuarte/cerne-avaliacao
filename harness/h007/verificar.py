#!/usr/bin/env python3
"""H-007 — verificação dos critérios do plano sobre a saída da re-derivação.

Só imprime PASS/FAIL e identificadores (regra 8): nenhum valor de tempo, token
ou custo é mostrado.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def rows(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ciclo", choices=["a", "b"], required=True)
    ap.add_argument("--rederivado", type=Path, default=None)
    ap.add_argument("--original", type=Path, default=None)
    a = ap.parse_args(argv)
    sub = {"a": "cicloA", "b": "cicloB"}[a.ciclo]
    orig_dir = a.original or ROOT / "dados" / sub
    red_dir = a.rederivado or orig_dir / "rederivado"
    S = rows(red_dir / "sessoes.csv")
    SEG = rows(red_dir / "segmentos.csv")
    INT = rows(red_dir / "intervencoes.csv")
    PRO = rows(red_dir / "revisoes_processo.csv")
    AUD = rows(red_dir / "auditoria.csv")
    ORIG = rows(orig_dir / "sessoes.csv")
    res: list[tuple[str, bool]] = []

    def check(nome: str, ok: bool) -> None:
        res.append((nome, bool(ok)))

    by = {r["sessao_id"]: r for r in S}
    pref = lambda p: next((r for r in S if r["sessao_id"].startswith(p)), None)  # noqa: E731

    # 1. uma linha por sessão (D-031, D-035)
    ids = [r["sessao_id"] for r in S]
    check("uma linha por sessao_id", len(ids) == len(set(ids)))
    # 2. toda sessão de unidade sem comando está na fase IMPL (plano §13.4)
    fases = {}
    for s in SEG:
        fases.setdefault(s["sessao_id"], set()).add((s["fase"], s["marcador_origem"]))
    sem_cmd = [sid for sid, fs in fases.items() if all(m in ("(nenhum)", "(correcao)") for _, m in fs)
               and by.get(sid, {}).get("id_rf") not in ("SETUP", "PLAN")]
    check("sessões de correção em IMPL (sem SETUP residual)", all(fases[sid] == {("IMPL", "(correcao)")} for sid in sem_cmd))
    # 3. contagem por tipo de intervenção sem tipos fora do protocolo
    tipos_ok = {"redirecionamento", "correção", "edição manual", "permissão negada", "interrupção", "esclarecimento não solicitado"}
    check("todos os tipos de intervenção são do protocolo", all(i["tipo"] in tipos_ok for i in INT))
    # 4. n_intervencoes e n_processo batem com as linhas das tabelas filhas
    ci = Counter(i["sessao_id"] for i in INT)
    cp = Counter(p["sessao_id"] for p in PRO)
    check("n_intervencoes == linhas de intervencoes.csv", all(int(r["n_intervencoes"]) == ci.get(r["sessao_id"], 0) for r in S))
    check("n_processo == linhas de revisoes_processo.csv", all(int(r["n_processo"]) == cp.get(r["sessao_id"], 0) for r in S))
    # 5. só as colunas esperadas mudaram em relação ao original
    esperadas = {"rate_limit_s", "n_processo", "n_intervencoes"}
    inesperadas = {c for r in AUD for c in r["colunas_alteradas"].split(";") if c} - esperadas
    check(f"colunas alteradas só entre {sorted(esperadas)} (D-044, D-015, D-020)", not inesperadas)
    # 6. linhas originais duplicadas viram uma só
    dup = Counter(r["sessao_id"] for r in ORIG)
    check("duplicatas de coleta da origem eliminadas", all(S.count(r) == 1 for r in [by[i] for i in dup if dup[i] > 1 and i in by]))

    if a.ciclo == "a":
        r = pref("391601bd")
        check("A: F000 391601bd tem 1 PROCESSO reconhecido (D-015)", r and r["n_processo"] == "1")
        for p in ("8963c779", "76a55d2d", "cf3759e2"):
            r = pref(p)
            ok = r and r["n_intervencoes"] == "1" and any(i["sessao_id"] == r["sessao_id"] and i["tipo"] == "correção" for i in INT)
            check(f"A: {p} tem 1 intervenção `correção` reconhecida mesmo colada (D-020)", ok)
        setup = [r["sessao_id"] for r in S if r["id_rf"] == "SETUP"]
        check("A: sessão SETUP tem fase ESPEC com speckit-constitution (D-014)",
              any(("ESPEC", "speckit-constitution") in fases.get(sid, set()) for sid in setup))
        check("A: 2 sessões sem coleta da RF04 incluídas (D-037)", all(pref(p) and pref(p)["id_rf"] == "RF04" for p in ("5256ebbb", "a18e05bf")))
    else:
        for p, u in (("7bbc5346", "RF03"), ("b03f306e", "RF01"), ("52633697", "RF01"), ("6be00999", "RF07"), ("15b67843", "RF04"), ("adf6b331", "RF08")):
            check(f"B: sessão sem coleta {p} incluída em {u} (D-094)", pref(p) and pref(p)["id_rf"] == u)
        check("B: nenhuma coluna alterada (coletado com o coletor corrigido)", not any(r["colunas_alteradas"] for r in AUD))

    falhas = [n for n, ok in res if not ok]
    for n, ok in res:
        print(("PASS " if ok else "FAIL ") + n)
    print(f"\n{len(res) - len(falhas)}/{len(res)} critérios atendidos")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
