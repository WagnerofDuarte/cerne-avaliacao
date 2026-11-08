"""/julgar-rf — M6 parte J: plano anonimizado + diff (so lib/ e test/) -> 3 execucoes -> voto -> julgamentos.jsonl
e `M6_div_nao_doc` em rf.csv.

Uso: python3 -m harness.avaliador.julgar_rf --repo <repo> --ciclo A --id-rf RF01 --tag v2 --tag-anterior v1 \
       --unidade-dir specs/001-entries --saida calibracao/saida [--simulado respostas.json]
Sem --simulado usa a API real (OPENAI_API_KEY no ambiente).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from harness.estatico.common import diff_added_lines, git, show

from . import anonimizar, csvio, julgar
from .cliente import ClienteReal, ClienteSimulado


def montar_entrada(repo, tag, anterior, unidade, secs=None, arquivos=None):
    # `arquivos` (D-105): {caminho_no_repo: texto}; Ciclo B passa as stories da unidade
    secs = secs or anonimizar.carregar()
    docs = []
    fontes = arquivos if arquivos is not None else {f"{unidade}/{n}": show(repo, tag, f"{unidade}/{n}") for n in ("spec.md", "plan.md", "tasks.md")}
    for caminho, t in fontes.items():
        if t:
            docs.append(f"--- {anonimizar.anonimizar_caminho(caminho, secs)} ---\n{anonimizar.anonimizar(t, secs)}")
    plano = "\n\n".join(docs)
    diff = git(repo, "diff", "--no-renames", "-U3", anterior, tag, "--", "lib", "test")
    anot = ["", "ADDED LINES WITH NEW-FILE LINE NUMBERS:"]
    for p, lst in sorted(diff_added_lines(repo, anterior, tag).items()):
        if p.startswith(("lib/", "test/")):
            anot += [f"{p}:{n}: {t}" for n, t in lst]
    return plano, anonimizar.anonimizar(diff, secs) + "\n".join(anot)


def julgar_unidade(repo, ciclo, id_rf, tag, anterior, unidade, saida, cliente, arquivos=None):
    plano, diff = montar_entrada(repo, tag, anterior, unidade, arquivos=arquivos)
    prompt = julgar.preencher("M6", PLAN=plano, DIFF=diff)
    h = hashlib.sha256(prompt.encode()).hexdigest()
    anon = anonimizar.mapa_para(ciclo, id_rf)
    res = julgar.julgar("M6", id_rf, anon, prompt, h, cliente, Path(saida) / "julgamentos.jsonl")
    linhas = csvio.ler(Path(saida) / "rf.csv")
    for r in linhas:
        if r["ciclo"] == ciclo and r["id_rf"] == id_rf and res["voto"] is not None:
            r["M6_div_nao_doc"] = res["voto"]["M6_div_nao_doc"]
            csvio.gravar(Path(saida) / "rf.csv", csvio.RF, [r], ("ciclo", "id_rf"))
    return res, prompt


def cliente_de(simulado):
    if simulado:
        return ClienteSimulado(json.loads(Path(simulado).read_text()))
    return ClienteReal()


def main():
    ap = argparse.ArgumentParser()
    for k in ("repo", "ciclo", "id-rf", "tag", "tag-anterior", "unidade-dir", "saida"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--simulado")
    a = ap.parse_args()
    saida = csvio.pasta_saida(a.saida)
    res, _ = julgar_unidade(a.repo, a.ciclo, a.id_rf, a.tag, a.tag_anterior, a.unidade_dir, saida, cliente_de(a.simulado))
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
