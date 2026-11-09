#!/usr/bin/env python3
"""Resume `dados/produto/` em tabelas Markdown (D-099 a D-110). Nao mede nada: so le os CSV/JSON gerados por
`harness/produto/` e o `m11_p6.csv`, e roda o teste pareado (Wilcoxon, Pratt, p exato) com o codigo de `harness/h007/`.
Uso: python3 scripts/resumo_produto.py > /tmp/resumo.md
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.h007.analise_pareada import PARES, wilcoxon_pratt  # noqa: E402

D = ROOT / "dados" / "produto"
UNID = ["F000", "RF03", "RF01", "RF02", "RF07", "RF06", "RF04", "RF10", "RF08", "RF05", "RF09"]


def rd(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fmt(x, nd=2):
    if x is None:
        return "—"
    return f"{x:.{nd}f}" if isinstance(x, float) and not float(x).is_integer() else str(int(x)) if isinstance(x, float) else str(x)


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def pareado(rotulo, f_a, f_b, nota=""):
    """f_a(id) e f_b(id): valor da unidade (None se faltar)."""
    dif, a_v, b_v = [], [], []
    for _, ids_a, ids_b in PARES:
        va = [f_a(i) for i in ids_a]
        vb = [f_b(i) for i in ids_b]
        if any(v is None for v in va) or any(v is None for v in vb):
            continue
        a_v.append(sum(va))
        b_v.append(sum(vb))
        dif.append(sum(vb) - sum(va))
    if len(dif) < 5:
        return [rotulo, len(dif), "—", "—", "—", "—", "—", nota]
    w = wilcoxon_pratt(dif)
    return [rotulo, len(dif), fmt(statistics.median(a_v)), fmt(statistics.median(b_v)), fmt(statistics.median(dif)),
            f"{sum(1 for x in dif if x > 0)}/{sum(1 for x in dif if x < 0)}", f"{w['p_exato']:.4f} / {w['r_bisserial']:.2f}", nota]


def main():
    rf = {(r["ciclo"], r["id_rf"]): r for r in rd(D / "rf.csv")}
    cic = {r["ciclo"]: r for r in rd(D / "ciclo.csv")}
    p6 = {(r["ciclo"].lower(), r["unidade"]): r for r in rd(D / "m11_p6.csv")}
    out = []

    def val(c, u, k):
        return num(rf[(c, u)][k]) if (c, u) in rf and rf[(c, u)][k] not in ("", None) else None

    # 1. final por ciclo
    out.append("## Estado final por ciclo (tag `final`)\n")
    m8 = {c: json.loads((D / f"{c}-m8.json").read_text()) for c in "ab" if (D / f"{c}-m8.json").exists()}
    m8b = {c: json.loads((D / f"{c}-m8b.json").read_text()) for c in "ab" if (D / f"{c}-m8b.json").exists()}
    linhas = []
    for c in "ab":
        f = rf[(c, "RF09")]
        linhas.append([c.upper(), f["testes_total"], f["M7"], f["M9_hardcodes"], f["M10_assinaturas"], fmt(num(f["M12_media"]), 3), f["M12_acima"],
                       fmt(m8[c]["M8"] * 100, 1) + " %" if c in m8 else "—", cic[c]["M15_divergencias"], cic[c]["M14"] and fmt(num(cic[c]["M14"]), 3)])
    out.append(tabela(["Ciclo", "Testes", "M7 viol.", "M9 hardcodes", "M10 assin. fora", "M12 média", "M12 acima", "M8 domínio", "M15 diverg.", "M14"], linhas))

    # 2. M8b
    out.append("\n## M8b — mutação (domínio)\n")
    linhas = []
    for c in "ab":
        if c not in m8b:
            linhas.append([c.upper(), "não concluída"] + ["—"] * 5)
            continue
        m = m8b[c]
        linhas.append([c.upper(), m["mutantes_enumerados"], m["amostra"] or "todos", m["mortos"], m["sobreviventes"], m["erros_compilacao"],
                       fmt(m["M8b_mutation"] * 100, 1) + " %" if m["M8b_mutation"] is not None else "—"])
    out.append(tabela(["Ciclo", "Enumerados", "Amostra", "Mortos", "Sobreviventes", "Erro compilação", "Escore"], linhas))

    # 3. por unidade
    for titulo, ks in (("M6 — aderência ao plano (D = estática; J = juiz Opus 5.5, maioria de 3)",
                        [("M6_tasks", "tasks %"), ("M6_alterados_nao_citados", "alt. não citados"), ("M6_citados_nao_alterados", "citados não alt."),
                         ("M6_inexist_arq", "inex. arq"), ("M6_inexist_pkg", "inex. pkg"), ("M6_inexist_backend", "inex. backend"),
                         ("M6_div_nao_doc_J", "J div. não doc."), ("M6_J_diff_truncado", "J diff trunc.")]),
                       ("Qualidade estática e testes no estado de cada unidade",
                        [("M7", "M7"), ("M9_hardcodes", "M9"), ("M10_assinaturas", "M10"), ("M12_media", "M12"), ("testes_total", "testes"),
                         ("M13", "M13"), ("M13_apagados", "apagados")])):
        out.append(f"\n## {titulo}\n")
        cab = ["Unidade"] + [f"A {n}" for _, n in ks] + [f"B {n}" for _, n in ks]
        linhas = []
        for u in UNID:
            l = [u]
            for c in "ab":
                for k, _ in ks:
                    v = rf.get((c, u), {}).get(k, "")
                    n = num(v)
                    l.append("—" if v in ("", None) else (fmt(n, 3) if n is not None and not float(n).is_integer() else (str(int(n)) if n is not None else v)))
            linhas.append(l)
        out.append(tabela(cab, linhas))

    # 4. P6
    out.append("\n## M11-P6 — verificação manual de fechamento (não cega; D-103)\n")
    linhas = []
    for u in UNID:
        a, b = p6.get(("a", u)), p6.get(("b", u))
        linhas.append([u, a["p6_rodadas"], a["p6_1a_rodada_aprovada"], a["p6_aprovada_final"], b["p6_rodadas"], b["p6_1a_rodada_aprovada"], b["p6_aprovada_final"]])
    out.append(tabela(["Unidade", "A rodadas", "A 1ª aprovada", "A final", "B rodadas", "B 1ª aprovada", "B final"], linhas))

    # 5. testes pareados
    out.append("\n## Testes pareados (9 pares, Wilcoxon-Pratt, p exato bilateral / r bisserial; exploratório)\n")
    def fp(c, k):
        return lambda i: val(c, i, k)
    def fr(c):
        return lambda i: num(p6[(c, i)]["p6_rodadas"]) if (c, i) in p6 and num(p6[(c, i)]["p6_rodadas"]) is not None else None
    linhas = [
        pareado("P6 — rodadas até fechar", fr("a"), fr("b"), "A: RF01+RF02; B: só a RF01 (D-098)"),
        pareado("M6-D — arquivos alterados não citados", fp("a", "M6_alterados_nao_citados"), fp("b", "M6_alterados_nao_citados"), "B: plano = stories"),
        pareado("M6-J — divergências não documentadas", fp("a", "M6_div_nao_doc_J"), fp("b", "M6_div_nao_doc_J"), "diff do B truncado em 8/10 unidades"),
        pareado("M13 — testes apagados", fp("a", "M13_apagados"), fp("b", "M13_apagados"), "uma unidade do A concentra 38"),
    ]
    out.append(tabela(["Métrica", "n", "mediana A", "mediana B", "mediana das dif. (B−A)", "B>A / B<A", "p / r", "nota"], linhas))
    print("\n".join(out))


if __name__ == "__main__":
    main()
