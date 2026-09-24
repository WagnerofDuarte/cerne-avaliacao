# Avaliador LLM — protocolo comum das rubricas

**Destino:** `cerne-avaliacao/harness/juiz/` · **Tarefa:** `C-021` · **Versão:** v1.0 (24/09/2026)
**Base:** documento de métricas v1.0, §6.

| Item | Valor |
|---|---|
| Modelo | `gpt-5.5-2026-04-23` (OpenAI; snapshot datado; aceita imagem). Disponibilidade conferida na página de descontinuações da OpenAI no `GATE-C23` e no `GATE-V01` |
| Parâmetros | `reasoning.effort = "medium"`, explícito em toda chamada; demais no padrão, todos registrados no log |
| Saída | JSON validado contra o schema da rubrica; resposta fora do schema = execução inválida, repetida uma vez; se falhar de novo, o item vai para a amostra humana |
| Execuções | 3 por item; resultado = voto majoritário (regra de maioria de cada rubrica) |
| Sem maioria | Item vai obrigatoriamente para a amostra humana |
| Log | Toda execução em `dados/julgamentos.jsonl`: métrica, item, ciclo anonimizado, nº da execução, entrada (hash), saída, voto final, modelo, parâmetros, data, hash do prompt |
| Prompts | Os textos marcados "Prompt" em cada rubrica, com hash congelado; qualquer revisão antes do congelamento ganha versão (v1.0, v1.1…) e entrada no changelog abaixo |

## Anonimização (vale para todas as rubricas)

Antes de enviar qualquer material ao avaliador, o harness:
1. troca o rótulo do ciclo por um código aleatório fixado por item (`X` ou `Y`), sem relação com A/B;
2. renomeia diretórios e arquivos que identificam a metodologia para rótulos neutros — ex.: `.specify/` → `plan-meta/`, `specs/NNN-nome/` → `plan-docs/unit-NN/`, diretórios de saída do BMAD → `plan-docs/` — e aplica o mesmo mapeamento aos caminhos citados no texto;
3. remove do texto, por regex, os termos `spec kit`, `spec-kit`, `speckit`, `bmad`, `bmm`, `brainstorming session`, nomes de persona do BMAD e cabeçalhos de template que identificam a ferramenta (lista congelada em `anonimizacao.txt`, escrita na trilha paralela e testada no repositório de calibração);
4. nunca envia o nome da metodologia, do ciclo, da tag ou datas.

## Rubricas

| Arquivo | Métrica | Item avaliado | Entrada |
|---|---|---|---|
| `m6-aderencia.md` | M6 (parte J) | Uma unidade | Plano da unidade + diff da unidade |
| `m9-espacamento.md` | M9 (espaçamento) | Um estado | Screenshot do app + frame do protótipo |
| `m14-handoff.md` | M14 | Uma decisão | Decisão + árvore e trechos do código final |
| `d16-severidade.md` | D16 | Uma intervenção de correção | Texto da intervenção + critério de aceite envolvido |

## Critério de aceite desta tarefa

Cada rubrica traz um **exemplo sintético** com a saída esperada. No `GATE-C22`, o Wagner aplica a rubrica à mão ao exemplo e confere se chega à mesma saída. Divergência = ajustar a rubrica antes do congelamento.

## Changelog
- v1.0 (24/09/2026) — versão inicial.
