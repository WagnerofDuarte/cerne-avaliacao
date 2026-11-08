"""M8 — cobertura de linhas do dominio (`lib/**/domain/**`).

Roda `flutter test --coverage` numa COPIA temporaria da tag; o lcov fica numa pasta temporaria
FORA do repositorio e e descartado (ou gravado em `--saida-lcov`, que deve ser externa).

Armadilha tratada: o lcov so lista arquivos que algum teste importa; arquivo de dominio nunca
importado ficaria fora do denominador e inflaria a cobertura. O modulo injeta na copia um teste
`test/_harness_importa_dominio_test.dart` que importa todos os arquivos de `domain/` (nao
executa nada), de modo que arquivos sem teste entram com 0% de linhas cobertas.
Se algum teste da suite falhar, o lcov ainda e lido (a cobertura e do que executou) e o
resultado traz `testes_falharam=true`.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

from .common import app_name, dart_files, dump, flutter_bin, flutter_env, rel, tag_copy


def injetar_importa_dominio(root):
    app = app_name(root)
    imports = []
    for f in dart_files(root):
        r = rel(root, f)
        if "/domain/" in r:
            imports.append(f"import 'package:{app}/{r[len('lib/'):]}';")
    corpo = "// injetado pelo harness (M8): garante que todo arquivo de dominio entre no lcov\n" + "\n".join(
        f"{l.rstrip(';')} as _i{n};" for n, l in enumerate(imports)) + "\nvoid main() {}\n"
    t = Path(root) / "test" / "_harness_importa_dominio_test.dart"
    t.parent.mkdir(exist_ok=True)
    t.write_text(corpo)
    return len(imports)


def parse_lcov(text):
    """{arquivo: (linhas_executaveis, linhas_cobertas, [linhas_nao_cobertas])}"""
    res, cur, da = {}, None, {}
    for l in text.splitlines():
        if l.startswith("SF:"):
            cur, da = l[3:], {}
        elif l.startswith("DA:") and cur:
            n, h = l[3:].split(",")[:2]
            da[int(n)] = int(h)
        elif l == "end_of_record" and cur:
            res[cur] = (len(da), sum(1 for h in da.values() if h > 0), sorted(n for n, h in da.items() if h == 0))
            cur = None
    return res


def so_dominio(lcov):
    return {f: v for f, v in lcov.items() if "/domain/" in "/" + f.replace("\\", "/")}


def resumo(dom):
    lf = sum(v[0] for v in dom.values())
    lh = sum(v[1] for v in dom.values())
    return {"M8": round(lh / lf, 6) if lf else None, "linhas_executaveis": lf, "linhas_cobertas": lh,
            "por_arquivo": {f: {"executaveis": v[0], "cobertas": v[1], "nao_cobertas": v[2]} for f, v in sorted(dom.items())}}


def medir(root, saida_lcov=None, timeout=600):
    n = injetar_importa_dominio(root)
    env = flutter_env()
    subprocess.run([flutter_bin(), "pub", "get"], cwd=root, capture_output=True, text=True, env=env, timeout=timeout)
    p = subprocess.run([flutter_bin(), "test", "--coverage", "--no-pub"], cwd=root, capture_output=True, text=True, env=env, timeout=timeout)
    lcov = Path(root) / "coverage" / "lcov.info"
    if not lcov.exists():
        raise RuntimeError("lcov nao gerado: " + (p.stdout[-400:] + p.stderr[-400:]))
    if saida_lcov:
        shutil.copy(lcov, saida_lcov)
    r = resumo(so_dominio(parse_lcov(lcov.read_text())))
    r["testes_falharam"] = p.returncode != 0
    r["arquivos_de_dominio"] = n
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--saida-lcov", help="caminho EXTERNO ao repositorio (opcional)")
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(medir(root, a.saida_lcov))


if __name__ == "__main__":
    main()
