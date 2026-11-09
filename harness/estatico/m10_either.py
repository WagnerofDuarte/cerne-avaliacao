"""M10 (parte D) — assinaturas de repositorio fora do padrao `Either<Failure, T>`.

Repositorio = classe (abstrata ou concreta) cujo nome contem `Repository`, ou que
`extends`/`implements` um tipo cujo nome termina em `Repository`. Cada metodo publico
declarado nela (com ou sem corpo; sem construtores, getters, campos e membros `_privados`)
deve retornar `Either<..>`, `Future<Either<..>>`, `Stream<Either<..>>`, `FutureOr<Either<..>>`
ou `TaskEither<..>`.

Contagem: `M10_assinaturas` = numero de ASSINATURAS fora do padrao (interpretacao registrada
nas notas: a coluna chama-se 'assinaturas'; o texto de 5.2 diz 'repositorios fora do padrao',
por isso a saida traz tambem `repositorios_fora`).
"""
from __future__ import annotations

import argparse
import re

from .common import dart_files, dump, line_of, mask_dart, read, rel, tag_copy

CLASS_RE = re.compile(
    r"\b(?:abstract\s+|base\s+|final\s+|interface\s+|sealed\s+)*class\s+(\w+)(?:<[^{]*?>)?"
    r"((?:\s+(?:extends|implements|with)\s+[\w<>,\s.?]+?)*)\s*\{")
OK_RET = re.compile(r"^(?:(?:Future|Stream|FutureOr)\s*<\s*)?(?:Either|TaskEither)\s*<")


def _body(code, open_pos):
    depth = 0
    for j in range(open_pos, len(code)):
        if code[j] == "{":
            depth += 1
        elif code[j] == "}":
            depth -= 1
            if depth == 0:
                return open_pos + 1, j
    return open_pos + 1, len(code)


def _members(code, a, b):
    """Divide o corpo da classe em membros (texto, posicao) no nivel 1."""
    out, brace, paren, start, i = [], 0, 0, a, a
    while i < b:
        c = code[i]
        if c == "(":
            paren += 1
        elif c == ")":
            paren -= 1
        elif c == "{":
            brace += 1
        elif c == "}":
            brace -= 1
            if brace == 0 and paren == 0:
                out.append((code[start:i + 1], start))
                start = i + 1
        elif c == ";" and brace == 0 and paren == 0:
            out.append((code[start:i + 1], start))
            start = i + 1
        i += 1
    return out


def analisar_arquivo(src):
    code = mask_dart(src, strings=True)
    res = []
    for m in CLASS_RE.finditer(code):
        name, heritage = m.group(1), m.group(2) or ""
        supers = re.findall(r"\b(\w+)", re.sub(r"<[^>]*>", "", heritage))
        if not ("Repository" in name or any(s.endswith("Repository") for s in supers)):
            continue
        a, b = _body(code, m.end() - 1)
        for text, pos in _members(code, a, b):
            lead = len(text) - len(text.lstrip())
            t = text.strip()
            t = re.sub(r"^(?:@\w+(?:\([^)]*\))?\s*)+", "", t)
            p = t.find("(")
            if p < 0:
                continue  # campo ou getter
            head = t[:p].strip()
            head = re.sub(r"\b(static|external|abstract|covariant|final|const)\b", "", head).strip()
            mm = re.match(r"^(.*?)(\w+)$", head, re.S)
            if not mm:
                continue
            ret, mname = mm.group(1).strip(), mm.group(2)
            if mname.startswith("_") or mname == name or mname == "operator" or not ret:
                continue  # privado, construtor ou sem tipo de retorno
            ret = re.sub(r"\s+", "", ret)
            if OK_RET.match(ret):
                continue
            off = text.find(mname, lead)
            res.append({"classe": name, "metodo": mname, "retorno": ret, "linha": line_of(code, pos + off)})
    return res


def analisar(root):
    out = []
    for f in dart_files(root):
        for v in analisar_arquivo(read(f)):
            out.append({"arquivo": rel(root, f), **v})
    out.sort(key=lambda v: (v["arquivo"], v["linha"]))
    return {"M10_assinaturas": len(out), "repositorios_fora": sorted({v["classe"] for v in out}), "violacoes": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(analisar(root))


if __name__ == "__main__":
    main()
