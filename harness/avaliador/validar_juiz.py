"""/validar-juiz — amostra cega, classificacoes humanas e kappa de Cohen por metrica.

Passo 1 `sortear`: escreve `amostra-cega.json` (amostra_id opaco, metrica e o MATERIAL a classificar; SEM voto do avaliador e
SEM ciclo de origem nem item_id) e `amostra-chave.json` (voto e ciclo_anon; para o script, NAO para o pesquisador).
Passo 2 `calcular`: le `classificacoes.csv` (amostra_id,classificacao_humana), junta o voto, grava `validacao.csv`
(esquema C-002) e `kappa.json` com kappa por metrica (limiar 0,61; abaixo: metrica exploratoria).
Amostra: >= `--minimo` (padrao 20) itens por metrica julgada, SOMADOS aos itens sem maioria (que entram sempre).
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from . import csvio

LIMIAR = 0.61


def voto_str(m, voto):
    if voto is None:
        return "sem_voto"
    return {"M6": lambda v: str(v["M6_div_nao_doc"]), "M9": lambda v: str(v["spacing_ok"]).lower(),
            "M14": lambda v: v["implemented"], "D16": lambda v: v["severity"]}[m](voto)


def itens_julgados(jsonl):
    itens = {}
    for l in Path(jsonl).read_text(encoding="utf-8").splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        itens.setdefault((r["metrica"], r["item_id"], r["ciclo_anon"]), r)
    return list(itens.values())


def sortear(jsonl, saida, material, minimo=20, semente=20260101):
    """material: {(metrica, item_id, ciclo_anon): texto a mostrar ao humano}."""
    rng = random.Random(semente)
    por_m = defaultdict(list)
    for r in itens_julgados(jsonl):
        por_m[r["metrica"]].append(r)
    cega, chave, n = [], [], 0
    avisos = []
    for m, rs in sorted(por_m.items()):
        sem = [r for r in rs if r["sem_maioria"]]
        resto = [r for r in rs if not r["sem_maioria"]]
        rng.shuffle(resto)
        pegos = resto[:minimo]
        if len(pegos) < minimo:
            avisos.append(f"{m}: so {len(rs)} itens julgados (minimo {minimo}); amostra = todos")
        for r in sem + pegos:
            n += 1
            sid = f"S{n:03d}"
            cega.append({"amostra_id": sid, "metrica": m, "material": material.get((m, r["item_id"], r["ciclo_anon"]), "")})
            chave.append({"amostra_id": sid, "metrica": m, "item_id": f"{r['item_id']}@{r['ciclo_anon']}", "voto_avaliador": voto_str(m, r["voto_final"]),
                          "sem_maioria": r["sem_maioria"]})
    rng.shuffle(cega)
    Path(saida, "amostra-cega.json").write_text(json.dumps(cega, indent=1, ensure_ascii=False))
    Path(saida, "amostra-chave.json").write_text(json.dumps(chave, indent=1, ensure_ascii=False))
    return {"n_amostra": len(cega), "por_metrica": dict(Counter(c["metrica"] for c in cega)), "avisos": avisos}


def kappa(pares):
    n = len(pares)
    if n == 0:
        return None
    cats = sorted({a for a, _ in pares} | {b for _, b in pares})
    po = sum(1 for a, b in pares if a == b) / n
    pe = sum((sum(1 for a, _ in pares if a == c) / n) * (sum(1 for _, b in pares if b == c) / n) for c in cats)
    return 1.0 if pe == 1 else round((po - pe) / (1 - pe), 6)


def calcular(saida, classificacoes):
    chave = {c["amostra_id"]: c for c in json.loads(Path(saida, "amostra-chave.json").read_text())}
    linhas, pares = [], defaultdict(list)
    for r in csvio.ler(classificacoes):
        c = chave[r["amostra_id"]]
        linhas.append({"metrica": c["metrica"], "item_id": c["item_id"], "classificacao_humana": r["classificacao_humana"],
                       "voto_avaliador": c["voto_avaliador"], "sem_maioria": c["sem_maioria"]})
        pares[c["metrica"]].append((r["classificacao_humana"], c["voto_avaliador"]))
    csvio.gravar(Path(saida) / "validacao.csv", csvio.VALIDACAO, linhas, ("metrica", "item_id"))
    res = {m: {"n": len(p), "kappa": kappa(p), "exploratoria": (kappa(p) is None or kappa(p) < LIMIAR)} for m, p in pares.items()}
    Path(saida, "kappa.json").write_text(json.dumps(res, indent=1))
    return res


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("sortear"); s.add_argument("--saida", required=True); s.add_argument("--minimo", type=int, default=20); s.add_argument("--material")
    c = sp.add_parser("calcular"); c.add_argument("--saida", required=True); c.add_argument("--classificacoes", required=True)
    a = ap.parse_args()
    saida = csvio.pasta_saida(a.saida)
    if a.cmd == "sortear":
        mat = {}
        if a.material:
            for r in json.loads(Path(a.material).read_text()):
                mat[(r["metrica"], r["item_id"], r["ciclo_anon"])] = r["material"]
        print(json.dumps(sortear(saida / "julgamentos.jsonl", saida, mat, a.minimo), ensure_ascii=False))
    else:
        print(json.dumps(calcular(saida, a.classificacoes), ensure_ascii=False))


if __name__ == "__main__":
    main()
