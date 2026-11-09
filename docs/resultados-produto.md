# Resultados das métricas de produto (08/11/2026)

Registro dos resultados de produto coletados depois do congelamento parcial do harness (`harness-v1.0`, D-101). Dados brutos em `dados/produto/`; as tabelas abaixo saem de `python3 scripts/resumo_produto.py`. Texto de referência: seções 4.5 a 4.7 da monografia.

**Escopo e ressalvas**
- Resultados do avaliador (`claude-opus-5-5`, três execuções, voto da maioria) são exploratórios: mesma família do agente, anonimização parcial, validação em 10 itens (D-111).
- M6 do avaliador: 5 de 21 unidades sem maioria; diff truncado em 700 mil caracteres em 8 das 10 unidades do Ciclo B e em 1 do A; sensibilidade com o diff completo em `dados/produto/sensibilidade-m6/` (D-112): Ciclo B 20→14 divergências, Ciclo A 60→59; direção igual nos 9 pares.
- M8b: Ciclo A com os 22 mutantes (19 mortos, IC95% de Wilson 67% a 95%); Ciclo B por amostra de 40 em 133 (6 mortos, 7% a 29%).
- M14: 4 decisões no Ciclo A e 6 no B (abaixo das 8 mínimas; D-109).
- M11 é medida pelas rodadas da verificação manual de fechamento (P6), registro não cego; as rodadas foram extraídas do plano de ciclos por um agente de leitura e conferidas por amostragem.
- Um teste de temporizador do Ciclo A (RF08) falhou uma vez sob carga da máquina e passou em 3 reexecuções isoladas; o dado original foi mantido (D-110).

## Estado final por ciclo (tag `final`)

| Ciclo | Testes | M7 viol. | M9 hardcodes | M10 assin. fora | M12 média | M12 acima | M8 domínio | M15 diverg. | M14 |
|---|---|---|---|---|---|---|---|---|---|
| A | 660 | 0 | 16 | 56 | 1.537 | 0 | 92.1 % | 31 | 1 |
| B | 1309 | 0 | 2 | 18 | 1.882 | 1 | 44.8 % | 36 | 0.667 |

## M8b — mutação (domínio)

| Ciclo | Enumerados | Amostra | Mortos | Sobreviventes | Erro compilação | Escore |
|---|---|---|---|---|---|---|
| A | 22 | todos | 19 | 3 | 0 | 86.4 % |
| B | 133 | 40 | 6 | 34 | 0 | 15 % |

## M6 — aderência ao plano (D = estática; J = juiz Opus 5.5, maioria de 3)

| Unidade | A tasks % | A alt. não citados | A citados não alt. | A inex. arq | A inex. pkg | A inex. backend | A J div. não doc. | A J diff trunc. | B tasks % | B alt. não citados | B citados não alt. | B inex. arq | B inex. pkg | B inex. backend | B J div. não doc. | B J diff trunc. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F000 | 1 | 33 | 0 | 0 | 3 | 108 | 7 | False | 1 | 2 | 0 | 0 | 2 | 114 | 3 | True |
| RF03 | 0.981 | 26 | 0 | 0 | 1 | 4 | 8 | False | 1 | 1 | 5 | 2 | 3 | 14 | 2 | True |
| RF01 | 0.986 | 34 | 0 | 0 | 1 | 34 | 4 | False | 1 | 0 | 5 | 0 | 1 | 22 | 2 | True |
| RF02 | 0.978 | 12 | 0 | 0 | 1 | 0 | 4 | False | — | — | — | — | — | — | — | — |
| RF07 | 0.951 | 21 | 1 | 0 | 2 | 25 | 3 | False | 1 | 5 | 9 | 0 | 0 | 28 | 0 | True |
| RF06 | 0.978 | 17 | 1 | 0 | 1 | 29 | 11 | False | 1 | 4 | 1 | 0 | 0 | 21 | 7 | True |
| RF04 | 0.984 | 26 | 0 | 0 | 0 | 32 | 7 | True | 1 | 5 | 5 | 0 | 0 | 36 | 6 | True |
| RF10 | 0.900 | 14 | 0 | 0 | 0 | 6 | 2 | False | 1 | 0 | 0 | 0 | 1 | 5 | 0 | False |
| RF08 | 0.976 | 11 | 0 | 0 | 2 | 10 | 4 | False | 1 | 0 | 0 | 0 | 1 | 16 | 0 | False |
| RF05 | 0.920 | 19 | 1 | 0 | 0 | 24 | 5 | False | 1 | 18 | 4 | 0 | 0 | 57 | 0 | True |
| RF09 | 0.985 | 32 | 0 | 0 | 0 | 22 | 5 | False | 1 | 0 | 3 | 0 | 0 | 25 | 0 | True |

## Qualidade estática e testes no estado de cada unidade

| Unidade | A M7 | A M9 | A M10 | A M12 | A testes | A M13 | A apagados | B M7 | B M9 | B M10 | B M12 | B testes | B M13 | B apagados |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F000 | 0 | 0 | 6 | 1.143 | 85 | — | — | 0 | 0 | 6 | 2.200 | 264 | — | — |
| RF03 | 0 | 0 | 26 | 1.368 | 131 | 0 | 0 | 0 | 2 | 16 | 2.200 | 367 | 0.011 | 3 |
| RF01 | 0 | 2 | 38 | 1.444 | 196 | 0 | 0 | 0 | 2 | 16 | 3 | 566 | 0 | 0 |
| RF02 | 0 | 2 | 38 | 1.370 | 214 | 0.194 | 38 | 0 | 2 | 16 | 3 | 566 | 0 | 0 |
| RF07 | 0 | 2 | 38 | 1.545 | 264 | 0 | 0 | 0 | 2 | 16 | 2.065 | 721 | 0.004 | 2 |
| RF06 | 0 | 6 | 38 | 1.615 | 336 | 0 | 0 | 0 | 2 | 16 | 2.106 | 840 | 0 | 0 |
| RF04 | 0 | 12 | 44 | 1.551 | 431 | 0 | 0 | 0 | 2 | 16 | 2.190 | 971 | 0.005 | 4 |
| RF10 | 0 | 12 | 48 | 1.551 | 468 | 0 | 0 | 0 | 2 | 16 | 2.013 | 1006 | 0 | 0 |
| RF08 | 0 | 12 | 48 | 1.509 | 517 | 0 | 0 | 0 | 2 | 16 | 2 | 1051 | 0 | 0 |
| RF05 | 0 | 15 | 48 | 1.491 | 586 | 0 | 0 | 0 | 2 | 16 | 1.857 | 1135 | 0 | 0 |
| RF09 | 0 | 16 | 56 | 1.537 | 660 | 0 | 0 | 0 | 2 | 18 | 1.882 | 1309 | 0.001 | 1 |

## M11-P6 — verificação manual de fechamento (não cega; D-103)

| Unidade | A rodadas | A 1ª aprovada | A final | B rodadas | B 1ª aprovada | B final |
|---|---|---|---|---|---|---|
| F000 | 3 | não | sim | 2 | não | sim |
| RF03 | 2 | não | sim | 2 | não | incompleta |
| RF01 | 4 | não | sim | 3 | não | sim |
| RF02 | 3 | não | sim | 1 | sim | sim |
| RF07 | 2 | não | sim | 1 | sim | sim |
| RF06 | 3 | não | sim | 2 | não | sim |
| RF04 | 5 | não | incompleta | 3 | não | sim |
| RF10 | 2 | não | sim | 1 | sim | sim |
| RF08 | 2 | não | sim | 1 | sim | sim |
| RF05 | 3 | não | sim | 1 | sim | sim |
| RF09 | 4 | não | sim | 1 | sim | sim |

## Testes pareados (9 pares, Wilcoxon-Pratt, p exato bilateral / r bisserial; exploratório)

| Métrica | n | mediana A | mediana B | mediana das dif. (B−A) | B>A / B<A | p / r | nota |
|---|---|---|---|---|---|---|---|
| P6 — rodadas até fechar | 9 | 3 | 1 | -1 | 0/8 | 0.0078 / -1.00 | A: RF01+RF02; B: só a RF01 (D-098) |
| M6-D — arquivos alterados não citados | 9 | 21 | 1 | -16 | 0/9 | 0.0039 / -1.00 | B: plano = stories |
| M6-J — divergências não documentadas | 9 | 5 | 0 | -4 | 0/9 | 0.0039 / -1.00 | diff do B truncado em 8/10 unidades |
| M13 — testes apagados | 9 | 0 | 0 | 0 | 4/1 | 0.3750 / 0.49 | uma unidade do A concentra 38 |
