"""M9 (parte D) — hardcodes de cor, fonte e espacamento fora de `design_tokens.dart`.

Escopo: `lib/**/*.dart` exceto qualquer arquivo chamado `design_tokens.dart`. Comentarios e
conteudo de strings sao ignorados. Uma ocorrencia = uma contagem (tipo, linha).

Regras (interpretacao registrada nas notas):
- cor: `Color(0x...)`, `Color.fromARGB/fromRGBO(`, `Colors.<nome>` (exceto `Colors.transparent`).
- tamanho de fonte: `fontSize: <numero>`.
- familia de fonte: `fontFamily: '<literal>'`.
- espacamento: `EdgeInsets.(all|symmetric|only|fromLTRB|fromSTEB)(...)` e `SizedBox(width|height: ...)`
  cujos argumentos tenham um literal numerico diferente de zero.
"""
from __future__ import annotations

import argparse
import re

from .common import dart_files, dump, line_of, mask_dart, read, rel, tag_copy

NUM = r"(?<![\w.$])(?:\d+\.\d+|\d+)(?![\w.])"
COLOR_RES = [
    re.compile(r"\bColor\s*\(\s*0[xX][0-9A-Fa-f]+"),
    re.compile(r"\bColor\s*\.\s*from(?:ARGB|RGBO)\s*\("),
    re.compile(r"\bColors\s*\.\s*(?!transparent\b)[A-Za-z_]\w*"),
]
FONT_SIZE = re.compile(r"\bfontSize\s*:\s*" + NUM)
FONT_FAMILY = re.compile(r"\bfontFamily\s*:\s*['\"]")
INSETS = re.compile(r"\bEdgeInsets\s*\.\s*(?:all|symmetric|only|fromLTRB|fromSTEB)\s*\(")
SIZEDBOX = re.compile(r"\bSizedBox\s*\(")


def _args(code, open_pos):
    depth, j = 0, open_pos
    while j < len(code):
        if code[j] == "(":
            depth += 1
        elif code[j] == ")":
            depth -= 1
            if depth == 0:
                return code[open_pos + 1:j]
        j += 1
    return code[open_pos + 1:]


def _nonzero_literal(text):
    return any(float(m.group()) != 0 for m in re.finditer(NUM, text))


def analisar_arquivo(src):
    code = mask_dart(src, strings=True)
    out = []
    for rx in COLOR_RES:
        for m in rx.finditer(code):
            out.append((m.start(), "cor"))
    for m in FONT_SIZE.finditer(code):
        out.append((m.start(), "tamanho_fonte"))
    for m in FONT_FAMILY.finditer(code):
        out.append((m.start(), "familia_fonte"))
    for m in INSETS.finditer(code):
        if _nonzero_literal(_args(code, m.end() - 1)):
            out.append((m.start(), "espacamento"))
    for m in SIZEDBOX.finditer(code):
        a = _args(code, m.end() - 1)
        for dim in re.finditer(r"\b(?:width|height)\s*:\s*(" + NUM + ")", a):
            if float(dim.group(1)) != 0:
                out.append((m.start(), "espacamento"))
                break
    return sorted((line_of(code, p), t) for p, t in out)


def analisar(root):
    res = []
    for f in dart_files(root):
        if f.name == "design_tokens.dart":
            continue
        for linha, tipo in analisar_arquivo(read(f)):
            res.append({"arquivo": rel(root, f), "linha": linha, "tipo": tipo})
    res.sort(key=lambda v: (v["arquivo"], v["linha"], v["tipo"]))
    return {"M9_hardcodes": len(res), "ocorrencias": res}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(analisar(root))


if __name__ == "__main__":
    main()
