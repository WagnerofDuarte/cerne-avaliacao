#!/usr/bin/env python3
"""M9 estatico (D-102): compara `lib/core/design_tokens.dart` da tag `final` com `holdout/tokens-prototipo.json`.
Por token do prototipo: cor = valor hexadecimal igual (RGB, ignorando o canal alfa) em alguma constante do arquivo;
familia = nome presente no arquivo; tamanho de fonte = numero presente como `fontSize`/constante de tamanho.
Nao mede pixels, nao mede uso nas telas (isso fica com a M9 de hardcodes) e nao mede espacamento (D-102).
Uso: python3 scripts/m9_tokens_estatico.py > dados/produto/m9_tokens.json
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS = {"a": ("/home/user/cerne-ciclo-a", "cicloA/final"), "b": ("/home/user/cerne-ciclo-b", "cicloB/final")}
proto = json.loads((ROOT / "holdout" / "tokens-prototipo.json").read_text())
res = {}
for c, (repo, tag) in REPOS.items():
    src = subprocess.run(["git", "-C", repo, "show", f"{tag}:lib/core/design_tokens.dart"], capture_output=True, text=True, check=True).stdout
    hexes = {m.group(1).upper() for m in re.finditer(r"0x[0-9A-Fa-f]{2}([0-9A-Fa-f]{6})", src)}
    cores = {k: v.lstrip("#").upper() in hexes for k, v in proto["cores"].items()}
    fam = {f: (f.lower() in src.lower()) for f in proto["fontFamilies"]}
    nums = {float(m) for m in re.findall(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])", src)}
    tam = {str(s): float(s) in nums for s in proto["fontSizes"]}
    res[c] = {"cor_primaria_igual": cores["colorPrimary"], "cores_iguais": sum(cores.values()), "cores_total": len(cores),
              "cores_ausentes": [k for k, v in cores.items() if not v],
              "familias_presentes": sum(fam.values()), "familias_total": len(fam), "familias_ausentes": [k for k, v in fam.items() if not v],
              "tamanhos_presentes": sum(tam.values()), "tamanhos_total": len(tam), "tamanhos_ausentes": [k for k, v in tam.items() if not v]}
json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
