"""M7 — violacoes de camada (RNF06) e regras estruturais do RF07 e do RF10.

RNF06 (conta na M7): arquivo em `domain/` que importa `package:flutter/...` ou qualquer
arquivo em `data/` (de qualquer feature). Regras estruturais (contam SO na M11, emitidas
a parte): RF07 'nenhum BLoC importa outro BLoC'; RF10 'o chat nao importa o repositorio
de entradas'. Configuracao do harness, nao o analysis_options do app.

Interpretacoes registradas (ver docs/trilha-harness-notas.md):
- 'package:flutter' = exatamente `package:flutter/` (SDK); `flutter_bloc` etc. nao contam.
- BLoC = arquivo `*_bloc.dart` ou `*_cubit.dart`; viola se importa OUTRO arquivo desse tipo.
- RF10: arquivo da feature de chat que importa, na feature de entradas, qualquer arquivo em
  `data/` ou com `repository`/`datasource`/`data_source` no nome.

Uso: python3 -m harness.estatico.m7_camadas --repo <repo> --tag <tag> [--chat-feature chat] [--entries-feature entries]
"""
from __future__ import annotations

import argparse
import re
from pathlib import PurePosixPath

from .common import (app_name, dart_files, dump, imports_of, layer_of, read, rel,
                     resolve_import, tag_copy)

BLOC_RE = re.compile(r"_(bloc|cubit)\.dart$")
REPO_RE = re.compile(r"repositor|datasource|data_source")


def analisar(root, chat_feature="chat", entries_feature="entries"):
    app = app_name(root)
    m7, rf07, rf10 = [], [], []
    for f in dart_files(root):
        fr = rel(root, f)
        feat, layer = layer_of(fr)
        for linha, uri in imports_of(read(f)):
            kind, target = resolve_import(root, fr, uri, app)
            if layer == "domain":
                if kind == "ext" and uri.startswith("package:flutter/"):
                    m7.append({"arquivo": fr, "linha": linha, "regra": "dominio_importa_flutter", "import": uri})
                elif kind == "int" and layer_of(target)[1] == "data":
                    m7.append({"arquivo": fr, "linha": linha, "regra": "dominio_importa_data", "import": uri})
            if kind == "int":
                if BLOC_RE.search(fr) and BLOC_RE.search(target) and target != fr:
                    rf07.append({"arquivo": fr, "linha": linha, "import": uri})
                tfeat, tlayer = layer_of(target)
                if feat == chat_feature and tfeat == entries_feature and (
                        tlayer == "data" or REPO_RE.search(PurePosixPath(target).name)):
                    rf10.append({"arquivo": fr, "linha": linha, "import": uri})
    key = lambda v: (v["arquivo"], v["linha"])
    return {"M7": sorted(m7, key=key), "M7_total": len(m7),
            "rf07_bloc_importa_bloc": sorted(rf07, key=key), "rf10_chat_importa_entradas": sorted(rf10, key=key)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--chat-feature", default="chat")
    ap.add_argument("--entries-feature", default="entries")
    a = ap.parse_args()
    with tag_copy(a.repo, a.tag) as root:
        dump(analisar(root, a.chat_feature, a.entries_feature))


if __name__ == "__main__":
    main()
