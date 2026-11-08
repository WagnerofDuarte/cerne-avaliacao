#!/usr/bin/env python3
"""Agrega os JSON de `rodar.py` e `julgar_lote.py` em dois CSV: `rf.csv` (uma linha por ciclo e unidade) e `ciclo.csv`
(uma linha por ciclo). Nao calcula metrica nova: so achata os resultados dos modulos congelados.
Uso: python3 -m harness.produto.agregar --saida dados/produto --ciclos a,b"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from harness.produto.rodar import CICLOS


def lj(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", required=True)
    ap.add_argument("--ciclos", default="a,b")
    a = ap.parse_args()
    s = Path(a.saida)
    m6j = {(r["ciclo"], r["id_rf"]): r for r in (lj(s / "m6-julgado.json") or [])}
    rf, ciclo = [], []
    for ci in a.ciclos.split(","):
        m13 = {r["id_rf"]: r for r in (lj(s / f"{ci}-m13.json") or [])}
        for uid, tg, _ in CICLOS[ci]["unidades"]:
            d = lj(s / f"{ci}-{uid}.json")
            if d is None:
                continue
            m6 = d.get("M6") or {}
            cont = m6.get("contagens") or {}
            j = m6j.get((ci, uid)) or {}
            voto = j.get("voto") or {}
            m = m13.get(uid) or {}
            rf.append({"ciclo": ci, "id_rf": uid, "tag": d["tag"], "erro": d.get("erro", ""),
                       "M6_tasks": m6.get("M6_tasks"), "M6_citados_nao_alterados": cont.get("citados_nao_alterados"),
                       "M6_alterados_nao_citados": cont.get("alterados_nao_citados"), "M6_inexist_arq": cont.get("inexist_arq"),
                       "M6_inexist_pkg": cont.get("inexist_pkg"), "M6_inexist_backend": cont.get("inexist_backend"),
                       "M6_div_nao_doc_J": voto.get("M6_div_nao_doc"), "M6_J_sem_maioria": j.get("sem_maioria"), "M6_J_diff_truncado": j.get("diff_truncado"),
                       "M7": d.get("M7"), "RF07_bloc_importa_bloc": d.get("RF07_bloc_importa_bloc"), "RF10_chat_importa_entradas": d.get("RF10_chat_importa_entradas"),
                       "M9_hardcodes": d.get("M9_hardcodes"), "M10_assinaturas": d.get("M10_assinaturas"),
                       "M12_media": d.get("M12_media"), "M12_acima": d.get("M12_acima"), "M12_metodos": d.get("M12_metodos"),
                       "testes_total": d.get("testes_total"), "testes_aprovados": d.get("testes_aprovados"), "testes_codigo_saida": d.get("testes_codigo_saida"),
                       "M13": m.get("M13"), "M13_sem_apagados": m.get("M13_sem_apagados"), "M13_apagados": m.get("M13_apagados"), "M13_seguranca": m.get("M13_seguranca")})
        fin, m8, m8b, m14 = lj(s / f"{ci}-final.json") or {}, lj(s / f"{ci}-m8.json") or {}, lj(s / f"{ci}-m8b.json") or {}, lj(s / f"{ci}-m14.json") or {}
        m15 = (fin.get("M15") or {})
        ciclo.append({"ciclo": ci, "M8_cobertura": m8.get("M8") if "M8" in m8 else m8.get("cobertura"), "M8_detalhe": json.dumps({k: v for k, v in m8.items() if k != "arquivos"}, ensure_ascii=False)[:300] if m8 else "",
                      "M8b_mutation": m8b.get("M8b_mutation"), "M8b_mortos": m8b.get("mortos"), "M8b_sobreviventes": m8b.get("sobreviventes"), "M8b_amostra": m8b.get("amostra"),
                      "M8b_enumerados": m8b.get("mutantes_enumerados"),
                      "M14": m14.get("M14"), "M14_selecionadas": m14.get("selecionadas"), "M14_candidatas": m14.get("candidatas"),
                      "M15_divergencias": m15.get("M15_divergencias"), "M15_detalhe": json.dumps(m15, ensure_ascii=False)[:300] if m15 else ""})
    for nome, linhas in (("rf.csv", rf), ("ciclo.csv", ciclo)):
        if not linhas:
            continue
        cols = list(linhas[0].keys())
        with open(s / nome, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(linhas)
    print(f"rf.csv: {len(rf)} linhas; ciclo.csv: {len(ciclo)} linhas")


if __name__ == "__main__":
    main()
