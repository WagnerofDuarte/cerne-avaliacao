"""M6 (parte D) — % de tarefas marcadas, cruzamento plano x diff e referencias inexistentes.

Interpretacoes registradas nas notas (o texto congelado nao fixa todos os detalhes):
- `M6_tasks`: `- [x]` / (`- [ ]` + `- [x]`) nos arquivos de tarefa informados (tasks.md no A;
  arquivos de story da unidade no B, escolhidos pelo `mapa-stories.csv`).
- citados x alterados: citados = `lib/...dart` em plan.md; alterados = arquivos `lib/**.dart`
  do diff da unidade (A, M ou D). citados_nao_alterados = citados - alterados (inclui os que
  nao existem); alterados_nao_citados = alterados - citados.
- referencias inexistentes: contadas por token DISTINTO por categoria na unidade. Fontes: spec.md,
  plan.md, tasks.md da unidade + linhas adicionadas no diff. (c2) e (c3) so em arquivos `data/`.
- contrato externo (openapi.yaml, error-taxonomy.md, backend/README.md) vem por argumento:
  `entrada/` nao existe neste checkout; o formato real NAO foi verificado (testado com versao
  sintetica em calibracao/backend-sintetico).
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

from .common import (diff_added_lines, diff_name_status, dump, git, read, show, tag_copy, tree_files)

FILE_RE = re.compile(r"lib/[A-Za-z0-9_/]+\.dart")
PKG_IMPORT_RE = re.compile(r"package:([a-z0-9_]+)/")
PKG_TICK_RE = re.compile(r"`([a-z0-9_]+)`")
ROUTE_RE = re.compile(r"(GET|POST|PATCH|DELETE)\s+(/[A-Za-z0-9_/{}:\-]+)")
FN_RE = re.compile(r"""['"]([a-z]+(?:-[a-z]+)+)['"]""")
FIELD_RES = [re.compile(r"""\[['"]([A-Za-z_][A-Za-z0-9_]*)['"]\]"""), re.compile(r"""['"]([A-Za-z_][A-Za-z0-9_]*)['"]\s*:""")]
CODE_RE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b")
EXCLUSOES_PADRAO = {"REPLAY_MISS"}  # lista de exclusao congelada junto com o codigo (regras.md §3)


def tasks_pct(textos):
    feitos = total = 0
    for t in textos:
        feitos += len(re.findall(r"^\s*[-*]\s*\[[xX]\]", t, re.M))
        total += len(re.findall(r"^\s*[-*]\s*\[[ xX]\]", t, re.M))
    return (feitos / total) if total else None


def norm_rota(p):
    return re.sub(r"(\{[^}/]*\}|:[A-Za-z_]\w*)", "{}", p.rstrip("/") or "/")


def carregar_contrato(openapi, taxonomia, readme):
    spec = yaml.safe_load(read(openapi))
    rotas = {norm_rota(p) for p in (spec.get("paths") or {})}
    campos = set()
    for sch in ((spec.get("components") or {}).get("schemas") or {}).values():
        campos.update((sch or {}).get("properties", {}) or {})
    codigos = set(CODE_RE.findall(read(taxonomia)))
    funcoes = set(re.findall(r"^\|\s*`([a-z]+(?:-[a-z]+)+)`", read(readme), re.M))
    return {"rotas": rotas, "campos": campos, "codigos": codigos, "funcoes": funcoes}


def analisar(repo, prev, tag, unidade, contrato, exclusoes=EXCLUSOES_PADRAO, docs=None):
    # `docs` (D-105): textos do plano da unidade quando nao ha spec.md/plan.md/tasks.md (Ciclo B: stories da unidade)
    docs = docs or {n: show(repo, tag, f"{unidade}/{n}") for n in ("spec.md", "plan.md", "tasks.md")}
    ns = diff_name_status(repo, prev, tag)
    added = diff_added_lines(repo, prev, tag)
    alterados = {p for s, p in ns if p.startswith("lib/") and p.endswith(".dart")}
    criados = {p for s, p in ns if s == "A"}
    citados = set(FILE_RE.findall(docs["plan.md"]))
    prev_tree = set(tree_files(repo, prev))
    pubspec = show(repo, tag, "pubspec.yaml")
    pkgs_ok = set(re.findall(r"^\s{2}([a-z0-9_]+):", pubspec, re.M)) | {"flutter", "flutter_test", "dart"}
    m = re.search(r"^name:\s*(\w+)", pubspec, re.M)
    if m:
        pkgs_ok.add(m.group(1))
    # textos varridos: documentos da unidade + linhas adicionadas no diff
    texto_diff = "\n".join(t for lst in added.values() for _, t in lst)
    texto_diff_data = "\n".join(t for p, lst in added.items() if "/data/" in p for _, t in lst)
    fontes = "\n".join(docs.values()) + "\n" + texto_diff

    inexist_arq = sorted(f for f in set(FILE_RE.findall(fontes)) if f not in prev_tree and f not in criados)
    pkgs = set(PKG_IMPORT_RE.findall(fontes))
    for frase in re.split(r"(?<=[.;\n])", "\n".join(docs.values())):
        if re.search(r"package|dependency|pub", frase, re.I):
            pkgs.update(PKG_TICK_RE.findall(frase))
    inexist_pkg = sorted(p for p in pkgs if p not in pkgs_ok)

    c1 = sorted({f"{mt} {p}" for mt, p in ROUTE_RE.findall(fontes) if norm_rota(p) not in contrato["rotas"]})
    c2 = sorted({f for f in FN_RE.findall(texto_diff_data) if f not in contrato["funcoes"]})
    campos = {x for rx in FIELD_RES for x in rx.findall(texto_diff_data)}
    c3 = sorted(c for c in campos if c not in contrato["campos"])
    c4 = sorted(c for c in set(CODE_RE.findall(fontes)) if c not in contrato["codigos"] and c not in exclusoes)
    return {
        "M6_tasks": tasks_pct([docs["tasks.md"]]),
        "M6_citados_nao_alterados": sorted(citados - alterados),
        "M6_alterados_nao_citados": sorted(alterados - citados),
        "M6_inexist_arq": inexist_arq,
        "M6_inexist_pkg": inexist_pkg,
        "M6_inexist_backend": {"c1": c1, "c2": c2, "c3": c3, "c4": c4},
        "contagens": {"citados_nao_alterados": len(citados - alterados), "alterados_nao_citados": len(alterados - citados),
                      "inexist_arq": len(inexist_arq), "inexist_pkg": len(inexist_pkg),
                      "inexist_backend": len(c1) + len(c2) + len(c3) + len(c4)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--prev-tag", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--unidade", required=True, help="pasta do plano da unidade, ex.: specs/003-captura")
    ap.add_argument("--openapi", required=True)
    ap.add_argument("--taxonomia", required=True)
    ap.add_argument("--readme-backend", required=True)
    a = ap.parse_args()
    dump(analisar(a.repo, a.prev_tag, a.tag, a.unidade, carregar_contrato(a.openapi, a.taxonomia, a.readme_backend)))


if __name__ == "__main__":
    main()
