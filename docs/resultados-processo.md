# Resultados de processo (M1 a M5) e M4 — Ciclo A (Spec Kit) × Ciclo B (BMAD)

**Origem dos números:** `dados/processo/ciclo.csv`, `dados/processo/rf.csv` e `dados/processo/m4.csv`, gerados por `harness/h007/agregar_processo.py` e `harness/h007/contar_m4.py` a partir das tabelas re-derivadas dos transcritos brutos (`dados/<ciclo>/rederivado/`, H-007, D-096). **Recorte e ordem dos portões:** D-097 (Parte IV antecipada e reduzida por prazo, antes do `GATE-H02`). **Fora deste documento, por não terem sido avaliadas:** M6 (parte do avaliador), M7 a M15 e a validação do avaliador (ver D-097).

**Como ler.** Tempo ativo (P5c): intervalos que terminam numa ação do agente contam inteiros; esperas pelo pesquisador contam até 30 min cada (o excedente vai para a pausa). Tokens e custo: transcrito principal mais subagentes; custo pela tabela congelada `harness/precos.md`. As unidades (F000 e RF01 a RF10) são as mesmas nos dois ciclos, mas a decomposição interna difere (Spec Kit: comandos por unidade; BMAD: stories, com um laço `bmad-build`, `bmad-code-review` e QA por story). Diferenças absolutas **não** são leitura de "melhor" ou "pior": ver as ameaças à validade.

## 1. Resumo por ciclo

| Métrica | Ciclo A (Spec Kit) | Ciclo B (BMAD) |
|---|---:|---:|
| M1 instalação (h) | 0.001 | 0.004 |
| M1 sessões SETUP (h) | 0.11 | 0.14 |
| M1 total (h) | 0.11 | 0.14 |
| M1 calendário, instalação → `setup-done` (h) | 101.0 | 3.1 |
| M2 tempo ativo total (h) | 25.9 | 82.7 |
| M2 só das 11 unidades (h) | 25.8 | 75.1 |
| M2 planejamento global `PLAN` (h) | 0.0 | 5.4 |
| M2 retrospectivas, `PLAN` depois de `plan-done` (h) | 0.0 | 2.0 |
| M2 fase ESPEC (h) | 7.6 | 5.5 |
| M2 fase IMPL (h) | 13.5 | 48.8 |
| M2 fase VALID (h) | 4.9 | 28.4 |
| Pausa fora do tempo ativo (h) | 23.0 | 38.0 |
| Sessões medidas | 138 | 136 |
| M3 tokens de entrada (agente principal) | 10 982 | 18 606 |
| M3 tokens de saída (agente principal) | 4 899 118 | 8 484 315 |
| M3 cache read (agente principal) | 788 931 858 | 1 463 672 039 |
| M3 cache write (agente principal) | 15 761 098 | 24 295 944 |
| M3 tokens de saída dos subagentes | 373 | 640 253 |
| M3 custo (USD) | 271.21 | 901.86 |
| M3 razão entrada:saída (com cache) | 165.3 | 325.5 |
| M3 fração de cache read na entrada | 0.980 | 0.974 |
| M5 intervenções (leitura principal) | 49 | 16 |
| M5 intervenções, leitura ampla (sensibilidade) | 66 | 51 |
| M5b respostas `PROCESSO:` (revisão exigida pelo processo) | 67 | 279 |
| M4 artefatos na tag `final` | 128 | 83 |
| M4 artefatos em `plan-done` (só B) | — | 31 |

## 2. M5 por tipo, causa e fase (leitura principal)

| | A | B |
|---|---:|---:|
| tipo `correção` | 40 | 14 |
| tipo `esclarecimento não solicitado` | 9 | 2 |
| causa `prd` (diferença contra o protótipo/pacote) | 40 | 11 |
| causa `chk` | 0 | 1 |
| causa `inc` | 0 | 2 |
| severidade S1 | 7 | 0 |
| severidade S2 | 27 | 11 |
| severidade S3 | 6 | 3 |
| fase ESPEC | 1 | 1 |
| fase IMPL | 45 | 15 |
| fase VALID | 3 | 0 |
| M5b fase ESPEC | 11 | 42 |
| M5b fase IMPL | 21 | 90 |
| M5b fase VALID | 35 | 147 |

**Sensibilidade da M5** (mensagens livres, sem prefixo, que a leitura principal não conta; `dados/<ciclo>/rederivado/mensagens_livres.csv`):

| | A | B |
|---|---:|---:|
| intervenções de sessões descartadas sem coleta (D-037, D-094) | 2 | 1 |
| interrupções por Esc | 9 | 16 |
| retomadas (`continue`, `ask again`, `Try again`) | 4 | 9 |
| outras mensagens livres | 2 | 9 |
| mensagens neutras (`Yes`, `Yes, proceed.`; não contam) | 8 | 11 |
| respostas de painel por clique, sem prefixo (não contam) | 1 | 21 |

## 3. Por unidade

Tempo ativo (h), tempo de calendário desde a tag anterior (h), custo (USD), intervenções (M5, leitura principal) e `PROCESSO:` (M5b). `>teto`: tempo ativo acima do teto de 8 h (12 h na F000); a unidade seguiu por decisão registrada (D-058, D-060, D-064, D-080, D-090). RF02 do B não teve sessões (nota B7).

| Unid. | Ciclo | Fecho | Sessões | Ativo (h) | Calendário (h) | Custo (USD) | M5 | M5b | |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| F000 | A | done | 16 | 3.19 | 5.4 | 23.15 | 5 | 8 |  |
| F000 | B | done | 21 | 12.04 | 180.4 | 117.59 | 1 | 45 | >teto |
| RF03 | A | done | 12 | 1.46 | 23.2 | 15.63 | 4 | 4 |  |
| RF03 | B | incompleto | 14 | 8.43 | 12.8 | 91.62 | 2 | 27 | >teto |
| RF01 | A | done | 13 | 2.92 | 21.7 | 28.67 | 4 | 7 |  |
| RF01 | B | done | 20 | 11.24 | 23.2 | 123.09 | 4 | 34 | >teto |
| RF02 | A | done | 10 | 1.47 | 94.9 | 15.88 | 2 | 7 |  |
| RF02 | B | done | 0 | 0.00 | 0.0 | 0.00 | 0 | 0 |  |
| RF07 | A | done | 9 | 1.46 | 2.6 | 19.23 | 1 | 5 |  |
| RF07 | B | done | 13 | 5.74 | 12.9 | 81.87 | 0 | 24 |  |
| RF06 | A | done | 10 | 2.38 | 43.0 | 23.43 | 5 | 6 |  |
| RF06 | B | done | 10 | 5.09 | 5.7 | 76.90 | 1 | 20 |  |
| RF04 | A | incompleto | 28 | 5.15 | 32.1 | 59.54 | 13 | 13 |  |
| RF04 | B | done | 12 | 6.84 | 8.4 | 93.13 | 7 | 20 |  |
| RF10 | A | done | 9 | 1.71 | 47.7 | 17.52 | 2 | 2 |  |
| RF10 | B | done | 3 | 2.46 | 11.0 | 36.05 | 0 | 7 |  |
| RF08 | A | done | 9 | 1.95 | 42.3 | 19.27 | 4 | 2 |  |
| RF08 | B | done | 5 | 3.42 | 3.3 | 37.47 | 0 | 5 |  |
| RF05 | A | done | 10 | 2.05 | 3.5 | 21.04 | 2 | 5 |  |
| RF05 | B | done | 9 | 11.24 | 21.6 | 68.81 | 0 | 21 | >teto |
| RF09 | A | done | 11 | 2.10 | 15.4 | 27.43 | 7 | 8 |  |
| RF09 | B | done | 15 | 8.65 | 23.5 | 110.02 | 0 | 32 | >teto |

## 4. M4 por tipo (arquivos)

**Ciclo A, tag `final`:**

| Tipo | Arquivos |
|---|---:|
| constitution | 1 |
| spec | 11 |
| plan | 11 |
| tasks | 11 |
| pesquisa_modelo_quickstart | 33 |
| contratos | 39 |
| checklists | 22 |
| outros_specs | 0 |
| **Total** | **128** |

**Ciclo B** (`_bmad-output/`; `.memlog.md` fora da leitura principal):

| Tipo | `plan-done` | `final` |
|---|---:|---:|
| brainstorming | 1 | 1 |
| forge | 2 | 2 |
| pesquisa | 5 | 5 |
| prfaq | 2 | 2 |
| brief | 2 | 2 |
| prd | 6 | 6 |
| relatorio_validacao_prd | 2 | 2 |
| ux | 2 | 2 |
| arquitetura | 7 | 7 |
| epicos | 1 | 9 |
| stories | 0 | 34 |
| sprint_status | 1 | 1 |
| retrospectivas | 0 | 8 |
| outros_implementacao | 0 | 2 |
| **Total** | **31** | **83** |

## 5. Ressalvas que a monografia deve declarar

- **A M4 mede volume, não qualidade** (Macedo, 2026, Tab. 7): o BMAD gera mais tipos de artefato por construção (PRD, UX, arquitetura, épicos e uma spec por story).
- **O tempo ativo conta até 30 min de espera do pesquisador por pausa** (P5c). O B tem mais pausas previstas pela metodologia (a série M5b), então parte da diferença de M2 é estrutural ao processo.
- **Topologia de agentes** (ameaça já registrada na M3): o B usa subagentes nas revisões; o custo não é comparável como "eficiência" sem essa ressalva.
- **Ciclo B com mais erros de execução do pesquisador**, todos declarados (D-038 a D-094), com as mensagens livres só em sensibilidade.
- **Cinco unidades do B passaram do teto de 8 h** por decisão registrada (D-058, D-060, D-064, D-080, D-090); a análise principal pode tratar o estado no teto como o resultado censurado, e a continuação como sensibilidade.
- **Retrospectivas do B** rodaram no fim, em lote (D-092, D-093), e estão em linha própria (`M2_retro_h`), fora de `PLAN` e das unidades.
- **Parte IV reduzida** (D-097): os resultados de produto (M6 a M15) não foram avaliados por prazo; este documento não permite concluir qual ciclo entrega o produto melhor.
