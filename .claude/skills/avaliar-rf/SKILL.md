---
name: avaliar-rf
description: Parte estatica da avaliacao de uma unidade (F000, RF01..RF10) de um ciclo - M4, M6 (parte D), M7, M8, M9 (hardcodes), M10 (assinaturas), M12, M13 numa copia temporaria da tag; so na tag final tambem M8b e M11/M10_cenarios a partir dos resultados do hold-out. Grava uma linha em rf.csv (esquema C-002). Uso - /avaliar-rf <ciclo> <ID>.
disable-model-invocation: true
---

# /avaliar-rf `<ciclo>` `<ID>` (ex.: `/avaliar-rf A RF04`)

**Quando:** só na fase de avaliação (Parte IV), depois do `GATE-H02` e do `GATE-V01`. Nunca durante um ciclo. **Antes do GATE-H02 só rode sobre o repositório de calibração** (`calibracao/montar-repo.sh <destino>` gera um git com as tags `v1`/`v2`).

## Regras (do `protocolo.md` e das métricas)
- Trabalhe **sempre numa cópia temporária da tag** (os módulos já usam `git archive`); nunca grave coverage, lcov ou relatório no repositório do app.
- Saída **só** em pasta de avaliação (`--saida`); o script recusa qualquer caminho com `dados/`. Em calibração use `calibracao/saida/` (ignorada pelo git).
- Não abra o repositório de nenhum ciclo antes da Parte IV (regra 8). Não leia `segredos/`.

## Passos
1. Resolva a tag da unidade e a **tag anterior** (ordem P9) em `dados/<ciclo>/tags.csv` (só leitura). Primeira unidade (`F000`): sem tag anterior (M6/M7_novas/M13 ficam vazios).
2. Rode (ajuste os caminhos; `--repo` é o clone local do repositório do ciclo, ou o de calibração):

```bash
python3 -m harness.avaliador.avaliar_rf --repo <repo> --ciclo <A|B> --id-rf <ID> --tag <tag> --tag-anterior <tag-anterior> \
  --unidade-dir <pasta do plano, ex. specs/003-...> --contrato <pasta com openapi.yaml, error-taxonomy.md e README.md do backend> \
  --chat-feature <nome da feature de chat> --entries-feature <nome da feature de entradas> --saida <pasta-de-saida>
```
   - Ciclo B: `--metodologia bmad` (os caminhos do BMAD em `harness/estatico/m4_artefatos.py` são **palpite** a confirmar) e o `M6_tasks` vem das stories do `mapa-stories.csv` (`harness/estatico/m6_aderencia.tasks_pct`).
   - **Só na tag `final`:** acrescente `--final --hold-out <json com M10_cenarios e M11 por RF> --m8b` (o build, o Maestro e os screenshots ficam no `V-002`; este passo só consome o resultado).
3. Confira a linha gravada em `<saida>/rf.csv` e responda só com: unidade, tag e **os números da linha** (a Parte IV é o primeiro momento em que números de métrica podem ser vistos; antes disso, só calibração).

Métricas por tag: 4, 6 (D), 7, 8, 9 (hardcodes), 10 (assinaturas), 12, 13. Só na `final`: 8b, 9 (cor, tipografia), 10 (cenários), 11.
