#!/usr/bin/env python3
"""Lote do avaliador Claude (D-099): M6-J por unidade e M14-J por decisao, em paralelo entre itens.
Cada item grava num arquivo proprio (sem corrida) e depois todos sao concatenados em `julgamentos.jsonl`.
Rotulo de todos os resultados: EXPLORATORIO (validacao humana pendente).

Uso: python3 -m harness.produto.julgar_lote --etapa m6|m14 --ciclos a,b --saida dados/produto [--modelo claude-opus-5-5]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from harness.avaliador import anonimizar, avaliar_ciclo, julgar, julgar_rf
from harness.avaliador.cliente import ClienteClaude
from harness.produto.rodar import CICLOS, arquivos_b, tag_de

LIMITE_DIFF = 700_000   # caracteres do diff anonimizado enviado ao juiz (D-105: truncamento declarado)
VAZAMENTO = re.compile(r"spec[ -]?kit|speckit|\bbmad|party[ -]mode|\.specify|_bmad", re.I)


def m6_item(ciclo, idx, saida, cliente):
    c = CICLOS[ciclo]
    uid, tg, pasta = c["unidades"][idx]
    tag = tag_de(c, tg)
    prev = tag_de(c, c["base"] if idx == 0 else c["unidades"][idx - 1][1])
    arquivos = arquivos_b(c, uid, tag) if c["metodologia"] == "bmad" else None
    if c["metodologia"] == "bmad" and not arquivos:
        return {"ciclo": ciclo, "id_rf": uid, "pulado": "sem stories (nota B7)"}
    plano, diff = julgar_rf.montar_entrada(c["repo"], tag, prev, pasta or "", arquivos=arquivos)
    truncado = len(diff) > LIMITE_DIFF
    if truncado:
        diff = diff[:LIMITE_DIFF] + "\n\n[... diff truncated by the harness at %d characters ...]" % LIMITE_DIFF
    prompt = julgar.preencher("M6", PLAN=plano, DIFF=diff)
    h = hashlib.sha256(prompt.encode()).hexdigest()
    cod = ciclo.upper()
    arq = Path(saida) / "julgamentos" / f"m6-{ciclo}-{uid}.jsonl"
    arq.parent.mkdir(parents=True, exist_ok=True)
    if arq.exists():
        arq.unlink()
    res = julgar.julgar("M6", f"{cod}-{uid}", anonimizar.mapa_para(cod, uid), prompt, h, cliente, arq)
    return {"ciclo": ciclo, "id_rf": uid, "voto": res["voto"], "sem_maioria": res["sem_maioria"], "diff_truncado": truncado,
            "chars_prompt": len(prompt), "vazamentos_no_prompt": len(VAZAMENTO.findall(prompt))}


def m14_ciclo(ciclo, saida, cliente):
    c = CICLOS[ciclo]
    pasta = Path(saida) / "julgamentos" / f"m14-{ciclo}"
    pasta.mkdir(parents=True, exist_ok=True)
    j = pasta / "julgamentos.jsonl"
    if j.exists():
        j.unlink()
    r = avaliar_ciclo.m14(c["repo"], ciclo.upper(), tag_de(c, "final"), c["constitution"], c["plan_f000"], pasta, cliente)
    (Path(saida) / f"{ciclo}-m14.json").write_text(json.dumps(r, ensure_ascii=False, indent=1))
    return {"ciclo": ciclo, "M14": r["M14"], "selecionadas": r["selecionadas"], "candidatas": r["candidatas"]}


def concatenar(saida):
    base = Path(saida) / "julgamentos"
    linhas = []
    for f in sorted(base.rglob("*.jsonl")):
        if f.name != "todos.jsonl":
            linhas += f.read_text(encoding="utf-8").splitlines()
    (Path(saida) / "julgamentos.jsonl").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return len(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--etapa", required=True, choices=["m6", "m14"])
    ap.add_argument("--ciclos", default="a,b")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--modelo", default="claude-opus-5-5")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--so", help="ids de unidade (m6), separados por virgula")
    a = ap.parse_args()
    cliente = ClienteClaude(a.modelo)
    ciclos = a.ciclos.split(",")
    if a.etapa == "m6":
        alvos = [(ci, i) for ci in ciclos for i, (u, _, _) in enumerate(CICLOS[ci]["unidades"]) if not a.so or u in a.so.split(",")]
        with ThreadPoolExecutor(a.workers) as ex:
            res = list(ex.map(lambda t: m6_item(t[0], t[1], a.saida, cliente), alvos))
        (Path(a.saida) / "m6-julgado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        with ThreadPoolExecutor(len(ciclos)) as ex:
            res = list(ex.map(lambda ci: m14_ciclo(ci, a.saida, cliente), ciclos))
        (Path(a.saida) / "m14-julgado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    n = concatenar(a.saida)
    print(json.dumps({"itens": len(res), "linhas_log": n, "modelos_observados": sorted(cliente.modelos_observados),
                      "chamadas": cliente.chamadas, "custo_usd": round(cliente.custo_usd, 2)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
