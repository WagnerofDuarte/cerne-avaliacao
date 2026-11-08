---
name: validar-juiz
description: Validacao humana cega do avaliador - sorteia amostra dos julgamentos (>= 20 itens por metrica julgada M6, espacamento M9, M14, D16, somados aos itens sem maioria), apresenta ao pesquisador SEM o voto do avaliador e SEM o ciclo de origem, recolhe as classificacoes e calcula o kappa de Cohen por metrica (limiar 0,61). Uso - /validar-juiz.
disable-model-invocation: true
---

# /validar-juiz

**Depois** de `/avaliar-ciclo` dos dois ciclos. **Cegueira obrigatória:** o assistente NÃO pode ler `julgamentos.jsonl` nem `amostra-chave.json` (têm o voto e o ciclo); só os scripts os leem. O pesquisador só vê `amostra-cega.json` (`amostra_id`, métrica e material).

1. Sortear (grava `amostra-cega.json` e `amostra-chave.json` na pasta de saída; o segundo é só do script):
```bash
python3 -m harness.avaliador.validar_juiz sortear --saida <pasta-de-saida> [--minimo 20] [--material material.json]
```
2. Mostre ao pesquisador, **um item por vez**, só `amostra_id`, `metrica` e `material` de `amostra-cega.json` (M6: nº de divergências não documentadas que ele conta; M9: `true/false` do espaçamento; M14: `yes/partial/no`; D16: `S1/S2/S3`). Grave as respostas em `classificacoes.csv` com as colunas `amostra_id,classificacao_humana`. Não comente, não sugira, não revele nada do avaliador.
3. Calcular (grava `validacao.csv` no esquema C-002 e `kappa.json`):
```bash
python3 -m harness.avaliador.validar_juiz calcular --saida <pasta-de-saida> --classificacoes classificacoes.csv
```
4. Informe o κ por métrica. **κ < 0,61 → métrica exploratória** (o resultado J é reportado com ressalva e a classificação humana vira o dado principal; na D16 ela já é o dado primário). Nenhuma troca de avaliador ou de rubrica depois de ver os dados. Com n≈20 o intervalo de confiança do κ é largo (limitação declarada).
