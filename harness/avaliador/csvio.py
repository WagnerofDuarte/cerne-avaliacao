"""Esquema do C-002 (secao 8.2 do documento de metricas) e gravacao dos CSVs. Saida SEMPRE numa pasta de
calibracao (padrao calibracao/saida/); recusa gravar dentro de `dados/` ou de um repositorio de app."""
from __future__ import annotations

import csv
from pathlib import Path

RF = ["ciclo", "id_rf", "tag", "commit", "timebox_censurado", "M4", "M6_tasks", "M6_citados_nao_alterados", "M6_alterados_nao_citados",
      "M6_inexist_arq", "M6_inexist_pkg", "M6_inexist_backend", "M6_div_nao_doc", "M7", "M7_novas", "M8", "M9_hardcodes", "M10_assinaturas",
      "M11_aprovados", "M11_total", "M11", "M12_media", "M12_acima", "M13", "M13_sem_apagados", "M13_apagados", "M13_seguranca"]
ESTADOS = ["ciclo", "estado_id", "cor_ok", "tipografia_ok", "espacamento_ok", "score"]
VALIDACAO = ["metrica", "item_id", "classificacao_humana", "voto_avaliador", "sem_maioria"]
CICLO = (["ciclo", "M1_instalacao_h", "M1_sessao_h", "M1_total_h", "M1_calendario_h", "M2_total_h", "M2_plan_h", "M2_espec_h", "M2_impl_h", "M2_valid_h",
          "M3_tokens_total", "M3_tokens_espec", "M3_tokens_impl", "M3_tokens_valid", "M3_sub_tokens_total", "M3_sub_tokens_espec", "M3_sub_tokens_impl",
          "M3_sub_tokens_valid", "M3_custo_usd", "M3_razao_in_out", "M3_frac_cache_read", "M4_total", "M5_total", "M5b_total", "M8b_mutation",
          "M10_cenarios", "M14", "M15_divergencias", "M9_score_medio"])


def pasta_saida(p):
    p = Path(p).resolve()
    partes = {x.lower() for x in p.parts}
    if "dados" in partes:
        raise SystemExit(f"recusado: a saida de calibracao nao pode ficar em dados/ ({p})")
    p.mkdir(parents=True, exist_ok=True)
    return p


def ler(caminho):
    return list(csv.DictReader(open(caminho, encoding="utf-8"))) if Path(caminho).exists() else []


def gravar(caminho, colunas, linhas, chaves):
    """Substitui as linhas com a mesma chave e grava ordenado pela ordem de insercao."""
    atuais = ler(caminho)
    chave = lambda r: tuple(str(r.get(k, "")) for k in chaves)
    novas = {chave(r): r for r in linhas}
    resto = [r for r in atuais if chave(r) not in novas]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas, extrasaction="raise")
        w.writeheader()
        for r in resto + list(novas.values()):
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in colunas})
    return caminho
