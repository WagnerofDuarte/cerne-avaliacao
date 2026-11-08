#!/usr/bin/env python3
"""M4 — número de artefatos gerados (documentos de especificação), por tipo.

Regras: `harness/regras.md` §4 (conta ARQUIVOS; código, testes, configuração e
arquivos gerados não contam). Leitura: Ciclo A, na tag de cada unidade e na
`final`; Ciclo B, nas tags `plan-done` e `final`. Roda só com `git ls-tree`
sobre as tags (nenhum arquivo do repositório do ciclo é alterado).

Tipos do Ciclo A: constitution; spec, plan, tasks; pesquisa/modelo de dados/
quickstart; contratos; checklists; outros arquivos de `specs/<unidade>/`
(relatórios de análise e convergência, quando gravados).
Tipos do Ciclo B (diretório `_bmad-output/`): brainstorming, forge, pesquisa,
PRFAQ, brief, PRD, relatório de validação do PRD, UX, arquitetura, épicos e
contextos de épico, stories (arquivos `spec-*.md`), sprint-status,
retrospectivas e outros. Arquivos `.memlog.md` (registro interno de memória do
agente) ficam fora da leitura principal e entram só na leitura ampla.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNIDADE_A = {
    "001-foundation": "F000", "002-biometric-auth-vault": "RF03", "003-multimodal-capture": "RF01",
    "004-stt-ocr-processing": "RF02", "005-multi-source-timeline": "RF07", "006-semantic-search-filter": "RF06",
    "007-chat-memory-rag": "RF04", "008-chat-message-bookmark": "RF10", "009-chat-proactive-insight": "RF08",
    "010-personal-summary-export": "RF05", "011-settings-dashboard": "RF09",
}


def ls_tree(repo: Path, tag: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", tag], capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


def tipo_a(path: str) -> str | None:
    if path == ".specify/memory/constitution.md":
        return "constitution"
    m = re.match(r"specs/([^/]+)/(.+)$", path)
    if not m:
        return None
    base = m.group(2)
    if base in ("spec.md", "plan.md", "tasks.md"):
        return base[:-3]
    if base in ("research.md", "data-model.md", "quickstart.md"):
        return "pesquisa_modelo_quickstart"
    if base.startswith("contracts/"):
        return "contratos"
    if base.startswith("checklists/"):
        return "checklists"
    return "outros_specs"


def tipo_b(path: str) -> str | None:
    if not path.startswith("_bmad-output/"):
        return None
    nome = path.rsplit("/", 1)[-1]
    if nome == ".memlog.md":
        return "memlog"
    if path.startswith("_bmad-output/party-mode/"):
        return "memlog"
    if path.startswith("_bmad-output/brainstorming/"):
        return "brainstorming"
    if path.startswith("_bmad-output/forge/"):
        return "forge"
    if "/research/" in path:
        return "pesquisa"
    if "prfaq" in nome:
        return "prfaq"
    if "/briefs/" in path:
        return "brief"
    if "/prds/" in path:
        return "relatorio_validacao_prd" if "validation-report" in nome else "prd"
    if "/ux-designs/" in path:
        return "ux"
    if "/architecture/" in path:
        return "arquitetura"
    if nome == "epics.md" or re.match(r"epic-\d+-context\.md", nome):
        return "epicos"
    if re.match(r"spec-.*\.md", nome):
        return "stories"
    if nome == "sprint-status.yaml":
        return "sprint_status"
    if re.match(r"epic-\d+-retro-.*\.md", nome):
        return "retrospectivas"
    return "outros_implementacao"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-a", type=Path, default=Path("/home/user/cerne-ciclo-a"))
    ap.add_argument("--repo-b", type=Path, default=Path("/home/user/cerne-ciclo-b"))
    ap.add_argument("--saida", type=Path, default=ROOT / "dados" / "processo" / "m4.csv")
    a = ap.parse_args(argv)
    linhas = []

    def fetch(repo: Path, tag: str):
        subprocess.run(["git", "-C", str(repo), "fetch", "-q", "--depth=1", "origin", f"refs/tags/{tag}:refs/tags/{tag}"], capture_output=True)

    # Ciclo A: unidade a unidade (tag da unidade) e final
    tags_a = ["f000-done", "rf03-done", "rf01-done", "rf02-done", "rf07-done", "rf06-done", "rf04-incompleto", "rf10-done", "rf08-done", "rf05-done", "rf09-done", "final"]
    for t in tags_a:
        tag = f"cicloA/{t}"
        fetch(a.repo_a, tag)
        c = Counter()
        for p in ls_tree(a.repo_a, tag):
            ty = tipo_a(p)
            if ty:
                c[ty] += 1
        for ty, n in sorted(c.items()):
            linhas.append({"ciclo": "a", "tag": tag, "tipo": ty, "n": n})
        linhas.append({"ciclo": "a", "tag": tag, "tipo": "TOTAL", "n": sum(c.values())})
    # por diretório de unidade, na tag final
    for p in ls_tree(a.repo_a, "cicloA/final"):
        pass
    por_dir = Counter()
    for p in ls_tree(a.repo_a, "cicloA/final"):
        m = re.match(r"specs/([^/]+)/", p)
        if m:
            por_dir[m.group(1)] += 1
    for d, n in sorted(por_dir.items()):
        linhas.append({"ciclo": "a", "tag": "cicloA/final", "tipo": f"unidade:{UNIDADE_A.get(d, d)}", "n": n})

    # Ciclo B: plan-done e final
    for t in ("plan-done", "final"):
        tag = f"cicloB/{t}"
        fetch(a.repo_b, tag)
        c = Counter()
        for p in ls_tree(a.repo_b, tag):
            ty = tipo_b(p)
            if ty:
                c[ty] += 1
        for ty, n in sorted(c.items()):
            linhas.append({"ciclo": "b", "tag": tag, "tipo": ty, "n": n})
        linhas.append({"ciclo": "b", "tag": tag, "tipo": "TOTAL", "n": sum(v for k, v in c.items() if k != "memlog")})
        linhas.append({"ciclo": "b", "tag": tag, "tipo": "TOTAL_ampla_com_memlog", "n": sum(c.values())})
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    with a.saida.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ciclo", "tag", "tipo", "n"])
        w.writeheader()
        w.writerows(linhas)
    print(f"gravado {a.saida} ({len(linhas)} linhas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
