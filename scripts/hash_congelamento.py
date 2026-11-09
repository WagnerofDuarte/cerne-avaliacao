#!/usr/bin/env python3
"""Hash combinado de diretorio/arquivo, no metodo de docs/hashes-congelamento.md:
lista `sha256<2 espacos>caminho_relativo` por arquivo, ordenada por caminho (bytes), uma linha por arquivo,
\\n no fim; o hash combinado e o SHA-256 dessa listagem. Ignora __pycache__, .pyc, .dart_tool, build/, .gitkeep.
Uso: python3 scripts/hash_congelamento.py <caminho>... [--lista]"""
import hashlib
import sys
from pathlib import Path

IGN = ("__pycache__", ".dart_tool", ".pytest_cache", ".gitkeep")


def arquivos(base: Path):
    if base.is_file():
        return [(base.name, base)]
    out = []
    for p in base.rglob("*"):
        if p.is_file() and not any(i in p.parts for i in IGN) and p.suffix != ".pyc" and "build" not in p.relative_to(base).parts[:1]:
            out.append((p.relative_to(base).as_posix(), p))
    return sorted(out, key=lambda x: x[0].encode())


def combinado(base: Path):
    linhas = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {rel}" for rel, p in arquivos(base)]
    return hashlib.sha256(("\n".join(linhas) + "\n").encode()).hexdigest(), linhas


if __name__ == "__main__":
    mostrar = "--lista" in sys.argv
    for a in [x for x in sys.argv[1:] if not x.startswith("--")]:
        h, linhas = combinado(Path(a))
        print(f"{h}  {a}  ({len(linhas)} arquivo(s))")
        if mostrar:
            print("\n".join("    " + l for l in linhas))
