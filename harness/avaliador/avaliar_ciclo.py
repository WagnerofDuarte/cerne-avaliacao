"""/avaliar-ciclo — agrega M1–M5, M8b, M9, M10_cenarios, M14 e M15 em ciclo.csv; grava estados_m9.csv
(esquema C-002). Roda so apos `cicloX/final`. Saida SEMPRE em pasta de calibracao/avaliacao, nunca em dados/.

Aproximacoes registradas (a conferir com dados reais na Parte IV): M1/M2/M3/M5 agregam os CSVs da coleta
(`--dados`, com sessoes/segmentos/intervencoes/revisoes_processo/tags .csv) por soma simples; `M2_plan_h` =
segmentos com id_rf=PLAN; `M2_espec/impl/valid_h` = demais segmentos por fase, sem os de rate limit;
`M9 score` = cor_ok + tipografia_ok + espacamento_ok (rubrica de 3 pontos; estado inalcancavel = 0).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path

from harness.estatico import m4_artefatos, m14_decisoes, m15_consistencia
from harness.estatico.common import show, tag_copy, tree_files

from . import anonimizar, csvio, julgar
from .cliente import ClienteReal, ClienteSimulado


def _f(x, d=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def agregar_processo(pasta, ciclo):
    """M1, M2, M3, M5 a partir dos CSVs da coleta (todos filtrados por `ciclo`)."""
    ler = lambda n: [r for r in csvio.ler(Path(pasta) / n) if r.get("ciclo") == ciclo]
    ses, seg, itv, rev, tags = ler("sessoes.csv"), ler("segmentos.csv"), ler("intervencoes.csv"), ler("revisoes_processo.csv"), ler("tags.csv")
    h = lambda s: s / 3600
    inst = [r for r in ses if r["tipo_sessao"] == "instalacao"]
    dev = [r for r in ses if r["tipo_sessao"] == "desenvolvimento"]
    o = {"M1_instalacao_h": h(sum(_f(r["duracao_s"]) for r in inst)),
         "M1_sessao_h": h(sum(_f(r["duracao_s"]) for r in dev if r["id_rf"] == "SETUP"))}
    o["M1_total_h"] = o["M1_instalacao_h"] + o["M1_sessao_h"]
    fim = next((r["data"] for r in tags if r["tipo"] == "setup-done"), None)
    ini = min((r["inicio"] for r in inst), default=None)
    o["M1_calendario_h"] = h((datetime.fromisoformat(fim) - datetime.fromisoformat(ini)).total_seconds()) if fim and ini else ""
    util = [s for s in seg if s.get("excluido_rate_limit", "").lower() != "true"]
    o["M2_total_h"] = h(sum(_f(r["duracao_s"]) for r in dev))
    o["M2_plan_h"] = h(sum(_f(s["duracao_s"]) for s in util if s["id_rf"] == "PLAN"))
    for fase, k in (("ESPEC", "espec"), ("IMPL", "impl"), ("VALID", "valid")):
        o[f"M2_{k}_h"] = h(sum(_f(s["duracao_s"]) for s in util if s["fase"] == fase and s["id_rf"] != "PLAN"))
    tok = lambda rows, pre: sum(_f(r[pre + c]) for r in rows for c in ("tokens_input", "tokens_output", "cache_read", "cache_write")) if pre == "" else \
        sum(_f(r["sub_" + c]) for r in rows for c in ("tokens_input", "tokens_output", "cache_read", "cache_write"))
    o["M3_tokens_total"], o["M3_sub_tokens_total"] = tok(dev, ""), tok(dev, "sub")
    for fase, k in (("ESPEC", "espec"), ("IMPL", "impl"), ("VALID", "valid")):
        o[f"M3_tokens_{k}"], o[f"M3_sub_tokens_{k}"] = tok([s for s in seg if s["fase"] == fase], ""), tok([s for s in seg if s["fase"] == fase], "sub")
    o["M3_custo_usd"] = sum(_f(r["custo_usd"]) for r in dev)
    ti, to = sum(_f(r["tokens_input"]) for r in dev), sum(_f(r["tokens_output"]) for r in dev)
    cr, cw = sum(_f(r["cache_read"]) for r in dev), sum(_f(r["cache_write"]) for r in dev)
    o["M3_razao_in_out"] = round(ti / to, 6) if to else ""
    o["M3_frac_cache_read"] = round(cr / (ti + cr + cw), 6) if (ti + cr + cw) else ""
    o["M5_total"], o["M5b_total"] = len(itv), len(rev)
    return o


def estados_m9(ciclo, estados, saida, cliente, escala=3):
    """estados: [{estado_id, cor_ok, tipografia_ok, screenshot, referencia, alcancavel}] -> estados_m9.csv + julgamentos."""
    linhas = []
    for e in estados:
        if not e.get("alcancavel", True):
            linhas.append({"ciclo": ciclo, "estado_id": e["estado_id"], "cor_ok": False, "tipografia_ok": False, "espacamento_ok": False, "score": 0})
            continue
        prompt = julgar.preencher("M9", SCALE=escala)
        h = hashlib.sha256(Path(e["screenshot"]).read_bytes() + Path(e["referencia"]).read_bytes()).hexdigest()
        res = julgar.julgar("M9", e["estado_id"], anonimizar.mapa_para(ciclo, e["estado_id"]), prompt, h, cliente, Path(saida) / "julgamentos.jsonl",
                            imagens=(e["referencia"], e["screenshot"]))
        esp = bool(res["voto"]["spacing_ok"]) if res["voto"] else False
        linhas.append({"ciclo": ciclo, "estado_id": e["estado_id"], "cor_ok": bool(e["cor_ok"]), "tipografia_ok": bool(e["tipografia_ok"]),
                       "espacamento_ok": esp, "score": int(bool(e["cor_ok"])) + int(bool(e["tipografia_ok"])) + int(esp)})
    csvio.gravar(Path(saida) / "estados_m9.csv", csvio.ESTADOS, linhas, ("ciclo", "estado_id"))
    return linhas


def codigo_para_juiz(root, d, limite_chars=200_000):
    """Arvore de lib/ e conteudo dos arquivos que contem os termos-chave da decisao (ordem por no de ocorrencias)."""
    lib = sorted(p for p in (Path(root) / "lib").rglob("*.dart"))
    arvore = "\n".join(p.relative_to(root).as_posix() for p in lib)
    termos = [t for t in d["identificadores"] if not t.startswith("lib/")] + [Path(t).stem for t in d["identificadores"] if t.startswith("lib/")]
    pont = []
    for p in lib:
        txt = p.read_text(encoding="utf-8", errors="replace")
        n = sum(txt.count(t) for t in termos)
        if n:
            pont.append((n, p, txt))
    pont.sort(key=lambda x: -x[0])
    out, usado, so_caminho = [], 0, []
    for n, p, txt in pont:
        if usado + len(txt) > limite_chars:
            so_caminho.append(p.relative_to(root).as_posix())
            continue
        usado += len(txt)
        out.append(f"--- {p.relative_to(root).as_posix()} ---\n{txt}")
    return arvore, "\n\n".join(out) + ("\n\n(only path, over size limit):\n" + "\n".join(so_caminho) if so_caminho else "")


def m14(repo, ciclo, tag, constitution, plan, saida, cliente):
    with tag_copy(repo, tag) as root:
        r = m14_decisoes.analisar(root, Path(root) / constitution, Path(root) / plan)
        impl = 0
        detalhe = []
        for d in r["decisoes"]:
            if d["estatica"]:
                ok = d["esperado"] == "ok"
                detalhe.append({"ordem": d["ordem"], "via": "estatica", "implementada": ok})
                impl += ok
                continue
            arv, arqs = codigo_para_juiz(root, {"identificadores": d["identificadores"]})
            prompt = julgar.preencher("M14", DECISION=anonimizar.anonimizar(d["texto"]), TREE=arv, FILES=arqs)
            res = julgar.julgar("M14", f"D{d['ordem']}", anonimizar.mapa_para(ciclo, f"D{d['ordem']}"), prompt,
                                hashlib.sha256(prompt.encode()).hexdigest(), cliente, Path(saida) / "julgamentos.jsonl")
            v = res["voto"]["implemented"] if res["voto"] else None
            detalhe.append({"ordem": d["ordem"], "via": "juiz", "implementada": v == "yes", "voto": v, "sem_maioria": res["sem_maioria"]})
            impl += v == "yes"
    n = len(r["decisoes"])
    return {"M14": round(impl / n, 6) if n else "", "decisoes": detalhe, "selecionadas": n, "candidatas": r["total_candidatas"]}


def main():
    ap = argparse.ArgumentParser()
    for k in ("repo", "ciclo", "tag-final", "saida"):
        ap.add_argument(f"--{k}", required=True)
    ap.add_argument("--tag-rf01", required=True)
    ap.add_argument("--ref-feature", required=True)
    ap.add_argument("--constitution", required=True)
    ap.add_argument("--plan-f000", required=True)
    ap.add_argument("--dados", help="pasta com os CSVs da coleta (sinteticos na calibracao)")
    ap.add_argument("--estados-json")
    ap.add_argument("--hold-out")
    ap.add_argument("--simulado")
    ap.add_argument("--metodologia", default="speckit")
    a = ap.parse_args()
    saida = csvio.pasta_saida(a.saida)
    cliente = ClienteSimulado(json.loads(Path(a.simulado).read_text())) if a.simulado else ClienteReal()
    linha = {"ciclo": a.ciclo}
    if a.dados:
        linha.update(agregar_processo(a.dados, a.ciclo))
    linha["M4_total"] = m4_artefatos.analisar_lista(tree_files(a.repo, a.tag_final), m4_artefatos.SPECKIT if a.metodologia == "speckit" else m4_artefatos.BMAD_PADRAO)["M4"]["total"]
    m8b = saida / f"m8b-{a.ciclo}.json"
    linha["M8b_mutation"] = json.loads(m8b.read_text())["M8b_mutation"] if m8b.exists() else ""
    ho = json.loads(Path(a.hold_out).read_text()) if a.hold_out else {}
    linha["M10_cenarios"] = ho.get("M10_cenarios", "")
    r14 = m14(a.repo, a.ciclo, a.tag_final, a.constitution, a.plan_f000, saida, cliente)
    linha["M14"] = r14["M14"]
    with tag_copy(a.repo, a.tag_rf01) as r1, tag_copy(a.repo, a.tag_final) as r2:
        linha["M15_divergencias"] = m15_consistencia.analisar(r1, r2, a.ref_feature)["M15_divergencias"]
    if a.estados_json:
        ls = estados_m9(a.ciclo, json.loads(Path(a.estados_json).read_text()), saida, cliente)
        linha["M9_score_medio"] = round(sum(l["score"] for l in ls) / len(ls), 6) if ls else ""
    csvio.gravar(saida / "ciclo.csv", csvio.CICLO, [linha], ("ciclo",))
    (saida / f"m14-{a.ciclo}.json").write_text(json.dumps(r14, indent=1, ensure_ascii=False))
    print(json.dumps({"ciclo.csv": str(saida / "ciclo.csv"), "linha": linha}, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
