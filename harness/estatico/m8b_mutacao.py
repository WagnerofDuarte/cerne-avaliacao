"""M8b — mutation score do dominio (`lib/**/domain/**`), so para a tag `final`.

Modulo proprio (decisao registrada nas notas): operadores simples e deterministicos aplicados
em uma COPIA temporaria da tag; cada mutante roda a suite do agente (`flutter test`). Mutante
MORTO = a suite passa a ter alguma falha que nao tinha na linha de base (conjunto de ids que
falham cresce) ou estoura o tempo; SOBREVIVENTE = o conjunto de falhas nao muda; ERRO DE
COMPILACAO fica fora do denominador. Score = mortos / (mortos + sobreviventes).
Linha de base com testes falhando e aceita (compara-se com o conjunto de falhas da linha de base).

Operadores (so em codigo, nunca em comentario/string/import): == <-> !=, <= -> <, >= -> >,
< -> <=, > -> >= (com espacos ao redor, para nao tocar genericos nem `=>`), && <-> ||,
` + ` <-> ` - `, true <-> false.

Custo: 1 execucao da suite por mutante. Decisao de ferramenta: `mutation_test` (pub.dev) nao foi
adotado — dependencia externa nao travada e comportamento nao deterministico nao avaliado.
"""
from __future__ import annotations

import argparse
import re
import subprocess

from .common import (dart_files, dump, flutter_bin, flutter_env, line_of, preparar_dependencias, mask_dart, parse_test_json, read, rel,
                     tag_copy)

OPS = [
    (re.compile(r"(?<=\s)==(?=\s)"), "!="), (re.compile(r"(?<=\s)!=(?=\s)"), "=="),
    (re.compile(r"(?<=\s)<=(?=\s)"), "<"), (re.compile(r"(?<=\s)>=(?=\s)"), ">"),
    (re.compile(r"(?<=\s)<(?=\s)"), "<="), (re.compile(r"(?<=\s)>(?=\s)"), ">="),
    (re.compile(r"&&"), "||"), (re.compile(r"\|\|"), "&&"),
    (re.compile(r"(?<=\s)\+(?=\s)"), "-"), (re.compile(r"(?<=\s)-(?=\s)"), "+"),
    (re.compile(r"\btrue\b"), "false"), (re.compile(r"\bfalse\b"), "true"),
]


def enumerar(src):
    """[(posicao, de, para, linha)] ordenados por posicao."""
    code = mask_dart(src, strings=True)
    skip = set()
    for m in re.finditer(r"^[ \t]*(?:import|export|part)\b[^\n]*", code, re.M):
        skip.update(range(m.start(), m.end()))
    out = []
    for rx, para in OPS:
        for m in rx.finditer(code):
            if m.start() in skip:
                continue
            out.append((m.start(), m.group(), para, line_of(code, m.start())))
    return sorted(out)


def _rodar(root, timeout):
    try:
        p = subprocess.run([flutter_bin(), "test", "--reporter", "json", "--no-pub"], cwd=root, capture_output=True,
                           text=True, env=flutter_env(), timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, {}
    return p.returncode, parse_test_json(p.stdout, root)


def _falhas(res):
    return {t for t, r in res.items() if r in ("failure", "error")}


def medir(root, timeout=180, max_mutantes=None, filtro_arquivo=None, amostra=None, semente=20261108):
    preparar_dependencias(root, flutter_env(), 600)
    rc, base = _rodar(root, 600)
    if not base:
        raise RuntimeError("linha de base sem resultados de teste")
    base_f = _falhas(base)
    mutantes = []
    for f in dart_files(root):
        r = rel(root, f)
        if "/domain/" not in r or (filtro_arquivo and filtro_arquivo not in r):
            continue
        src = read(f)
        for pos, de, para, linha in enumerar(src):
            mutantes.append((r, f, src, pos, de, para, linha))
    if max_mutantes:
        mutantes = mutantes[:max_mutantes]
    total_enumerados = len(mutantes)
    if amostra and len(mutantes) > amostra:   # D-104: amostra deterministica (semente fixa, ordem original preservada)
        import random
        idx = sorted(random.Random(semente).sample(range(len(mutantes)), amostra))
        mutantes = [mutantes[i] for i in idx]
    out = []
    for r, f, src, pos, de, para, linha in mutantes:
        f.write_text(src[:pos] + para + src[pos + len(de):])
        try:
            rc, res = _rodar(root, timeout)
        finally:
            f.write_text(src)
        if rc is None:
            estado = "morto_timeout"
        elif not res:
            estado = "erro_compilacao"
        else:
            estado = "morto" if (_falhas(res) - base_f) else "sobrevivente"
        out.append({"arquivo": r, "linha": linha, "de": de, "para": para, "estado": estado})
    mortos = sum(1 for m in out if m["estado"].startswith("morto"))
    viv = sum(1 for m in out if m["estado"] == "sobrevivente")
    return {"M8b_mutation": round(mortos / (mortos + viv), 6) if (mortos + viv) else None, "mutantes_enumerados": total_enumerados,
            "amostra": amostra, "semente": semente if amostra else None, "mortos": mortos,
            "sobreviventes": viv, "erros_compilacao": sum(1 for m in out if m["estado"] == "erro_compilacao"),
            "falhas_linha_de_base": sorted(base_f), "mutantes": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--max-mutantes", type=int)
    ap.add_argument("--amostra", type=int, help="D-104: tamanho da amostra deterministica de mutantes")
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(medir(root, a.timeout, a.max_mutantes, amostra=a.amostra))


if __name__ == "__main__":
    main()
