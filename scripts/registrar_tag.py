#!/usr/bin/env python3
"""Acrescenta uma linha a dados/<ciclo>/tags.csv (C-017).

Usado por iniciar-ciclo, instalar-metodologia, concluir-rf e rf-incompleto
— nunca chamado direto por um pesquisador.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import coletar_sessao as cs  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ciclo", required=True, choices=["a", "b"])
    p.add_argument("--tag", required=True)
    p.add_argument("--tipo", required=True, choices=["baseline", "instalado", "setup-done", "plan-done", "done", "incompleto", "final"])
    p.add_argument("--id-rf", default="")
    p.add_argument("--commit", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--dados-dir", default=None, type=Path)
    args = p.parse_args(argv)

    dados_dir = args.dados_dir or cs.dados_dir_default(args.ciclo)
    cs.append_csv(
        dados_dir / "tags.csv",
        cs.CSV_FIELDS["tags.csv"],
        {
            "ciclo": args.ciclo,
            "tag": args.tag,
            "tipo": args.tipo,
            "id_rf": args.id_rf,
            "commit": args.commit,
            "data": args.data,
        },
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
