#!/usr/bin/env python3
"""Gera `docs/resultados-processo.md` a partir de `dados/processo/*.csv` (D-097).
Cada número do texto é rastreável a uma linha de CSV (V-006)."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "dados" / "processo"
ciclo = {r["ciclo"]: r for r in csv.DictReader(open(P / "ciclo.csv", encoding="utf-8"))}
rf = list(csv.DictReader(open(P / "rf.csv", encoding="utf-8")))
m4 = list(csv.DictReader(open(P / "m4.csv", encoding="utf-8")))
A, B = ciclo["a"], ciclo["b"]


def g(r, k, nd=1):
    v = r[k]
    try:
        x = float(v)
    except ValueError:
        return v
    return f"{x:,.{nd}f}".replace(",", " ") if nd else f"{int(x):,}".replace(",", " ")


def m4v(c, tag, tipo):
    for r in m4:
        if r["ciclo"] == c and r["tag"] == tag and r["tipo"] == tipo:
            return r["n"]
    return ""


out = []
w = out.append
w("# Resultados de processo (M1 a M5) e M4 — Ciclo A (Spec Kit) × Ciclo B (BMAD)\n")
w("**Origem dos números:** `dados/processo/ciclo.csv`, `dados/processo/rf.csv` e `dados/processo/m4.csv`, gerados por `harness/h007/agregar_processo.py` e `harness/h007/contar_m4.py` a partir das tabelas re-derivadas dos transcritos brutos (`dados/<ciclo>/rederivado/`, H-007, D-096). **Recorte e ordem dos portões:** D-097 (Parte IV antecipada e reduzida por prazo, antes do `GATE-H02`). **Fora deste documento, por não terem sido avaliadas:** M6 (parte do avaliador), M7 a M15 e a validação do avaliador (ver D-097).\n")
w("**Como ler.** Tempo ativo (P5c): intervalos que terminam numa ação do agente contam inteiros; esperas pelo pesquisador contam até 30 min cada (o excedente vai para a pausa). Tokens e custo: transcrito principal mais subagentes; custo pela tabela congelada `harness/precos.md`. As unidades (F000 e RF01 a RF10) são as mesmas nos dois ciclos, mas a decomposição interna difere (Spec Kit: comandos por unidade; BMAD: stories, com um laço `bmad-build`, `bmad-code-review` e QA por story). Diferenças absolutas **não** são leitura de \"melhor\" ou \"pior\": ver as ameaças à validade.\n")
w("## 1. Resumo por ciclo\n")
w("| Métrica | Ciclo A (Spec Kit) | Ciclo B (BMAD) |\n|---|---:|---:|")
rows = [
    ("M1 instalação (h)", "M1_instalacao_h", 3), ("M1 sessões SETUP (h)", "M1_sessao_h", 2), ("M1 total (h)", "M1_total_h", 2),
    ("M1 calendário, instalação → `setup-done` (h)", "M1_calendario_h", 1),
    ("M2 tempo ativo total (h)", "M2_total_h", 1), ("M2 só das 11 unidades (h)", "M2_unidades_h", 1),
    ("M2 planejamento global `PLAN` (h)", "M2_plan_h", 1), ("M2 retrospectivas, `PLAN` depois de `plan-done` (h)", "M2_retro_h", 1),
    ("M2 fase ESPEC (h)", "M2_espec_h", 1), ("M2 fase IMPL (h)", "M2_impl_h", 1), ("M2 fase VALID (h)", "M2_valid_h", 1),
    ("Pausa fora do tempo ativo (h)", "M2_pausa_h", 1), ("Sessões medidas", "n_sessoes", 0),
    ("M3 tokens de entrada (agente principal)", "M3_tokens_input", 0), ("M3 tokens de saída (agente principal)", "M3_tokens_output", 0),
    ("M3 cache read (agente principal)", "M3_cache_read", 0), ("M3 cache write (agente principal)", "M3_cache_write", 0),
    ("M3 tokens de saída dos subagentes", "M3_sub_tokens_output", 0), ("M3 custo (USD)", "M3_custo_usd", 2),
    ("M3 razão entrada:saída (com cache)", "M3_razao_in_out", 1), ("M3 fração de cache read na entrada", "M3_frac_cache_read", 3),
    ("M5 intervenções (leitura principal)", "M5_total", 0), ("M5 intervenções, leitura ampla (sensibilidade)", "M5_leitura_ampla", 0),
    ("M5b respostas `PROCESSO:` (revisão exigida pelo processo)", "M5b_total", 0),
]
for nome, k, nd in rows:
    w(f"| {nome} | {g(A, k, nd)} | {g(B, k, nd)} |")
w(f"| M4 artefatos na tag `final` | {m4v('a', 'cicloA/final', 'TOTAL')} | {m4v('b', 'cicloB/final', 'TOTAL')} |")
w(f"| M4 artefatos em `plan-done` (só B) | — | {m4v('b', 'cicloB/plan-done', 'TOTAL')} |")
w("\n## 2. M5 por tipo, causa e fase (leitura principal)\n")
w("| | A | B |\n|---|---:|---:|")
for k, nome in [("M5_tipo_correção", "tipo `correção`"), ("M5_tipo_esclarecimento não solicitado", "tipo `esclarecimento não solicitado`"),
                ("M5_causa_prd", "causa `prd` (diferença contra o protótipo/pacote)"), ("M5_causa_chk", "causa `chk`"), ("M5_causa_inc", "causa `inc`"),
                ("M5_sev_S1", "severidade S1"), ("M5_sev_S2", "severidade S2"), ("M5_sev_S3", "severidade S3"),
                ("M5_fase_espec", "fase ESPEC"), ("M5_fase_impl", "fase IMPL"), ("M5_fase_valid", "fase VALID"),
                ("M5b_fase_espec", "M5b fase ESPEC"), ("M5b_fase_impl", "M5b fase IMPL"), ("M5b_fase_valid", "M5b fase VALID")]:
    w(f"| {nome} | {g(A, k, 0)} | {g(B, k, 0)} |")
w("\n**Sensibilidade da M5** (mensagens livres, sem prefixo, que a leitura principal não conta; `dados/<ciclo>/rederivado/mensagens_livres.csv`):\n")
w("| | A | B |\n|---|---:|---:|")
for k, nome in [("M5_sens_sem_coleta", "intervenções de sessões descartadas sem coleta (D-037, D-094)"), ("M5_sens_interrupcao", "interrupções por Esc"),
                ("M5_sens_retomada", "retomadas (`continue`, `ask again`, `Try again`)"), ("M5_sens_outra", "outras mensagens livres"),
                ("M5_sens_neutra", "mensagens neutras (`Yes`, `Yes, proceed.`; não contam)"), ("M5_sens_painel_sem_prefixo", "respostas de painel por clique, sem prefixo (não contam)")]:
    w(f"| {nome} | {g(A, k, 0)} | {g(B, k, 0)} |")
w("\n## 3. Por unidade\n")
w("Tempo ativo (h), tempo de calendário desde a tag anterior (h), custo (USD), intervenções (M5, leitura principal) e `PROCESSO:` (M5b). `>teto`: tempo ativo acima do teto de 8 h (12 h na F000); a unidade seguiu por decisão registrada (D-058, D-060, D-064, D-080, D-090). RF02 do B não teve sessões (nota B7).\n")
w("| Unid. | Ciclo | Fecho | Sessões | Ativo (h) | Calendário (h) | Custo (USD) | M5 | M5b | |\n|---|---|---|---:|---:|---:|---:|---:|---:|---|")
for u in ["F000", "RF03", "RF01", "RF02", "RF07", "RF06", "RF04", "RF10", "RF08", "RF05", "RF09"]:
    for c in ("a", "b"):
        r = next(x for x in rf if x["ciclo"] == c and x["id_rf"] == u)
        flag = ">teto" if r["acima_do_teto"] == "True" else ""
        w(f"| {u} | {c.upper()} | {r['fechamento']} | {r['n_sessoes']} | {float(r['M2_sessao_h']):.2f} | {float(r['M2_calendario_h']):.1f} | {float(r['M3_custo_usd']):.2f} | {r['M5']} | {r['M5b']} | {flag} |")
w("\n## 4. M4 por tipo (arquivos)\n")
tipos_a = ["constitution", "spec", "plan", "tasks", "pesquisa_modelo_quickstart", "contratos", "checklists", "outros_specs"]
w("**Ciclo A, tag `final`:**\n\n| Tipo | Arquivos |\n|---|---:|")
for t in tipos_a:
    w(f"| {t} | {m4v('a', 'cicloA/final', t) or 0} |")
w(f"| **Total** | **{m4v('a', 'cicloA/final', 'TOTAL')}** |")
tipos_b = ["brainstorming", "forge", "pesquisa", "prfaq", "brief", "prd", "relatorio_validacao_prd", "ux", "arquitetura", "epicos", "stories", "sprint_status", "retrospectivas", "outros_implementacao"]
w("\n**Ciclo B** (`_bmad-output/`; `.memlog.md` fora da leitura principal):\n\n| Tipo | `plan-done` | `final` |\n|---|---:|---:|")
for t in tipos_b:
    w(f"| {t} | {m4v('b', 'cicloB/plan-done', t) or 0} | {m4v('b', 'cicloB/final', t) or 0} |")
w(f"| **Total** | **{m4v('b', 'cicloB/plan-done', 'TOTAL')}** | **{m4v('b', 'cicloB/final', 'TOTAL')}** |")
w("\n## 5. Ressalvas que a monografia deve declarar\n")
for t in [
    "**A M4 mede volume, não qualidade** (Macedo, 2026, Tab. 7): o BMAD gera mais tipos de artefato por construção (PRD, UX, arquitetura, épicos e uma spec por story).",
    "**O tempo ativo conta até 30 min de espera do pesquisador por pausa** (P5c). O B tem mais pausas previstas pela metodologia (a série M5b), então parte da diferença de M2 é estrutural ao processo.",
    "**Topologia de agentes** (ameaça já registrada na M3): o B usa subagentes nas revisões; o custo não é comparável como \"eficiência\" sem essa ressalva.",
    "**Ciclo B com mais erros de execução do pesquisador**, todos declarados (D-038 a D-094), com as mensagens livres só em sensibilidade.",
    "**Cinco unidades do B passaram do teto de 8 h** por decisão registrada (D-058, D-060, D-064, D-080, D-090); a análise principal pode tratar o estado no teto como o resultado censurado, e a continuação como sensibilidade.",
    "**Retrospectivas do B** rodaram no fim, em lote (D-092, D-093), e estão em linha própria (`M2_retro_h`), fora de `PLAN` e das unidades.",
    "**Parte IV reduzida** (D-097): os resultados de produto (M6 a M15) não foram avaliados por prazo; este documento não permite concluir qual ciclo entrega o produto melhor.",
]:
    w(f"- {t}")
(ROOT / "docs" / "resultados-processo.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("gravado docs/resultados-processo.md")
