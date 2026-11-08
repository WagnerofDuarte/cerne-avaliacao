#!/usr/bin/env python3
"""Orquestrador da Parte IV (produto, parte estatica) — D-100/D-101/D-102.

Roda, por ciclo, os modulos congelados de `harness/estatico/` sobre as tags dos repositorios dos ciclos:
  por unidade (tag de cada unidade): M7 (+ RF07/RF10), M9 (hardcodes), M10 (assinaturas), M12, M6-D, M13 (suite do agente);
  na tag `final`: M8 (cobertura), M8b (mutacao, teto de tempo), M15, M14 (selecao + checks estaticos).
Nada e gravado dentro de repositorio de app: copias temporarias por `git archive`. Saida em `--saida` (JSON por item).

Uso: python3 -m harness.produto.rodar --ciclo a|b|cal --etapa unidades|final|m8|m8b [--tags f000-done,...] --saida dados/produto
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from harness.estatico import (m6_aderencia, m7_camadas, m8_cobertura, m8b_mutacao, m9_hardcodes, m10_either,
                              m12_complexidade, m13_regressao, m14_decisoes, m15_consistencia)
from harness.estatico.common import run_flutter_tests_json, show, tag_copy

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA = RAIZ / "entrada" / "backend"
CONTRATO = (ENTRADA / "api" / "openapi.yaml", ENTRADA / "error-taxonomy.md", ENTRADA / "README.md")

UNIDADES_A = [("F000", "f000-done", "specs/001-foundation"), ("RF03", "rf03-done", "specs/002-biometric-auth-vault"),
              ("RF01", "rf01-done", "specs/003-multimodal-capture"), ("RF02", "rf02-done", "specs/004-stt-ocr-processing"),
              ("RF07", "rf07-done", "specs/005-multi-source-timeline"), ("RF06", "rf06-done", "specs/006-semantic-search-filter"),
              ("RF04", "rf04-incompleto", "specs/007-chat-memory-rag"), ("RF10", "rf10-done", "specs/008-chat-message-bookmark"),
              ("RF08", "rf08-done", "specs/009-chat-proactive-insight"), ("RF05", "rf05-done", "specs/010-personal-summary-export"),
              ("RF09", "rf09-done", "specs/011-settings-dashboard")]
UNIDADES_B = [("F000", "f000-done", None), ("RF03", "rf03-incompleto", None), ("RF01", "rf01-done", None), ("RF02", "rf02-done", None),
              ("RF07", "rf07-done", None), ("RF06", "rf06-done", None), ("RF04", "rf04-done", None), ("RF10", "rf10-done", None),
              ("RF08", "rf08-done", None), ("RF05", "rf05-done", None), ("RF09", "rf09-done", None)]

CAL_UNIDADES = [("RF01", "v1", "specs/001-entries"), ("RF02", "v2", "specs/002-chat")]

CICLOS = {
    "cal": {"repo": "/tmp/cal", "pref": "", "base": "v1", "unidades": CAL_UNIDADES, "metodologia": "speckit",
            "constitution": "", "plan_f000": "", "ref_tag": "v1", "ref_feature": "entries", "chat": "chat", "entries": "entries"},
    "a": {"repo": "/home/user/cerne-ciclo-a", "pref": "cicloA", "base": "setup-done", "unidades": UNIDADES_A, "metodologia": "speckit",
          "constitution": ".specify/memory/constitution.md", "plan_f000": "specs/001-foundation/plan.md",
          "ref_tag": "rf01-done", "ref_feature": "capture", "chat": "chat", "entries": "entries"},
    "b": {"repo": "/home/user/cerne-ciclo-b", "pref": "cicloB", "base": "plan-done", "unidades": UNIDADES_B, "metodologia": "bmad",
          "constitution": "_bmad-output/planning-artifacts/architecture/architecture-cerne-ciclo-b-2026-10-26/ARCHITECTURE-SPINE.md",
          "plan_f000": "_bmad-output/planning-artifacts/architecture/architecture-cerne-ciclo-b-2026-10-26/ARCHITECTURE-SPINE.md",
          "ref_tag": "rf01-done", "ref_feature": "capture", "chat": "chat", "entries": "entries",
          "mapa": RAIZ / "dados" / "cicloB" / "mapa-stories.csv"},
}


def tag_de(c, t):
    if c["pref"] == "" and t == "final":
        return "v2"
    return f"{c['pref']}/{t}" if c["pref"] else t


def docs_b(c, unidade, tag):
    """Ciclo B (D-105): o 'plano' da unidade sao as stories dela, escolhidas pelo mapa-stories.csv, lidas na tag da unidade."""
    with open(c["mapa"], newline="", encoding="utf-8") as f:
        ids = [r["story_id"] for r in csv.DictReader(f) if r["unidade"] == unidade]
    textos = {i: show(c["repo"], tag, f"_bmad-output/implementation-artifacts/spec-{i}.md") for i in ids}
    textos = {k: v for k, v in textos.items() if v}
    return textos


def arquivos_b(c, unidade, tag):
    return {f"_bmad-output/implementation-artifacts/spec-{k}.md": v for k, v in docs_b(c, unidade, tag).items()}


def m6_unidade(c, unidade, tag, prev, pasta, contrato):
    if c["metodologia"] == "speckit":
        return m6_aderencia.analisar(c["repo"], prev, tag, pasta, contrato)
    stories = docs_b(c, unidade, tag)
    if not stories:
        return {"sem_stories": True}
    txt = "\n\n".join(stories.values())
    return m6_aderencia.analisar(c["repo"], prev, tag, "", contrato, docs={"spec.md": "", "plan.md": txt, "tasks.md": txt})


def estaticos_da_tag(c, unidade, tag, root):
    r7 = m7_camadas.analisar(root, c["chat"], c["entries"])
    r9 = m9_hardcodes.analisar(root)
    r10 = m10_either.analisar(root)
    r12 = m12_complexidade.rodar(root)
    return {"M7": r7["M7_total"], "M7_detalhe": r7["M7"], "RF07_bloc_importa_bloc": len(r7["rf07_bloc_importa_bloc"]),
            "RF10_chat_importa_entradas": len(r10_safe(r7)), "M9_hardcodes": r9["M9_hardcodes"],
            "M10_assinaturas": r10["M10_assinaturas"], "M12_media": r12["M12_media"], "M12_acima": r12["M12_acima"],
            "M12_metodos": r12["metodos"]}


def r10_safe(r7):
    return r7["rf10_chat_importa_entradas"]


def unidade_tag(ciclo, unidade_idx, saida, contrato, com_testes=True, timeout=900):
    c = CICLOS[ciclo]
    uid, tg, pasta = c["unidades"][unidade_idx]
    tag = tag_de(c, tg)
    prev = tag_de(c, c["base"] if unidade_idx == 0 else c["unidades"][unidade_idx - 1][1])
    t0 = time.time()
    saida_f = Path(saida) / f"{ciclo}-{uid}.json"
    res = {"ciclo": ciclo, "id_rf": uid, "tag": tag, "prev": prev}
    try:
        with tag_copy(c["repo"], tag) as root:
            res.update(estaticos_da_tag(c, uid, tag, root))
            if com_testes:
                cod, testes = run_flutter_tests_json(root, timeout=timeout)
                res["testes_codigo_saida"] = cod
                res["testes_total"] = len(testes)
                res["testes_aprovados"] = sum(1 for v in testes.values() if v == "success")
                (Path(saida) / "testes").mkdir(parents=True, exist_ok=True)
                (Path(saida) / "testes" / f"{ciclo}-{uid}.json").write_text(json.dumps(testes, ensure_ascii=False, sort_keys=True))
        contr = m6_aderencia.carregar_contrato(*CONTRATO) if contrato is None else contrato
        m6 = m6_unidade(c, uid, tag, prev, pasta, contr)
        res["M6"] = m6
    except Exception as e:  # noqa: BLE001
        res["erro"] = f"{type(e).__name__}: {e}"[:500]
    res["segundos"] = round(time.time() - t0, 1)
    saida_f.write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    return res


def calcular_m13(ciclo, saida):
    """M13 entre tags de unidade consecutivas, a partir dos testes ja gravados."""
    c = CICLOS[ciclo]
    out, ant = [], None
    for uid, tg, _ in c["unidades"]:
        f = Path(saida) / "testes" / f"{ciclo}-{uid}.json"
        if not f.exists():
            out.append({"id_rf": uid, "M13": None, "nota": "sem testes gravados"})
            continue
        atual = json.loads(f.read_text())
        if ant is None:
            out.append({"id_rf": uid, "M13": None, "nota": "primeira unidade"})
        else:
            r = m13_regressao.comparar(ant[1], atual)
            out.append({"id_rf": uid, "anterior": ant[0], "M13": r["M13"], "M13_sem_apagados": r["M13_sem_apagados"], "M13_apagados": r["M13_apagados"],
                        "M13_seguranca": r["M13_seguranca"], "aprovados_anterior": r["aprovados_anterior"], "regressoes": r["regressoes"], "apagados": r["apagados"]})
        ant = (uid, atual)
    (Path(saida) / f"{ciclo}-m13.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return out


def final(ciclo, saida):
    c = CICLOS[ciclo]
    repo, tag = c["repo"], tag_de(c, "final")
    res = {"ciclo": ciclo, "tag": tag}
    with tag_copy(repo, tag) as r2, tag_copy(repo, tag_de(c, c["ref_tag"])) as r1:
        res["M15"] = m15_consistencia.analisar(r1, r2, c["ref_feature"])
        res["M14_selecao"] = m14_decisoes.analisar(r2, Path(r2) / c["constitution"], Path(r2) / c["plan_f000"])
    (Path(saida) / f"{ciclo}-final.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    return res


def m8(ciclo, saida):
    c = CICLOS[ciclo]
    with tag_copy(c["repo"], tag_de(c, "final")) as root:
        r = m8_cobertura.medir(root)
    (Path(saida) / f"{ciclo}-m8.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=str))
    return r


def m8b(ciclo, saida, amostra=None, timeout=300):
    c = CICLOS[ciclo]
    with tag_copy(c["repo"], tag_de(c, "final")) as root:
        r = m8b_mutacao.medir(root, timeout=timeout, amostra=amostra)
    (Path(saida) / f"{ciclo}-m8b.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=str))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ciclo", required=True, choices=sorted(CICLOS))
    ap.add_argument("--etapa", required=True, choices=["unidades", "m13", "final", "m8", "m8b"])
    ap.add_argument("--saida", required=True)
    ap.add_argument("--so", help="ids de unidade separados por virgula (default: todas)")
    ap.add_argument("--sem-testes", action="store_true")
    ap.add_argument("--paralelo", type=int, default=2)
    ap.add_argument("--amostra", type=int, help="M8b: amostra deterministica de mutantes (D-104)")
    a = ap.parse_args()
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    if a.etapa == "unidades":
        c = CICLOS[a.ciclo]
        alvo = [i for i, (u, _, _) in enumerate(c["unidades"]) if not a.so or u in a.so.split(",")]
        contrato = m6_aderencia.carregar_contrato(*CONTRATO)
        with ThreadPoolExecutor(a.paralelo) as ex:
            for r in ex.map(lambda i: unidade_tag(a.ciclo, i, saida, contrato, not a.sem_testes), alvo):
                print(r["id_rf"], r.get("erro", "ok"), r["segundos"], flush=True)
    elif a.etapa == "m13":
        calcular_m13(a.ciclo, saida)
    elif a.etapa == "final":
        final(a.ciclo, saida)
    elif a.etapa == "m8":
        m8(a.ciclo, saida)
    elif a.etapa == "m8b":
        m8b(a.ciclo, saida, a.amostra)


if __name__ == "__main__":
    main()
