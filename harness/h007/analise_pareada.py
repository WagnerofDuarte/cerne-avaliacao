#!/usr/bin/env python3
"""Análise pareada por requisito (plano de análise, seção 3.8 da monografia).

Pareamento: nove pares. A RF02 do Ciclo B não teve sessões (nota B7: a transcrição e o OCR
foram feitos nas stories 3.2 e 3.3 da RF01), então o par RF01 soma RF01 e RF02 do Ciclo A
contra a RF01 do Ciclo B. F000 e retrospectivas ficam fora do pareamento.

Métricas por par (diferença d = B - A):
  M2_iv   tempo ativo das fases IMPL + VALID (h). Leitura principal: nas unidades do B
          que passaram do teto (RF03, RF01, RF05, RF09) o valor é o do estado no teto,
          teto - tempo de ESPEC (censura). Sensibilidade 1: sem os pares censurados.
          Sensibilidade 2: valores observados, com a continuação além do teto.
  M2_u    tempo ativo da unidade inteira (ESPEC + IMPL + VALID), mesmo tratamento.
  M3_usd  custo (USD) da unidade inteira, valores observados (a censura só está definida em tempo).
  M3_out  tokens de saída da unidade (agente principal + subagentes), valores observados.
  M5      intervenções (leitura principal), valores observados.
Teste: postos sinalizados de Wilcoxon, diferenças nulas pelo método de Pratt, p exato bilateral
por permutação dos sinais, tamanho de efeito = correlação bisserial de postos (r = (W+ - W-)/(W+ + W-)).
"""
from __future__ import annotations

import csv
import itertools
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARES = [("RF03", ["RF03"], ["RF03"]), ("RF01+RF02", ["RF01", "RF02"], ["RF01"]), ("RF07", ["RF07"], ["RF07"]),
         ("RF06", ["RF06"], ["RF06"]), ("RF04", ["RF04"], ["RF04"]), ("RF10", ["RF10"], ["RF10"]),
         ("RF08", ["RF08"], ["RF08"]), ("RF05", ["RF05"], ["RF05"]), ("RF09", ["RF09"], ["RF09"])]


def rd(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fl(r, k):
    return float(r[k] or 0)


def rank_abs(vals):
    order = sorted(range(len(vals)), key=lambda i: abs(vals[i]))
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and abs(abs(vals[order[j + 1]]) - abs(vals[order[i]])) < 1e-9:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def wilcoxon_pratt(d):
    """Pratt: os zeros entram no ranqueamento e saem depois; p exato por permutação dos sinais."""
    n = len(d)
    ranks = rank_abs(d)
    pos = sum(r for r, x in zip(ranks, d) if x > 1e-9)
    neg = sum(r for r, x in zip(ranks, d) if x < -1e-9)
    nz = [r for r, x in zip(ranks, d) if abs(x) > 1e-9]
    tot = sum(nz)
    mean = tot / 2
    obs = abs(pos - mean)
    cnt = 0
    for signs in itertools.product((0, 1), repeat=len(nz)):
        w = sum(r for r, s in zip(nz, signs) if s)
        if abs(w - mean) >= obs - 1e-9:
            cnt += 1
    p = cnt / 2 ** len(nz)
    r_rb = (pos - neg) / tot if tot else 0.0
    return {"n": n, "n_nulos": n - len(nz), "W_pos": pos, "W_neg": neg, "p_exato": p, "r_bisserial": r_rb}


def main():
    rf = {(r["ciclo"], r["id_rf"]): r for r in rd(ROOT / "dados/processo/rf.csv")}

    def soma(c, ids, k):
        return sum(fl(rf[(c, i)], k) for i in ids)

    linhas = []
    for nome, ids_a, ids_b in PARES:
        b0 = rf[("b", ids_b[0])]
        censurado = str(b0["acima_do_teto"]).lower() == "true"
        teto = fl(b0, "teto_h")
        a_iv = soma("a", ids_a, "M2_impl_h") + soma("a", ids_a, "M2_valid_h")
        b_iv_obs = soma("b", ids_b, "M2_impl_h") + soma("b", ids_b, "M2_valid_h")
        b_esp = soma("b", ids_b, "M2_espec_h")
        b_iv = min(b_iv_obs, teto - b_esp) if censurado else b_iv_obs
        a_u = soma("a", ids_a, "M2_sessao_h")
        b_u_obs = soma("b", ids_b, "M2_sessao_h")
        b_u = min(b_u_obs, teto) if censurado else b_u_obs
        linhas.append({
            "par": nome, "censurado_B": censurado,
            "A_iv": a_iv, "B_iv": b_iv, "B_iv_obs": b_iv_obs,
            "A_u": a_u, "B_u": b_u, "B_u_obs": b_u_obs,
            "A_usd": soma("a", ids_a, "M3_custo_usd"), "B_usd": soma("b", ids_b, "M3_custo_usd"),
            "A_out": soma("a", ids_a, "M3_tokens_output") + soma("a", ids_a, "M3_sub_tokens_output"),
            "B_out": soma("b", ids_b, "M3_tokens_output") + soma("b", ids_b, "M3_sub_tokens_output"),
            "A_m5": soma("a", ids_a, "M5"), "B_m5": soma("b", ids_b, "M5"),
            "A_m5b": soma("a", ids_a, "M5b"), "B_m5b": soma("b", ids_b, "M5b"),
        })

    def teste(rotulo, ka, kb, sel=None):
        L = [l for l in linhas if sel is None or sel(l)]
        d = [l[kb] - l[ka] for l in L]
        w = wilcoxon_pratt(d)
        a = [l[ka] for l in L]
        b = [l[kb] for l in L]
        return {
            "metrica": rotulo, "n_pares": len(L), "mediana_A": round(statistics.median(a), 2),
            "mediana_B": round(statistics.median(b), 2), "mediana_dif": round(statistics.median(d), 2),
            "B_maior_em": sum(1 for x in d if x > 1e-9), "A_maior_em": sum(1 for x in d if x < -1e-9),
            "W_pos": w["W_pos"], "W_neg": w["W_neg"], "p_exato": round(w["p_exato"], 4),
            "r_bisserial": round(w["r_bisserial"], 2),
        }

    nao_cens = lambda l: not l["censurado_B"]  # noqa: E731
    saida = [
        teste("M2 IMPL+VALID (h) — principal, censura no teto", "A_iv", "B_iv"),
        teste("M2 IMPL+VALID (h) — sem pares censurados", "A_iv", "B_iv", nao_cens),
        teste("M2 IMPL+VALID (h) — observado, com continuação", "A_iv", "B_iv_obs"),
        teste("M2 unidade inteira (h) — censura no teto", "A_u", "B_u"),
        teste("M2 unidade inteira (h) — observado", "A_u", "B_u_obs"),
        teste("M3 custo da unidade (USD) — observado", "A_usd", "B_usd"),
        teste("M3 custo da unidade (USD) — sem pares censurados", "A_usd", "B_usd", nao_cens),
        teste("M3 tokens de saída da unidade — observado", "A_out", "B_out"),
        teste("M5 intervenções — observado", "A_m5", "B_m5"),
        teste("M5 intervenções — sem pares censurados", "A_m5", "B_m5", nao_cens),
        teste("M5b respostas PROCESSO — observado", "A_m5b", "B_m5b"),
    ]
    out = ROOT / "dados/processo"
    with open(out / "pareado_pares.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        for l in linhas:
            w.writerow({k: (round(v, 3) if isinstance(v, float) else v) for k, v in l.items()})
    with open(out / "pareado_testes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(saida[0].keys()))
        w.writeheader()
        w.writerows(saida)
    for l in linhas:
        print(l["par"], "cens" if l["censurado_B"] else "", "A_iv=%.2f B_iv=%.2f (obs %.2f) A_u=%.2f B_u=%.2f usd %.1f/%.1f M5 %d/%d M5b %d/%d" % (
            l["A_iv"], l["B_iv"], l["B_iv_obs"], l["A_u"], l["B_u"], l["A_usd"], l["B_usd"], l["A_m5"], l["B_m5"], l["A_m5b"], l["B_m5b"]))
    print()
    for s in saida:
        print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
