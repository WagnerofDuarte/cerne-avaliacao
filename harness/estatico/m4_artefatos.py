"""M4 — numero de artefatos por tipo (arquivos; codigo, testes e config nao contam).

Spec Kit: padroes de harness/regras.md §4. BMAD: os caminhos exatos NAO estao nos
documentos congelados (regras.md §4 diz 'confirmados na Fase 4'); o padrao abaixo e um
PALPITE configuravel (`--bmad-config arquivo.json`) e deve ser conferido contra a
instalacao real antes do GATE-H02 (pendencia registrada nas notas).
"""
from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path

from .common import dump, git, tag_copy, tree_files

SPECKIT = {
    "constitution": [".specify/memory/constitution.md"],
    "spec": ["specs/*/spec.md"],
    "plan": ["specs/*/plan.md"],
    "tasks": ["specs/*/tasks.md"],
    "research": ["specs/*/research.md"],
    "data_model": ["specs/*/data-model.md"],
    "quickstart": ["specs/*/quickstart.md"],
    "contracts": ["specs/*/contracts/*"],
    "checklists": ["specs/*/checklists/*"],
    # relatorios de analise/convergencia gravados em arquivo: tipo pelo nome
    "analysis": ["specs/*/*analy*", "specs/*/*converge*"],
}

BMAD_PADRAO = {  # PALPITE: saida padrao do BMAD v6 (_bmad-output/); confirmar na Fase 4
    "brief_pesquisa_prfaq_brainstorming": ["_bmad-output/planning-artifacts/*brief*", "_bmad-output/planning-artifacts/*research*",
                                           "_bmad-output/planning-artifacts/*prfaq*", "_bmad-output/planning-artifacts/*brainstorm*"],
    "prd": ["_bmad-output/planning-artifacts/*prd*"],
    "ux": ["_bmad-output/planning-artifacts/DESIGN.md", "_bmad-output/planning-artifacts/EXPERIENCE.md", "_bmad-output/planning-artifacts/*ux*"],
    "arquitetura": ["_bmad-output/planning-artifacts/*architecture*"],
    "epicos_stories": ["_bmad-output/planning-artifacts/*epic*", "_bmad-output/implementation-artifacts/*-*-*.md"],
    "status_review_retro": ["_bmad-output/implementation-artifacts/sprint-status.yaml", "_bmad-output/implementation-artifacts/*review*",
                            "_bmad-output/implementation-artifacts/*retro*"],
}


def contar(files, padroes):
    por_tipo, vistos = {}, set()
    for tipo, pats in padroes.items():
        achados = sorted(f for f in files if f not in vistos and any(fnmatch.fnmatchcase(f, p) for p in pats))
        vistos.update(achados)
        por_tipo[tipo] = achados
    return por_tipo


def analisar_lista(files, padroes):
    por_tipo = contar(files, padroes)
    res = {t: len(v) for t, v in por_tipo.items()}
    res["total"] = sum(res.values())
    return {"M4": res, "arquivos": por_tipo}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--metodologia", choices=["speckit", "bmad"], default="speckit")
    ap.add_argument("--bmad-config")
    a = ap.parse_args()
    pad = SPECKIT if a.metodologia == "speckit" else (json.loads(Path(a.bmad_config).read_text()) if a.bmad_config else BMAD_PADRAO)
    dump(analisar_lista(tree_files(a.repo, a.tag), pad))


if __name__ == "__main__":
    main()
