#!/usr/bin/env python3
"""Acrescenta a linha de instalação da metodologia a dados/<ciclo>/sessoes.csv
(C-017/M1) — tipo_sessao=instalacao, modo_coleta=script, campos de tokens
em 0 (Metricas_e_Skills_Ciclos.md §8). Chamado por instalar-metodologia,
nunca direto por um pesquisador."""
from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import coletar_sessao as cs  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ciclo", required=True, choices=["a", "b"])
    p.add_argument("--inicio", required=True)
    p.add_argument("--corte", required=True)
    p.add_argument("--duracao-s", required=True, type=int)
    p.add_argument("--dados-dir", default=None, type=Path)
    args = p.parse_args(argv)

    dados_dir = args.dados_dir or cs.dados_dir_default(args.ciclo)
    row = {k: "" for k in cs.CSV_FIELDS["sessoes.csv"]}
    row.update(
        {
            "ciclo": args.ciclo,
            "id_rf": "SETUP",
            "sessao_id": f"instalacao-{uuid.uuid4()}",
            "tipo_sessao": "instalacao",
            "modo_coleta": "script",
            "motivo_fim": "normal",
            "inicio": args.inicio,
            "corte": args.corte,
            "duracao_s": args.duracao_s,
            "duracao_bruta_s": args.duracao_s,
            "pausa_s": 0,
            "rate_limit_s": 0,
            "tokens_input": 0, "tokens_output": 0, "cache_read": 0, "cache_write": 0,
            "sub_tokens_input": 0, "sub_tokens_output": 0, "sub_cache_read": 0, "sub_cache_write": 0,
            "custo_usd": 0,
            "n_intervencoes": 0, "n_processo": 0, "n_avisos": 0, "n_compactacoes": 0,
            "n_msgs_contexto_ide": 0, "div_otel": "", "div_otel_alerta": False,
            "modelo": "", "versao_claude_code": "", "config_raciocinio": "",
        }
    )
    cs.append_csv(dados_dir / "sessoes.csv", cs.CSV_FIELDS["sessoes.csv"], row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
