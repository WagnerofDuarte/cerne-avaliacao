# Gabarito do repositório de calibração (H-001)

Fonte única: `gabarito.json` (escrito à mão; linhas conferidas com `grep -n` nos snapshots). Este arquivo é gerado por `python3 gerar_gabarito_md.py`.
`v1` = unidade anterior (papel de `rf01-done`); `v2` = unidade medida (papel de `final`). Montagem: `./montar-repo.sh <destino>`.

## M4 — artefatos (Spec Kit)

- `v1`: {'constitution': 1, 'spec': 1, 'plan': 0, 'tasks': 0, 'research': 0, 'data_model': 0, 'quickstart': 0, 'contracts': 0, 'checklists': 0, 'analysis': 0, 'total': 2}
- `v2`: {'constitution': 1, 'spec': 1, 'plan': 1, 'tasks': 1, 'research': 1, 'data_model': 1, 'quickstart': 1, 'contracts': 1, 'checklists': 1, 'analysis': 1, 'total': 10}

Decoy: `specs/001-entries/notes.txt` (não conta).

## M6 — parte D (unidade v2, anterior v1)

- `m6_tasks`: 0.75
- `citados_nao_alterados`: ['lib/features/entries/domain/usecases/classify_entry.dart', 'lib/features/entries/domain/usecases/export_entries.dart']
- `alterados_nao_citados`: ['lib/features/entries/data/models/entry_json.dart', 'lib/features/entries/domain/usecases/audit_entry.dart', 'lib/features/timeline/presentation/pages/timeline_card.dart']
- `inexist_arq`: ['lib/features/entries/domain/usecases/export_entries.dart']
- `inexist_pkg`: ['dio']
- `inexist_backend`: {'c1': ['POST /entries/search'], 'c2': ['entries-bulk-purge'], 'c3': ['phantomField'], 'c4': ['ENTRY_GHOST_ERROR']}
- `inexist_backend_total`: 4

## M7 — imports proibidos (RNF06)

**v1**

| arquivo | linha | regra |
|---|---|---|
| lib/features/entries/domain/usecases/format_badge.dart | 1 | dominio_importa_flutter |
| lib/features/entries/domain/entities/leaky_entry.dart | 1 | dominio_importa_data |

**v2**

| arquivo | linha | regra |
|---|---|---|
| lib/features/entries/domain/usecases/format_badge.dart | 1 | dominio_importa_flutter |
| lib/features/entries/domain/entities/leaky_entry.dart | 1 | dominio_importa_data |
| lib/features/entries/domain/usecases/audit_entry.dart | 1 | dominio_importa_data |

`M7_novas` em v2: 1

## Regras estruturais (contam na M11)

**rf07_bloc_importa_bloc**

| arquivo | linha |
|---|---|
| lib/features/timeline/presentation/bloc/timeline_bloc.dart | 3 |

**rf10_chat_importa_entradas**

| arquivo | linha |
|---|---|
| lib/features/chat/presentation/cubit/chat_cubit.dart | 3 |

## M9 — hardcodes (v1 e v2)

| arquivo | linha | tipo |
|---|---|---|
| lib/features/entries/presentation/pages/entries_page.dart | 13 | cor |
| lib/features/entries/presentation/pages/entries_page.dart | 14 | espacamento |
| lib/features/entries/presentation/pages/entries_page.dart | 21 | tamanho_fonte |
| lib/features/entries/presentation/pages/entries_page.dart | 22 | familia_fonte |

Decoys que NÃO contam: literais em `core/design_tokens.dart`, em comentário e dentro de string (`entries_page.dart` linhas 6 e 11).

## M10 — assinaturas fora de `Either` (v1 e v2)

| arquivo | linha | metodo |
|---|---|---|
| lib/features/chat/domain/repositories/chat_repository.dart | 9 | ChatRepository.lastDraft |
| lib/features/chat/data/repositories/chat_repo.dart | 13 | ChatRepo.lastDraft |

## M12 — complexidade ciclomática à mão (domínio)

1 + if, for, for-in, while, do, case (cada rotulo; default nao conta), catch, &&, ||, ?:, ??, if de colecao. for de colecao NAO conta (nao esta na lista). Corpo de closure conta no metodo que a contem. So declaracoes com corpo (bloco ou =>); construtor sem corpo e metodo abstrato nao entram.

| arquivo | linha | metodo | cc |
|---|---|---|---|
| lib/features/entries/domain/entities/entry.dart | 22 | Entry.isMedia | 2 |
| lib/features/entries/domain/entities/leaky_entry.dart | 8 | LeakyEntry.describe | 2 |
| lib/features/entries/domain/usecases/classify_entry.dart | 4 | ClassifyEntry.call | 12 |
| lib/features/entries/domain/usecases/summarize_entries.dart | 11 | SummarizeEntries.call | 5 |
| lib/features/entries/domain/usecases/validate_entry.dart | 4 | ValidateEntry.call | 2 |
| lib/features/entries/domain/usecases/format_badge.dart | 4 | FormatBadge.label | 1 |
| lib/features/timeline/domain/usecases/build_timeline.dart | 5 | BuildTimeline.call | 3 |
| lib/features/chat/domain/usecases/send_message.dart | 13 | SendMessage.call | 2 |
| lib/features/chat/domain/entities/message.dart | 7 | Message.fromUser | 1 |

Resumo v1: {'metodos': 9, 'soma': 30, 'media': 3.3333, 'acima_de_10': 1}

| arquivo | linha | metodo | cc |
|---|---|---|---|
| lib/features/entries/domain/usecases/audit_entry.dart | 4 | AuditEntry.run | 1 |

Resumo v2: {'metodos': 10, 'soma': 31, 'media': 3.1, 'acima_de_10': 1}

## M13 — regressão (v1 → v2)

- passa em v1 e falha em v2: ['test/features/entries/domain/summarize_entries_test.dart::SummarizeEntries averages media durations to one decimal']
- apagado em v2: ['test/features/timeline/domain/build_timeline_test.dart::BuildTimeline oldest first keeps order']
- M13 = 0.2; sem apagados = 0.1; apagados = 1; segurança = 0.8

## M14 — decisões (parte D)

| ordem | id_principal | estatica | esperado |
|---|---|---|---|
| 1 | dio | True | falha |
| 2 | EntriesRepositoryImpl | True | ok |
| 3 | ChatCubit | True | falha |
| 4 | BuildTimeline | False | juiz |
| 5 | SummarizeEntries | True | ok |
| 6 | export_entries.dart | True | falha |

Excluídas: ['flutter_bloc/Clean Architecture (repete P8)', 'Tests should be written first (sem identificador)', 'docs/decisions.md (nao e lib/)', 'ClassifyEntry is reused unchanged (sem verbo de prescricao)', 'fpdart (repete P8)']

## M15 — consistência (referência `entries`)

{'referencia': 'entries', 'chat': {'C1': 2, 'C2': 1, 'C3': 1, 'C4': 3, 'total': 7, 'respeitadas': 0}, 'timeline': {'C1': 0, 'C2': 0, 'C3': 0, 'C4': 0, 'total': 0, 'respeitadas': 4}, 'M15_divergencias': 7}

## M8 / M8b

- M8: {'_nota': "Invariantes conferidos a mao: (1) classify_entry.dart:24 e a unica linha nao coberta do arquivo (ramo 'bad' sem teste); (2) arquivos de dominio sem nenhum teste ficam com 0 linhas cobertas (injecao de importa-tudo); (3) validate_entry.dart tem todas as linhas executaveis cobertas apesar de o teste nao afirmar nada (contraste com a M8b). O denominador (linhas executaveis) e o definido pela VM do Dart e NAO e derivavel a mao sem ambiguidade (ex.: construtor const com super.message conta como coberto); os totais abaixo vem da primeira execucao do modulo, apos conferencia dos invariantes.", 'v1': {'M8': 0.711111, 'linhas_executaveis': 45, 'linhas_cobertas': 32, 'testes_falharam': False, 'nao_cobertas': {'lib/features/chat/domain/entities/message.dart': [2, 7], 'lib/features/chat/domain/usecases/send_message.dart': [9, 13, 14, 15, 17], 'lib/features/entries/domain/entities/entries_failure.dart': [4], 'lib/features/entries/domain/entities/leaky_entry.dart': [4, 8], 'lib/features/entries/domain/usecases/classify_entry.dart': [24], 'lib/features/entries/domain/usecases/format_badge.dart': [4], 'lib/features/timeline/domain/entities/timeline_failure.dart': [4]}}, 'v2': {'M8': 0.695652, 'linhas_executaveis': 46, 'linhas_cobertas': 32, 'testes_falharam': True, 'nao_cobertas_adicional': {'lib/features/entries/domain/usecases/audit_entry.dart': [4]}}}
- M8b: {'_nota': 'Lista de mutantes e destino derivada a mao (analise de cada operador contra os testes de v1) ANTES de rodar o modulo; o modulo reproduziu exatamente. Mutante plantado: validate_entry.dart:5 (`<=` -> `<`), que sobrevive porque o teste cobre a linha sem afirmar nada (M8 cobre, M8b nao mata).', 'v1': {'total': 17, 'mortos': 9, 'M8b_mutation': 0.529412, 'plantado': {'arquivo': 'lib/features/entries/domain/usecases/validate_entry.dart', 'linha': 5, 'de': '<=', 'para': '<', 'estado': 'sobrevivente'}, 'lista_sobreviventes': [['lib/features/chat/domain/entities/message.dart', 7, '=='], ['lib/features/entries/domain/entities/entry.dart', 22, '== (2o)'], ['lib/features/entries/domain/usecases/classify_entry.dart', 8, '&&'], ['lib/features/entries/domain/usecases/classify_entry.dart', 8, '>'], ['lib/features/entries/domain/usecases/classify_entry.dart', 14, '>'], ['lib/features/entries/domain/usecases/summarize_entries.dart', 15, '&&'], ['lib/features/entries/domain/usecases/validate_entry.dart', 5, '&&'], ['lib/features/entries/domain/usecases/validate_entry.dart', 5, '<=']], 'n_sobreviventes': 8}}
