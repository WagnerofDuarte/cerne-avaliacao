---
name: julgar-rf
description: M6 parte J - envia ao avaliador LLM (gpt-5.5-2026-04-23, reasoning.effort medium) o plano anonimizado da unidade e o diff, 3 execucoes com voto majoritario; grava julgamentos.jsonl e M6_div_nao_doc em rf.csv. Uso - /julgar-rf <ciclo> <ID>, depois de /avaliar-rf do mesmo RF.
disable-model-invocation: true
---

# /julgar-rf `<ciclo>` `<ID>`

**Depois** de `/avaliar-rf` do mesmo RF (a linha de `rf.csv` já existe). Mesmas regras de cegamento e de saída do `/avaliar-rf`.

## O que o script faz (`harness/avaliador/julgar_rf.py`)
1. Monta o **plano** (`spec.md`, `plan.md`, `tasks.md` da unidade; no B, arquitetura + stories do `mapa-stories.csv`) e o **diff** da tag anterior até a tag da unidade (só `lib/` e `test/`, com números de linha), e **anonimiza** tudo com `harness/juiz/anonimizacao.txt` (termos, cabeçalhos de template, diretórios → rótulos neutros; sem nome de metodologia, ciclo, tag ou data). O ciclo vira `X`/`Y` por um código fixo por item.
2. Usa o **prompt congelado** de `harness/juiz/m6-aderencia.md` (v1.1), 3 execuções, resposta inválida repetida 1 vez; voto majoritário pela regra da rubrica (mesma divergência = mesmo arquivo com linhas a ±10; vale se aparece em ≥ 2 de 3; empate em `documented`/`cause` → **sem maioria → amostra humana**).
3. Grava cada execução em `<saida>/julgamentos.jsonl` (esquema C-002 + `hash_entrada`) e `M6_div_nao_doc` em `rf.csv`.

```bash
python3 -m harness.avaliador.julgar_rf --repo <repo> --ciclo <A|B> --id-rf <ID> --tag <tag> --tag-anterior <anterior> \
  --unidade-dir <pasta do plano> --saida <pasta-de-saida>            # chave: OPENAI_API_KEY do ambiente do operador
python3 -m harness.avaliador.julgar_rf ... --simulado respostas.json    # SEM rede: respostas simuladas (testes/calibração)
```
**Segredos:** a chave vem só de `OPENAI_API_KEY` no ambiente; nunca peça, leia de arquivo nem escreva a chave. A chamada real nunca foi exercitada pela trilha do harness (só simulada): rode primeiro um item de calibração.
Não altere o prompt nem a rubrica: mudança = desvio registrado. Itens `sem_maioria` seguem para o `/validar-juiz`.
