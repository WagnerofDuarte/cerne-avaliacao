# Ficha de validação humana do juiz (cega)

Objetivo: conferir, sem ver o voto do juiz, uma amostra das respostas do avaliador Claude (D-099). **Não abra `dados/produto/validacao-chave.json`** até terminar. Responda com **sim / não / parcial** e, se quiser, uma frase. Tempo estimado: 25 a 35 minutos. Se faltar tempo, responda só a Parte 1 (≈10 min).

## Parte 1 — M14: a decisão de arquitetura está implementada?

Repositório: `cerne-ciclo-b`, tag `cicloB/final`. A decisão vem do documento de arquitetura do ciclo. Pergunta: **o código em `lib/` na tag final respeita esta decisão?**

**P1.1.** Only `data/` imports `dio`/`hive_ce`/platform plugins.

Resposta: ____  Observação: ____

**P1.2.** **Rule:** retry logic is implemented once (the `dio` interceptor / `ApiClient` wrapper), fires only for the 6 server `retryable:true` codes (`NETWORK_TIMEOUT`, `NETWORK_OFFLINE`, `PII_CHECK_FAILED`, `EMBEDDING_FAILED`, `AI_GENERATION_TIMEOUT`, `RATE_LIMITED`).

Resposta: ____  Observação: ____

**P1.3.** **Prevents:** F000 and RF03 each building an independent navigation gate (two competing `redirect` callbacks, or RF03 bolting a second check onto screens individually) — `go_router` supports only one top-level `redirect`, so two independently-built gates cannot both "just work."

Resposta: ____  Observação: ____

**P1.4.** **Integration spike flagged, not yet run:** `dio` + `flutter_secure_storage` + `get_it` have not been verified working together in one scaffold (each is independently current per the Stack table, but their combination at F000's bootstrap time is unverified).

Resposta: ____  Observação: ____

## Parte 2 — M6: a divergência entre plano e código é real?

Cada item abaixo é uma divergência apontada pelo juiz entre o plano da unidade e o diff da unidade (texto em inglês, como o juiz escreveu). Pergunta: **(a)** a divergência existe no código (sim/não/parcial)? **(b)** ela estava documentada ou justificada no próprio plano ou em outro documento do repositório (sim/não)?

**P2.1.** Repositório `cerne-ciclo-a`, unidade **RF03** (tags `cicloA/…`). 
> A wrong PIN only keeps an error that was already there. In PIN-only mode, which starts with no error, a wrong PIN just clears the digits with no message. The spec requires an inline error on incorrect attempts.
> Evidências citadas: `lib/features/vault/presentation/bloc/vault_bloc.dart:192`

(a) Existe? ____  (b) Documentada? ____

**P2.2.** Repositório `cerne-ciclo-a`, unidade **RF06** (tags `cicloA/…`). 
> The filter sheet has no "Limpar" button. FR-003, T024 and Story 2 Acceptance Scenario 3 require one that resets the sheet's own selections without closing it. Only "Aplicar" exists, and the test checks that "Limpar" is absent.
> Evidências citadas: `lib/features/records/presentation/widgets/filter_sheet.dart:82-91`, `test/features/records/presentation/widgets/filter_sheet_test.dart:84-88`

(a) Existe? ____  (b) Documentada? ____

**P2.3.** Repositório `cerne-ciclo-b`, unidade **RF05** (tags `cicloB/…`). 
> An app-wide pt_BR locale and localization delegates were added to MaterialApp.router so showDateRangePicker renders in Portuguese. No spec-7-1 task asked for this; it was added during review.
> Evidências citadas: `lib/main.dart:161`

(a) Existe? ____  (b) Documentada? ____

**P2.4.** Repositório `cerne-ciclo-b`, unidade **RF06** (tags `cicloB/…`). 
> Active-filter chips use a colorSecondaryTint fill and radiusSm corners instead of the planned colorSecondary/colorCategoryChipText/radiusFull pill. The selected chip inside the filter sheet uses colorPrimary/colorOnPrimary.
> Evidências citadas: `lib/features/entries/presentation/screens/meus_registros_screen.dart:783`, `lib/features/entries/presentation/screens/meus_registros_screen.dart:789`, `lib/features/entries/presentation/screens/meus_registros_screen.dart:791`, `lib/features/entries/presentation/widgets/entries_filter_sheet.dart:292`

(a) Existe? ____  (b) Documentada? ____

**P2.5.** Repositório `cerne-ciclo-b`, unidade **RF04** (tags `cicloB/…`). 
> No plan asks for it, but the 'Meus Registros' drawer nav icon changes from Icons.menu_book_outlined to Icons.note_outlined. This is a visible UI change.
> Evidências citadas: `lib/core/widgets/app_drawer.dart:126`

(a) Existe? ____  (b) Documentada? ____

**P2.6.** Repositório `cerne-ciclo-a`, unidade **RF02** (tags `cicloA/…`). 
> T001 says to add sizePhotoThumbnail = 64. The diff sets it to 56 and adds three tokens the plan never lists: sizePhotoThumbnailWideWidth, sizePhotoThumbnailWideHeight and valueLoadingIndicatorArc. The plan's Scale/Scope says only two new tokens.
> Evidências citadas: `lib/core/design_tokens.dart:128`, `lib/core/design_tokens.dart:129`, `lib/core/design_tokens.dart:130`, `lib/core/design_tokens.dart:118`

(a) Existe? ____  (b) Documentada? ____

---

## Respostas e resultado (08/11/2026)

**Procedimento (D-111).** As respostas foram elaboradas pelo assistente de apoio (Claude Sonnet 5.5) a partir da leitura dos repositórios, sem acesso a `dados/produto/validacao-chave.json`, e apresentadas ao pesquisador, que as aceitou integralmente ("Concordo com todas") e delegou ao assistente quatro pontos de julgamento, decididos pelos critérios das rubricas (M14: "parcial" quando a decisão é seguida em parte do código aplicável; M6: comentário no código não conta como documentação).

| Item | Resposta validada |
|---|---|
| P1.1 | parcial (10 arquivos fora de `data/` importam dio, hive_ce e plugins: `core/di`, `core/network` e 4 `*_injection.dart`; `domain/` e `presentation/` estão limpos) |
| P1.2 | sim |
| P1.3 | sim |
| P1.4 | sim |
| P2.1 | existe: sim; documentada: não |
| P2.2 | existe: sim; documentada: não |
| P2.3 | existe: sim; documentada: sim |
| P2.4 | existe: sim; documentada: não |
| P2.5 | existe: sim; documentada: não (só comentário no código) |
| P2.6 | existe: sim; documentada: não |

**Concordância com o juiz (aberta a chave depois das respostas):** M14, 4 de 4 (κ = 1,00); M6 existência, 6 de 6 (κ indefinido: uma única categoria); M6 documentada, 6 de 6 (κ = 1,00). No total, 16 de 16 classificações concordantes (limite inferior unilateral de 95%: 0,79). Dados em `dados/produto/validacao-resultado.json`.

**Ressalvas.** O segundo avaliador é da mesma família do juiz e o aceite do pesquisador não é classificação independente; a amostra tem 10 itens (abaixo dos 20 por medida da seção 3.6.4); a M6 mede só a precisão das divergências apontadas, não as omitidas; a M14 do Ciclo A foi verificada só de forma estática.
