"""M12 — orquestrador Python do CLI Dart `harness/m12/` (AST do package:analyzer).

Uso: python3 -m harness.estatico.m12_complexidade --repo <repo> --tag <tag>
Roda o CLI sobre uma COPIA temporaria da tag, restrito a `lib/**/domain/**`.
Requer `dart` no PATH e `dart pub get` feito em harness/m12 (uma vez).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from .common import dump, tag_copy

M12_DIR = Path(__file__).resolve().parents[1] / "m12"


def rodar(root, todos=False):
    dart = shutil.which("dart") or "dart"
    cmd = [dart, "run", "bin/m12.dart", "--root", str(root)] + (["--all"] if todos else [])
    p = subprocess.run(cmd, cwd=M12_DIR, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"m12: {p.stderr.strip() or p.stdout.strip()}")
    return json.loads(p.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(rodar(root))


if __name__ == "__main__":
    main()
