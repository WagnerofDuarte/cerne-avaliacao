#!/usr/bin/env python3
"""V-005 (parte de processo) — agrega M1, M2, M3, M5 e M5b a partir das tabelas
re-derivadas (H-007, D-096). Grava `dados/processo/ciclo.csv` (uma linha por
ciclo, esquema da §8.2 do documento de métricas) e `dados/processo/rf.csv`
(uma linha por unidade e ciclo).

Definições (documento de métricas v1.0, §5.1):
  M1  = instalação + sessões SETUP (tempo ativo) + calendário (instalação -> setup-done).
  M2  = tempo ativo por unidade e total (P5c); por fase pela soma do tempo ativo
        dos segmentos; PLAN em linha própria (zero no Spec Kit por construção);
        as retrospectivas do B (sessões PLAN depois de plan-done, D-092/D-093)
        ficam em `M2_retro_h`, fora de `M2_plan_h`.
        Tempo de calendário da unidade = tag anterior -> tag da unidade.
  M3  = tokens por categoria (principal e subagentes à parte), custo pela tabela
        congelada; por fase só do agente principal (os subagentes não são
        discriminados por fase na coleta).
  M5  = linhas de `intervencoes.csv`; M5b = linhas de `revisoes_processo.csv`.
Leitura principal da M5: intervenções reconhecidas, sem as das sessões sem coleta
(D-037, D-094: a mesma mensagem foi reenviada e coletada em outra sessão).
Leitura ampla da M5 (sensibilidade): acrescenta as das sessões sem coleta e soma das mensagens livres das categorias
`interrupcao`, `retomada` e `outra` (D-020, D-036, D-059, D-072, D-074 e
posteriores); `neutra` e `painel_sem_prefixo` não contam.
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNIDADES = ["F000", "RF03", "RF01", "RF02", "RF07", "RF06", "RF04", "RF10", "RF08", "RF05", "RF09"]
FASES = ["ESPEC", "IMPL", "VALID"]
TIPOS = ["redirecionamento", "correção", "edição manual", "permissão negada", "interrupção", "esclarecimento não solicitado"]
CAUSAS = ["ctx", "chk", "inc", "prd", "amb", "out"]
TETO_H = {"F000": 12.0}
TETO_PADRAO_H = 8.0


def rd(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def h(sec: float) -> float:
    return round(sec / 3600.0, 3)


def agregar(ciclo: str, dados: Path):
    red = dados / "rederivado"
    S = rd(red / "sessoes.csv")
    SEG = rd(red / "segmentos.csv")
    INT = rd(red / "intervencoes.csv")
    PRO = rd(red / "revisoes_processo.csv")
    LIV = rd(red / "mensagens_livres.csv")
    TAGS = rd(dados / "tags.csv")
    tag_data = {t["tag"].split("/")[1]: ts(t["data"]) for t in TAGS}
    tag_tipo = {t["tag"].split("/")[1]: t["tipo"] for t in TAGS}
    tag_commit = {t["tag"].split("/")[1]: t["commit"] for t in TAGS}

    ins = [r for r in S if r["tipo_sessao"] == "instalacao"]
    desenv = [r for r in S if r["tipo_sessao"] != "instalacao"]
    f = lambda r, k: float(r.get(k) or 0)  # noqa: E731

    # ---- M1
    m1_inst = sum(f(r, "duracao_s") for r in ins)
    m1_sessao = sum(f(r, "duracao_s") for r in desenv if r["id_rf"] == "SETUP")
    inst_inicio = min((ts(r["inicio"]) for r in ins), default=tag_data["instalado"])
    m1_cal = (tag_data["setup-done"] - inst_inicio).total_seconds()

    # ---- M2
    plan_done = tag_data.get("plan-done")
    plan_rows = [r for r in desenv if r["id_rf"] == "PLAN"]
    plan_ate = [r for r in plan_rows if plan_done is None or ts(r["inicio"]) <= plan_done]
    retro = [r for r in plan_rows if plan_done is not None and ts(r["inicio"]) > plan_done]
    unid_rows = [r for r in desenv if r["id_rf"] in UNIDADES]
    m2_total = sum(f(r, "duracao_s") for r in desenv)
    fase_s = Counter()
    for sg in SEG:
        fase_s[sg["fase"]] += f(sg, "duracao_ativa_s")

    # ---- M3 (principal, subagentes) por categoria; por fase só principal
    cat = ["tokens_input", "tokens_output", "cache_read", "cache_write"]
    sub = ["sub_tokens_input", "sub_tokens_output", "sub_cache_read", "sub_cache_write"]
    tot = {k: sum(f(r, k) for r in desenv) for k in cat + sub}
    custo = sum(f(r, "custo_usd") for r in desenv)
    tok_fase = {fa: {k: 0.0 for k in cat} for fa in FASES + ["SETUP"]}
    for sg in SEG:
        fa = sg["fase"] if sg["fase"] in tok_fase else "SETUP"
        for k in cat:
            tok_fase[fa][k] += f(sg, k)
    in_total = tot["tokens_input"] + tot["cache_read"] + tot["cache_write"] + tot["sub_tokens_input"] + tot["sub_cache_read"] + tot["sub_cache_write"]
    out_total = tot["tokens_output"] + tot["sub_tokens_output"]
    cr_total = tot["cache_read"] + tot["sub_cache_read"]

    # ---- M5 / M5b
    sem_coleta = {r["sessao_id"] for r in S if r.get("modo_coleta") == "sem_coleta"}
    INT_SC = [i for i in INT if i["sessao_id"] in sem_coleta]  # D-037/D-094: reenviadas e coletadas depois
    INT = [i for i in INT if i["sessao_id"] not in sem_coleta]  # leitura principal: conta uma vez
    m5_tipo = Counter(i["tipo"] for i in INT)
    m5_fase = Counter(i["fase"] for i in INT)
    m5_causa = Counter(i["causa"] or "(sem)" for i in INT)
    m5_sev = Counter(i["severidade"] or "(sem)" for i in INT)
    m5b_fase = Counter(p["fase"] for p in PRO)
    liv = Counter(l["categoria"] for l in LIV)
    m5_ampla = len(INT) + len(INT_SC) + liv["interrupcao"] + liv["retomada"] + liv["outra"]

    ciclo_row = {
        "ciclo": ciclo,
        "M1_instalacao_h": h(m1_inst), "M1_sessao_h": h(m1_sessao), "M1_total_h": h(m1_inst + m1_sessao), "M1_calendario_h": h(m1_cal),
        "M2_total_h": h(m2_total),
        "M2_unidades_h": h(sum(f(r, "duracao_s") for r in unid_rows)),
        "M2_plan_h": h(sum(f(r, "duracao_s") for r in plan_ate)),
        "M2_retro_h": h(sum(f(r, "duracao_s") for r in retro)),
        "M2_espec_h": h(fase_s["ESPEC"]), "M2_impl_h": h(fase_s["IMPL"]), "M2_valid_h": h(fase_s["VALID"]),
        "M2_setup_fase_h": h(fase_s["SETUP"]),
        "M2_pausa_h": h(sum(f(r, "pausa_s") for r in desenv)),
        "M2_bruto_h": h(sum(f(r, "duracao_bruta_s") for r in desenv)),
        "n_sessoes": len(desenv),
        **{f"M3_{k}": int(v) for k, v in tot.items()},
        "M3_custo_usd": round(custo, 2),
        **{f"M3_{k}_{fa.lower()}": int(tok_fase[fa][k]) for fa in FASES for k in cat},
        "M3_razao_in_out": round(in_total / out_total, 2) if out_total else "",
        "M3_frac_cache_read": round(cr_total / in_total, 4) if in_total else "",
        "M5_total": len(INT), "M5b_total": len(PRO), "M5_sens_sem_coleta": len(INT_SC),
        **{f"M5_tipo_{t}": m5_tipo[t] for t in TIPOS},
        **{f"M5_fase_{fa.lower()}": m5_fase[fa] for fa in FASES},
        **{f"M5_causa_{c}": m5_causa[c] for c in CAUSAS},
        **{f"M5_sev_{s}": m5_sev[s] for s in ("S1", "S2", "S3")},
        **{f"M5b_fase_{fa.lower()}": m5b_fase[fa] for fa in FASES},
        "M5_sens_interrupcao": liv["interrupcao"], "M5_sens_retomada": liv["retomada"], "M5_sens_outra": liv["outra"],
        "M5_sens_neutra": liv["neutra"], "M5_sens_painel_sem_prefixo": liv["painel_sem_prefixo"],
        "M5_leitura_ampla": m5_ampla,
    }

    # ---- por unidade
    ordem = sorted((u for u in UNIDADES if any(k.startswith(u.lower() + "-") for k in tag_data)),
                   key=lambda u: next(v for k, v in tag_data.items() if k.startswith(u.lower() + "-")))
    anterior = tag_data.get("plan-done") or tag_data["setup-done"]
    rf_rows = []
    for u in ordem:
        tg = next(k for k in tag_data if k.startswith(u.lower() + "-"))
        rows = [r for r in desenv if r["id_rf"] == u]
        seg_u = [sg for sg in SEG if sg["id_rf"] == u]
        ativo = sum(f(r, "duracao_s") for r in rows)
        teto = TETO_H.get(u, TETO_PADRAO_H)
        ints = [i for i in INT if i["id_rf"] == u]
        ints_sc = [i for i in INT_SC if i["id_rf"] == u]
        pros = [p for p in PRO if p["id_rf"] == u]
        lv = Counter(l["categoria"] for l in LIV if l["id_rf"] == u)
        fs = Counter()
        for sg in seg_u:
            fs[sg["fase"]] += f(sg, "duracao_ativa_s")
        rf_rows.append({
            "ciclo": ciclo, "id_rf": u, "tag": f"{ciclo.upper() if False else 'ciclo'}{ciclo.upper()}/{tg}",
            "commit": tag_commit[tg], "data_tag": tag_data[tg].isoformat(),
            "fechamento": tag_tipo[tg], "timebox_censurado": tag_tipo[tg] == "incompleto",
            "acima_do_teto": h(ativo) > teto, "teto_h": teto,
            "n_sessoes": len(rows),
            "M2_sessao_h": h(ativo), "M2_bruto_h": h(sum(f(r, "duracao_bruta_s") for r in rows)),
            "M2_pausa_h": h(sum(f(r, "pausa_s") for r in rows)),
            "M2_calendario_h": h((tag_data[tg] - anterior).total_seconds()),
            "M2_espec_h": h(fs["ESPEC"]), "M2_impl_h": h(fs["IMPL"]), "M2_valid_h": h(fs["VALID"]),
            **{f"M3_{k}": int(sum(f(r, k) for r in rows)) for k in cat + sub},
            "M3_custo_usd": round(sum(f(r, "custo_usd") for r in rows), 2),
            "M5": len(ints), "M5b": len(pros), "M5_sens_sem_coleta": len(ints_sc),
            **{f"M5_tipo_{t}": sum(1 for i in ints if i["tipo"] == t) for t in TIPOS},
            "M5_sens_interrupcao": lv["interrupcao"], "M5_sens_retomada": lv["retomada"], "M5_sens_outra": lv["outra"],
            "M5_leitura_ampla": len(ints) + len(ints_sc) + lv["interrupcao"] + lv["retomada"] + lv["outra"],
        })
        anterior = max(anterior, tag_data[tg])
    return ciclo_row, rf_rows


def write(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--saida", type=Path, default=ROOT / "dados" / "processo")
    a = ap.parse_args(argv)
    ciclos, rfs = [], []
    for c, d in (("a", "cicloA"), ("b", "cicloB")):
        cr, rr = agregar(c, ROOT / "dados" / d)
        ciclos.append(cr)
        rfs += rr
    write(a.saida / "ciclo.csv", ciclos)
    write(a.saida / "rf.csv", rfs)
    print(f"gravado: {a.saida / 'ciclo.csv'} ({len(ciclos)} linhas) e {a.saida / 'rf.csv'} ({len(rfs)} linhas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
