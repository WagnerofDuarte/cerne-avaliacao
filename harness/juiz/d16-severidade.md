# Rubrica D16 — reclassificação de severidade das correções

**Item:** uma intervenção do tipo `correção` (linha de `intervencoes.csv`).
**Papel do avaliador:** **validador**, nunca classificador primário — a severidade registrada no momento pelo pesquisador é o dado; o avaliador serve para medir a concordância (κ). Métricas v1.0, §5.4.
**Entrada enviada:** (1) o texto da mensagem de intervenção, sem o prefixo (sem a severidade dada pelo pesquisador); (2) o texto do critério de aceite ou requisito ao qual o sintoma se refere, quando a mensagem o identifica.

## Escala de severidade (decidida em 24/09/2026, R30)
Derivada do eixo "bloqueante / não bloqueante" da política de defeito do backend (D16), aplicada ao app:

| Nível | Definição |
|---|---|
| `S1` — cosmético | Detalhe visual ou de texto; nenhum critério de aceite afetado |
| `S2` — funcional com contorno | Um critério de aceite ou requisito falha em parte, mas o fluxo é utilizável ou há contorno razoável |
| `S3` — bloqueante | Um critério de aceite fica impossível de cumprir, ou há crash ou perda de dados do usuário |

## Prompt (v1.0)

```text
You classify the severity of a defect reported during app development, from its SYMPTOM description.

S1 = cosmetic: a visual or text detail; no acceptance criterion is affected.
S2 = functional with workaround: an acceptance criterion or requirement partly fails, but the flow is
usable or there is a reasonable workaround.
S3 = blocking: an acceptance criterion becomes impossible to meet, or there is a crash or loss of user data.

Use only the information given. Answer only with JSON matching the schema.

SYMPTOM:
<<<SYMPTOM>>>

RELATED REQUIREMENT (may be empty):
<<<REQUIREMENT>>>
```

## Schema da saída

```json
{"severity": "S1|S2|S3", "justification": "string"}
```

## Regra de maioria
`severity` com ≥ 2 das 3 execuções; três níveis diferentes = sem maioria → amostra humana. **Resultado:** concordância pesquisador × avaliador (κ de Cohen) na amostra; a classificação humana continua sendo o dado primário qualquer que seja o κ.

## Exemplo sintético
**Sintoma:** "When I save an audio entry and the network drops, the app closes and the transcribed text is lost." **Requisito:** RNF09.
**Saída esperada:** `{"severity": "S3", "justification": "Crash with loss of user data."}`
