---
name: avaliar-ciclo
description: Agrega as metricas de um ciclo apos cicloX/final - M1 a M5 (a partir dos CSVs da coleta, com a linha PLAN e a serie M5b), M4 total, M8b, M9 (screenshots, espacamento pelo avaliador com visao e score), M10_cenarios, M14 (checks estaticos + avaliador) e M15; grava ciclo.csv e estados_m9.csv. Uso - /avaliar-ciclo <ciclo>.
disable-model-invocation: true
---

# /avaliar-ciclo `<ciclo>`

**Quando:** depois de `cicloX/final`, de `/avaliar-rf` (todas as unidades) e `/julgar-rf`. Mesmas regras de cegamento e de saída (nunca em `dados/`).

```bash
python3 -m harness.avaliador.avaliar_ciclo --repo <repo> --ciclo <A|B> --tag-final <tag final> --tag-rf01 <tag rf01-done> \
  --ref-feature <feature do RF01> --constitution <caminho da constitution na tag> --plan-f000 <plan.md da F000 na tag> \
  --dados <pasta com sessoes.csv, segmentos.csv, intervencoes.csv, revisoes_processo.csv, tags.csv> \
  --estados-json <lista de estados: estado_id, cor_ok, tipografia_ok, screenshot, referencia, alcancavel> \
  --hold-out <json com M10_cenarios> --saida <pasta-de-saida>      # + --simulado respostas.json sem rede
```
O que entra em `ciclo.csv` (esquema C-002): M1 (instalação, sessão `SETUP`, calendário), M2 (total e por fase, `M2_plan_h` da linha `PLAN`), M3 (tokens, subagentes, custo, razões), M4 total, M5 e M5b, M8b (de `m8b-<ciclo>.json`, vazio se retirada), M10 cenários, **M14** (seleção por `harness/regras.md` §1; decisões estáticas por check, as demais pelo avaliador com `m14-handoff.md`; ≥ 8–10 decisões), **M15** (C1–C4 de `harness/regras.md` §2), **M9** (`estados_m9.csv`: cor e tipografia vêm do H-004/H-003; **espaçamento** pelo avaliador com visão, par screenshot × frame; score 0–3 = soma dos três booleanos; estado inalcançável = 0).

Avaliador `gpt-5.5-2026-04-23`, `reasoning.effort = medium`, 3 execuções, voto majoritário, tudo em `julgamentos.jsonl`. Gere as tabelas da monografia só no `V-006`. Responda só com o caminho dos CSVs e o que faltou (dados de entrada ausentes, itens sem maioria).
