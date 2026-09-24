# Rubrica M6 (parte J) — divergências entre plano e código

**Item:** uma unidade (F000, RF01…RF10) de um ciclo.
**Entrada enviada:** (1) o plano da unidade, anonimizado — Ciclo A: `spec.md`, `plan.md` e `tasks.md` da unidade; Ciclo B: a seção pertinente da arquitetura e as stories da unidade, atribuídas pelo `mapa-stories.csv`; (2) o diff do código entre a tag anterior e a tag da unidade (`git diff`, só `lib/` e `test/`), com números de linha.

## Definições
- **Divergência:** diferença verificável entre o que o plano diz que seria feito e o que o diff fez — algo planejado e não feito, feito de forma diferente da planejada, ou feito sem estar no plano **quando muda comportamento, arquitetura, contrato com o backend ou uma decisão de produto**. Estilo, nomes locais e refatorações sem efeito externo não são divergência.
- **Documentada:** o próprio plano (ou um artefato de planejamento da unidade) registra a mudança — ex.: tarefa reescrita, nota de desvio, item de "decisões" atualizado. Comentário no código não conta.
- **Causa:** códigos da M5 — `ctx` (incompatibilidade com o repositório ou o backend: API, caminho, pacote ou convenção inexistente), `chk` (falha de teste, lint ou build), `inc` (implementação incompleta), `prd` (desvio do produto especificado), `amb` (ambiguidade do plano), `out` (outra).

## Prompt (v1.0)

```text
You are auditing whether code followed its plan. You receive a PLAN and a DIFF.

List every divergence between the PLAN and the DIFF. A divergence is a verifiable difference:
something planned and not done, done differently from the plan, or done without being in the plan
when it changes behavior, architecture, the backend contract, or a product decision.
Style, local naming and refactors without external effect are NOT divergences.

For each divergence, say whether the plan itself documents the change (a rewritten task, a
deviation note, an updated decision). Code comments do not count as documentation.

Classify the cause of each divergence with exactly one code:
ctx = mismatch with the repository or backend (nonexistent API, path, package or convention);
chk = test, lint or build failure; inc = incomplete implementation; prd = deviation from the
specified product; amb = the plan was ambiguous; out = other.

Answer only with JSON matching the schema. Cite evidence as file:line from the DIFF.
If there are no divergences, return an empty list.

PLAN:
<<<PLAN>>>

DIFF:
<<<DIFF>>>
```

## Schema da saída

```json
{
  "divergences": [
    {
      "description": "string",
      "evidence": ["path/to/file.dart:123"],
      "documented": true,
      "cause": "ctx|chk|inc|prd|amb|out"
    }
  ]
}
```

## Regra de maioria
Duas divergências de execuções diferentes são **a mesma** quando citam o mesmo arquivo com intervalos de linha que se sobrepõem em até ±10 linhas. Uma divergência entra no resultado se aparece em ≥ 2 das 3 execuções; `documented` e `cause` seguem a maioria entre as ocorrências (empate → item vai para a amostra humana). **Resultado da unidade:** número de divergências com `documented = false` (`M6_div_nao_doc`).

## Exemplo sintético
**Plano:** "Task 3: `EntryRepository.create` returns `Either<Failure, Entry>` and calls `POST /entries`. Task 4: show a spinner while saving."
**Diff:** `lib/features/entries/data/entry_repository_impl.dart:40-58` implementa `create` retornando `Either`, chamando `POST /entries`; nenhum arquivo de `presentation/` alterado; `lib/features/entries/data/entry_repository_impl.dart:60-75` acrescenta um método `deleteEntry` que chama `DELETE /entries/:id`.
**Saída esperada:**
```json
{"divergences":[
 {"description":"Task 4 (spinner while saving) was not implemented","evidence":[],"documented":false,"cause":"inc"},
 {"description":"deleteEntry calls DELETE /entries/:id, which is not in the plan and does not exist in the backend","evidence":["lib/features/entries/data/entry_repository_impl.dart:60"],"documented":false,"cause":"ctx"}
]}
```
