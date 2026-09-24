# GATE-C13 — Conferência lado a lado: requisitos (fonte PT × pacote EN)

**Como usar:** para cada bloco, leia a fonte e a tradução e marque uma das opções. Procure três coisas: (1) critério ou valor acrescentado, omitido ou alterado; (2) texto de interface que deveria ter ficado em português literal; (3) algo que revele metodologias, métricas ou o estudo. As remoções **intencionais** (linhas "Estressa", notas de histórico, ferramentas de medição) estão listadas em `gate-c13-lista-de-revisao.md`, itens 2.1–2.3, e não contam como omissão.

Fonte: `ux/Requisitos_e_Fluxo_de_Telas_TCC.md` (SHA-256 `a62d8439…3db0`). Pacote: `entrada/requirements.md`.

## 1. RF01

**Fonte (PT)**

```text
### RF01 — Captura Multimodal (texto/áudio/foto)
**Estressa:** camada de serviços / integração de device.
Entrada de dados via texto, gravação de áudio em tempo real e upload de fotografia — sempre pela Tela 2 (Modal de Inserção), que passa a ter também um campo de texto bruto, não só microfone e galeria. Toda captura aqui vira um registro persistido (`POST /entries`), **distinto de uma mensagem de chat** (ver nota de separação em RF04).
**Critérios de aceite:**
- As três modalidades (texto, áudio, foto) resultam no mesmo formato de entrada persistida — nenhuma é tratada de forma estruturalmente diferente das outras após a captura.
- Cancelar a captura no meio (ex: interromper gravação) não cria uma entrada parcial/vazia.
```

**Pacote (EN)**

```text
### RF01 — Multimodal capture (text / audio / photo)
Data entry by text, real-time audio recording and photo upload — always through Screen 2 (Insertion Modal), which has a raw text field in addition to the microphone and the gallery. Every capture becomes a persisted record (`POST /entries`), **distinct from a chat message** (see the separation note in RF04).

**Acceptance criteria:**
- The three modalities (text, audio, photo) result in the same persisted-entry format — none is treated structurally differently from the others after capture.
- Cancelling a capture midway (e.g., interrupting a recording) does not create a partial or empty entry.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 2. RF02

**Fonte (PT)**

```text
### RF02 — Processamento STT/OCR
**Estressa:** camada de serviços / integração de API externa.
Transcrição de áudio (speech-to-text) e reconhecimento de texto em imagem (OCR) sobre o conteúdo capturado no RF01.
**Critérios de aceite:** quatro estados visíveis — gravando, processando, transcrito, erro de transcrição.
```

**Pacote (EN)**

```text
### RF02 — Speech-to-text / OCR processing
Transcription of audio (speech-to-text) and recognition of text in images (OCR) over the content captured in RF01.

**Acceptance criteria:** four visible states — recording, processing, transcribed, transcription error.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 3. RF03

**Fonte (PT)**

```text
### RF03 — Cofre de Autenticação Biométrica
**Estressa:** camada de serviços / segurança.
Barreira de acesso via Face ID / Touch ID / PIN antes de expor dados do usuário.
**Critérios de aceite:**
- Falha de biometria (ex: dedo não reconhecido) oferece PIN como alternativa, sem travar o usuário fora do app.
- App em background e retomado após 5 minutos exige nova autenticação — não fica indefinidamente desbloqueado (valor fixo, não configurável pelo usuário, para manter os dois ciclos comparáveis).
```

**Pacote (EN)**

```text
### RF03 — Biometric authentication vault
Access barrier via Face ID / Touch ID / PIN before exposing the user's data.

**Acceptance criteria:**
- A biometric failure (e.g., fingerprint not recognized) offers PIN as an alternative, without locking the user out of the app.
- The app, sent to the background and resumed after 5 minutes, requires authentication again — it does not stay unlocked indefinitely (fixed value, not configurable by the user).
```

- [ ] Fiel  - [ ] Ajustar: ______

## 4. RF04

**Fonte (PT)**

```text
### RF04 — Chat Interativo com Memória (RAG)
**Estressa:** BLoC (estado assíncrono complexo) + camada de dados.
Conversa contínua com o agente de IA, com busca semântica sobre entradas anteriores. **Mensagens de chat são conversacionais e não criam entradas de diário automaticamente** — a única exceção é a ação explícita de salvar descrita no RF10. Fora isso, o chat consulta as entradas existentes via RAG, mas não escreve nelas.
**Critérios de aceite:**
- Três estados obrigatórios de UI: processando/streaming, erro, resposta completa.
- Se o streaming da resposta cair no meio, a mensagem parcial permanece visível com indicação de falha (não desaparece).
```

**Pacote (EN)**

```text
### RF04 — Interactive chat with memory (RAG)
Continuous conversation with the AI agent, with semantic search over previous entries. **Chat messages are conversational and do not create journal entries automatically** — the only exception is the explicit save action described in RF10. Otherwise, the chat queries existing entries via RAG but does not write to them.

**Acceptance criteria:**
- Three mandatory UI states: processing/streaming, error, complete response.
- If the response stream drops midway, the partial message stays visible with a failure indication (it does not disappear).
```

- [ ] Fiel  - [ ] Ajustar: ______

## 5. RF05

**Fonte (PT)**

```text
### RF05 — Exportação de Resumo Pessoal
*(Renomeado — anteriormente "Relatórios Clínicos"; removida a conotação médica/diagnóstica, fora do escopo do projeto.)*
**Estressa:** camada de serviços / permissões de sistema.
Geração de um resumo narrativo por IA (Claude Haiku 4.5) a partir das entradas do usuário, exportável em PDF, com opção adicional de baixar os dados brutos sem narrativa. **Escopo medido: geração do job, download do arquivo e tratamento de falha — nunca a qualidade do texto narrativo gerado.**
**Critérios de aceite:**
- Job de exportação com zero entradas no período retorna um estado de erro tratado (não um PDF vazio nem crash).
- Falha na geração do texto narrativo (timeout do modelo) ainda permite baixar os dados brutos sem narrativa — a exportação não fica bloqueada por uma falha de IA.
```

**Pacote (EN)**

```text
### RF05 — Personal summary export
Generation of a narrative summary by AI (Claude Haiku 4.5) from the user's entries, exportable as PDF, with an additional option to download the raw data without the narrative. No clinical or diagnostic connotation. **Scope: job generation, file download and failure handling — never the quality of the generated narrative text.**

**Acceptance criteria:**
- An export job with zero entries in the period returns a handled error state (not an empty PDF, not a crash).
- A failure generating the narrative text (model timeout) still allows downloading the raw data without the narrative — the export is not blocked by an AI failure.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 6. RF06

**Fonte (PT)**

```text
### RF06 — Busca Semântica/Filtro sobre Entradas do Diário
**Estressa:** BLoC + camada de dados / offline.
Busca por similaridade semântica (via embeddings Voyage AI, reaproveitando os já gerados no RF01) combinada com filtros de metadado (data, tipo de entrada). *(Correção em 10/09/2026 — a versão anterior deste requisito também citava "categoria" como dimensão de filtro; o backend real não implementa filtro por tag/categoria em nenhum endpoint — `GET /entries`/`GET /entries/search` só aceitam `source` e `dateFrom`/`dateTo`. Consistente com a Seção 2: a categorização é "tags manuais" e não recebe implementação funcional em nenhum dos dois ciclos — tags só aparecem embutidas, para leitura, no objeto `Entry`.)*
**Critérios de aceite:**
- Busca por um termo encontra entradas relacionadas semanticamente mesmo sem a palavra exata (ex: buscar "ansiedade" retorna uma entrada que só menciona "nervosismo", sem o termo literal).
- Debounce de busca de 300ms: digitação rápida dispara uma única consulta, não uma por tecla.
- Resultado do cache local de leitura permanece consistente com o servidor após reconexão, sem duplicar itens exibidos *(ajustado — arquitetura é cloud-only; offline permite apenas visualização de dados já cacheados, não escrita)*.
- Dois ou mais filtros aplicados simultaneamente (`source`+`dateFrom`/`dateTo`) restringem com lógica E (não OU).
- Limpar filtros retorna à lista completa sem reiniciar a tela.
```

**Pacote (EN)**

```text
### RF06 — Semantic search / filter over journal entries
Semantic similarity search (via Voyage AI embeddings, reusing the ones already generated in RF01) combined with metadata filters (date, entry type). There is no filter by tag or category: the backend does not implement it in any endpoint — `GET /entries` and `GET /entries/search` accept only `source` and `dateFrom`/`dateTo`. Tags appear only embedded, read-only, in the `Entry` object (see section 2).

**Acceptance criteria:**
- Searching for a term finds semantically related entries even without the exact word (e.g., searching "ansiedade" returns an entry that only mentions "nervosismo", without the literal term).
- 300 ms search debounce: fast typing triggers a single query, not one per keystroke.
- Results from the local read cache stay consistent with the server after reconnection, without duplicating displayed items *(the architecture is cloud-only; offline allows only viewing already-cached data, not writing)*.
- Two or more filters applied at the same time (`source` + `dateFrom`/`dateTo`) narrow results with AND logic (not OR).
- Clearing the filters returns to the full list without restarting the screen.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 7. RF07

**Fonte (PT)**

```text
### RF07 — Histórico Multi-fonte (Timeline)
**Estressa:** composição de múltiplos BLoCs.
Tela cujo estado depende simultaneamente de autenticação, status de sincronização e dados das entradas.
**Critérios de aceite:**
- Expiração de sessão durante visualização dispara prompt de novo login sem crash e sem perder a posição de scroll.
- Badge de status de sincronização por entrada atualiza independentemente da stream de autenticação.
- Nenhum BLoC importa outro BLoC diretamente (checável via revisão de imports ou extensão do lint de arquitetura do RNF06).
```

**Pacote (EN)**

```text
### RF07 — Multi-source history (timeline)
A screen whose state depends simultaneously on authentication, synchronization status and entry data.

**Acceptance criteria:**
- Session expiration while viewing triggers a new-login prompt without a crash and without losing the scroll position.
- The per-entry synchronization status badge updates independently of the authentication stream.
- No BLoC imports another BLoC directly.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 8. RF08

**Fonte (PT)**

```text
### RF08 — Insights Proativos (mecanismo)
**Estressa:** isolamento de falha / concorrência.
Sugestão inserida no chat sem o usuário pedir. **Escopo medido: apenas o mecanismo de disparo, nunca a qualidade do texto gerado.**
**Critérios de aceite:**
- Gatilho após N=5 mensagens do usuário OU T=2min de inatividade — dispara exatamente uma vez por condição satisfeita.
- Se a geração do insight falhar (timeout/erro de rede), o chat principal continua funcionando normalmente.
- Descartar o insight não altera scroll nem estado da conversa principal.
```

**Pacote (EN)**

```text
### RF08 — Proactive insights (mechanism)
A suggestion inserted into the chat without the user asking for it. **Scope: only the trigger mechanism, never the quality of the generated text.**

**Acceptance criteria:**
- Trigger after N = 5 user messages OR T = 2 min of inactivity — fires exactly once per satisfied condition.
- If insight generation fails (timeout / network error), the main chat keeps working normally.
- Dismissing the insight does not change the scroll position or the state of the main conversation.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 9. RF09

**Fonte (PT)**

```text
### RF09 — Resumos Temporais / Dashboard
**Estressa:** agregação de dados + visualização.
Gráfico de evolução com balanço textual, computado sob demanda ao abrir a aba de Configurações. **Escopo medido: agregação e renderização, nunca a qualidade do texto narrativo.**
**Critérios de aceite:**
- Renderiza corretamente em três cenários: zero entradas, uma entrada, >30 entradas.
- Agregação recalcula corretamente após criar uma entrada (teste de invalidação de cache). *(Correção em 10/09/2026 — a versão anterior também citava "editar/apagar uma entrada"; entradas são imutáveis por decisão de arquitetura, D3 — "conteúdo original íntegro, nunca censurado". Não existe `PATCH /entries/:id` nem `DELETE /entries/:id` no backend real, e nenhuma tela deste documento descreve uma ação de editar/apagar entrada — o texto anterior não correspondia a nenhuma interação de fato prevista.)*
- Texto narrativo da IA só é checado quanto a não quebrar a UI em casos extremos — nunca quanto ao conteúdo.
```

**Pacote (EN)**

```text
### RF09 — Temporal summaries / dashboard
An evolution chart with a textual summary, computed on demand when the Settings tab is opened. **Scope: aggregation and rendering, never the quality of the narrative text.**

**Acceptance criteria:**
- Renders correctly in three scenarios: zero entries, one entry, more than 30 entries.
- The aggregation recalculates correctly after an entry is created (cache-invalidation test). Entries are immutable: there is no `PATCH /entries/:id` or `DELETE /entries/:id` in the backend, and no screen describes an edit or delete action on an entry.
- The AI narrative text is checked only for not breaking the UI in extreme cases — never for its content.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 10. RF10

**Fonte (PT)**

```text
### RF10 — Salvar Mensagem do Chat como Entrada
**Estressa:** comunicação entre features dentro da Clean Architecture (o chat precisa acionar a criação de uma entrada sem depender diretamente da camada de dados do RF01).
Botão em cada mensagem do usuário no chat que a converte numa entrada persistida — para os momentos em que o usuário insere um dado relevante durante a conversa, não só via captura dedicada (RF01). Reaproveita o mesmo pipeline de `POST /entries` (checagem de PII + embedding), com a origem marcada como `chat`.
**Critérios de aceite:**
- A feature de chat aciona a criação da entrada através de uma interface/caso de uso compartilhado, nunca importando diretamente um repositório ou datasource da feature de entradas — violação aqui conta para o RNF06.
- Salvar a mesma mensagem duas vezes não cria entradas duplicadas (idempotência).
- Falha ao salvar (rede indisponível) mantém a conversa funcionando normalmente e o botão retorna a um estado que permite tentar de novo — mesmo padrão de isolamento de falha do RF08.
- Só mensagens do usuário têm o botão — respostas da IA não podem virar entrada.
```

**Pacote (EN)**

```text
### RF10 — Save a chat message as an entry
A button on each user message in the chat that converts it into a persisted entry — for moments when the user states relevant information during the conversation, not only through dedicated capture (RF01). It reuses the same `POST /entries` pipeline (PII check + embedding), with the origin marked as `chat`.

**Acceptance criteria:**
- The chat feature triggers the creation of the entry through a shared interface / use case, never by directly importing a repository or data source of the entries feature — a violation here also breaks RNF06.
- Saving the same message twice does not create duplicate entries (idempotency).
- A failure to save (network unavailable) keeps the conversation working normally, and the button returns to a state that allows trying again — the same failure-isolation pattern as RF08.
- Only user messages have the button — AI responses cannot become entries.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 11. Extensões (§2 → section 2)

**Fonte (PT)**

```text
## 2. Requisitos Funcionais — Extensão de Produto
 
Mantêm a "essência" do fluxo original e existem no protótipo do Claude Design, mas **não recebem implementação funcional em nenhum dos dois ciclos comparativos** — ficam como trabalho futuro na monografia.
 
| Requisito original | Tratamento na versão atual |
|---|---|
| Categorização Dinâmica (IA) | Simplificada para tags manuais criadas pelo usuário (tela Meus Registros) |
| Extração Autônoma de Metas | Tela Planos de Ação — estática, sem lógica |
| Ajuste Dinâmico de Persona | Toggle cosmético simples (Configurações), baixo custo de manter |
```

**Pacote (EN)**

```text
## 2. Extension features — not implemented

They keep the "essence" of the original product flow and exist in the prototype, but **receive no functional implementation**. A menu entry may exist as a placeholder.

| Original feature | Treatment in the current version |
|---|---|
| Dynamic categorization (AI) | Simplified to manual tags created by the user (My Records screen) |
| Autonomous goal extraction | Action Plans screen — static, no logic |
| Dynamic persona adjustment | Simple cosmetic toggle (Settings) |
```

- [ ] Fiel  - [ ] Ajustar: ______

## 12. Requisitos de qualidade (§3 → section 3)

**Fonte (PT)**

```text
## 3. Requisitos Não Funcionais — Núcleo Mensurável (automatizáveis)
 
| ID | Requisito | Ferramenta / mecânica | Meta |
|---|---|---|---|
| RNF06 | Zero Violações de Camada | Lint de arquitetura (`clean_architecture_kit` ou `import_linter`) — domínio não pode importar `package:flutter` nem classes de `data/` | 0 violações |
| RNF07 | Cobertura Mínima de Testes | `flutter test --coverage` + `very_good_coverage`, filtrado para `lib/**/domain/**` | ≥80% |
| RNF08 | Fidelidade Visual ao Protótipo | Rubrica de 3 pontos por tela (cor primária bate o hex do protótipo / tipografia bate família+tamanho / espaçamento dentro de ±4dp) + check estático de valores hardcoded fora do arquivo central `design_tokens.dart` | Score 0–3 por tela + 0 hardcodes |
| RNF09 | Tratamento de Erro de Rede Consistente | Padrão `Either<Failure, T>` via `fpdart`; check estático de assinaturas de repositório + testes com `mocktail` simulando falhas em todos os endpoints de escrita (5 endpoints × 3 tipos de falha — timeout, resposta malformada, sem conexão) | 0 assinaturas fora do padrão / 15 de 15 cenários tratados |
```

**Pacote (EN)**

```text
## 3. Quality requirements

| ID | Requirement | Target |
|---|---|---|
| RNF06 | Zero layer violations — the domain layer does not import `package:flutter` nor classes from `data/` | 0 violations |
| RNF07 | Minimum test coverage of the domain layer (`lib/**/domain/**`) | ≥ 80% |
| RNF08 | Visual fidelity to the prototype — primary colors match the prototype's hex values, typography matches family and size, spacing matches the prototype; no visual value hardcoded outside the central file `design_tokens.dart` | Every screen faithful in color, typography and spacing; 0 hardcoded values |
| RNF09 | Consistent network-error handling — `Either<Failure, T>` pattern via `fpdart` in every repository; every write endpoint (5 endpoints) handles three failure types — timeout, malformed response, no connection — covered by tests with `mocktail` | 0 repository signatures outside the pattern; 15 of 15 scenarios handled |
```

- [ ] Fiel  - [ ] Ajustar: ______

## 13. Outros RNF e limitação (§4 → section 4)

**Fonte (PT)**

```text
## 4. Requisitos Não Funcionais — Higiene (não comparativos)
 
RNF01 — Latência de Interação (ação local reflete na UI em <100ms; qualquer chamada de rede acima de 300ms exibe indicador de carregamento) · RNF02 — PII Stripping (via Claude Haiku 4.5 com prompt estruturado/tool use, não um modelo de NER dedicado) · RNF03 — Zero Data Retention · RNF04 — RLS (Row Level Security) · RNF05 — Hard Delete de Conta/Dados (LGPD)
 
**Limitação consciente:** o sistema não possui protocolo de detecção/resposta a sinais de risco (ideação suicida, autolesão) em entradas ou mensagens de chat. Como o produto não é mais enquadrado como app de saúde mental, essa ausência é uma decisão de escopo explícita — vale registrá-la como limitação reconhecida na monografia, não como lacuna esquecida.
```

**Pacote (EN)**

```text
## 4. Other non-functional requirements

RNF01 — Interaction latency (a local action is reflected in the UI in < 100 ms; any network call above 300 ms shows a loading indicator) · RNF02 — PII stripping (via Claude Haiku 4.5 with a structured prompt / tool use, not a dedicated NER model) · RNF03 — Zero data retention · RNF04 — RLS (Row Level Security) · RNF05 — Hard delete of account and data (LGPD).

**Known limitation:** the system has no protocol for detecting or responding to risk signals (suicidal ideation, self-harm) in entries or chat messages. Since the product is not framed as a mental-health app, this absence is an explicit scope decision.
```

- [ ] Fiel  - [ ] Ajustar: ______

## 14. Telas (§5.2 → 5.2)

**Fonte (PT)**

```text
### 5.2 Telas
 
**Tela 0 — Splash Screen:** carregamento inicial; verifica conexão e sincroniza cache em background. *Conecta a: RF06, RNF01.*
 
**Tela 0.1 — Cofre de Autenticação:** barreira biométrica/PIN antes do acesso. *Conecta a: RF03.*
 
**Tela 1 — Home (Chat):** tela principal, conversa contínua, botão "+" para entrada multimodal, indicador de estado da IA, botão "salvar no diário" em cada mensagem do usuário. *Conecta a: RF04, RF08, RF10, RNF01, RNF09.*
 
**Tela 2 — Modal de Inserção:** overlay com três formas de captura — campo de texto bruto, microfone (áudio) e galeria/câmera (foto) — com indicador de transcrição. Toda captura aqui cria uma entrada persistida, nunca uma mensagem de chat. *Conecta a: RF01, RF02.*
 
**Tela 3 — Menu Lateral (Sidebar):** hub de navegação, histórico de sessões, acesso a Meus Registros/Planos de Ação/Configurações. Deverá ganhar um botão "Novo Chat" (pendência aberta em 10/09/2026, ver Seção 13.1) que leva à Tela 1 em estado vazio. *Conecta a: RF04 (via botão "Novo Chat"); demais itens são navegação pura.*
 
**Tela 4 — Meus Registros:** timeline consolidada, filtros, tags manuais, exportação. *Conecta a: RF07, RF06, RF05; extensão de categorização.*
 
**Tela 5 — Planos de Ação:** painel Kanban simples (colunas "A Fazer" / "Em Andamento" / "Concluído") com cards estáticos de exemplo. *(Extensão — existe visualmente no protótipo do Claude Design para completude da demo, mas sem lógica funcional em nenhum dos dois ciclos comparativos.)*
 
**Tela 6 — Configurações e Perfil:** dashboard de evolução, seletor de persona — "Analítico" / "Empático" / "Socrático" (extensão, só troca a string do system prompt do RF04), apagar conta. *Conecta a: RF09, RNF05; extensão de persona.*
```

**Pacote (EN)**

```text
### 5.2 Screens

**Screen 0 — Splash:** initial loading; checks the connection and syncs the cache in the background. *Connects to: RF06, RNF01.*

**Screen 0.1 — Authentication vault:** biometric/PIN barrier before access. *Connects to: RF03.*

**Screen 1 — Home (chat):** main screen, continuous conversation, "+" button for multimodal input, AI status indicator, "save to journal" button on each user message. *Connects to: RF04, RF08, RF10, RNF01, RNF09.*

**Screen 2 — Insertion Modal:** overlay with three ways to capture — raw text field, microphone (audio) and gallery/camera (photo) — with a transcription indicator. Every capture here creates a persisted entry, never a chat message. *Connects to: RF01, RF02.*

**Screen 3 — Side menu (sidebar):** navigation hub, session history, access to My Records / Action Plans / Settings, and a "Novo Chat" button that opens Screen 1 in its empty state. *Connects to: RF04 (via the "Novo Chat" button); the other items are pure navigation.*

**Screen 4 — My Records:** consolidated timeline, filters, manual tags (extension, section 2), export. *Connects to: RF07, RF06, RF05.*

**Screen 5 — Action Plans:** simple Kanban board (columns "A Fazer" / "Em Andamento" / "Concluído") with static example cards. *(Extension — section 2.)*

**Screen 6 — Settings and profile:** evolution dashboard, persona selector — "Analítico" / "Empático" / "Socrático" (extension, section 2; it would only change the system-prompt string of RF04), delete account. *Connects to: RF09, RNF05.*
```

- [ ] Fiel  - [ ] Ajustar: ______

## 15. Parâmetros (§11 → section 10)

**Fonte (PT)**

```text
## 11. Parâmetros de Configuração (fixados para reprodutibilidade entre ciclos)
 
Valores travados propositalmente — nenhum dos dois ciclos deve reinterpretar esses números, senão a comparação deixa de ser justa.
 
| Parâmetro | Valor | Requisito |
|---|---|---|
| Timeout de sessão em background | 5 min | RF03 |
| Debounce de busca | 300ms | RF06 |
| Gatilho de insight proativo | 5 mensagens OU 2 min de inatividade | RF08 |
| Cenários de renderização do dashboard | 0 / 1 / >30 entradas | RF09 |
| Cobertura mínima de testes (domínio) | ≥80% | RNF07 |
| Limiar de complexidade ciclomática | >10 por método | Seção 8.2 |
| Latência de UI local | <100ms | RNF01 |
| Limiar de indicador de carregamento | >300ms | RNF01 |
| Cenários de erro de rede testados | 5 endpoints × 3 falhas = 15 | RNF09 |
| Decisões de plano checadas (fidelidade de handoff) | 8–10 | Seção 8.3 |
```

**Pacote (EN)**

```text
## 10. Configuration parameters

Fixed values — not to be reinterpreted.

| Parameter | Value | Requirement |
|---|---|---|
| Background session timeout | 5 min | RF03 |
| Search debounce | 300 ms | RF06 |
| Proactive insight trigger | 5 messages OR 2 min of inactivity | RF08 |
| Dashboard rendering scenarios | 0 / 1 / > 30 entries | RF09 |
| Minimum test coverage (domain) | ≥ 80% | RNF07 |
| Local UI latency | < 100 ms | RNF01 |
| Loading-indicator threshold | > 300 ms | RNF01 |
| Network-error scenarios tested | 5 endpoints × 3 failures = 15 | RNF09 |
```

- [ ] Fiel  - [ ] Ajustar: ______

## 16. Códigos de erro (§12 → section 11)

**Fonte (PT)**

```text
## 12. Taxonomia de Códigos de Erro (RNF09)
 
Todo endpoint retorna `{ code, message, retryable }`. Códigos mínimos a implementar nos dois ciclos, para manter o contrato idêntico:
 
| Código | Situação | `retryable` |
|---|---|---|
| `AUTH_EXPIRED` | Sessão expirada, precisa reautenticar | não |
| `AUTH_INVALID` | Credenciais/biometria inválidas | não |
| `NETWORK_TIMEOUT` | Requisição excedeu o tempo limite | sim |
| `NETWORK_OFFLINE` | Sem conexão — ação bloqueada (ver RF04/RF06) | sim |
| `VALIDATION_ERROR` | Corpo da requisição malformado | não |
| `PII_CHECK_FAILED` | Checagem de PII falhou antes de persistir | sim |
| `EMBEDDING_FAILED` | Voyage AI indisponível/erro | sim |
| `AI_GENERATION_TIMEOUT` | Claude não respondeu a tempo (chat/insight/resumo/dashboard) | sim |
| `NOT_FOUND` | Recurso não existe ou não pertence ao usuário | não |
| `RATE_LIMITED` | Limite de requisições excedido | sim |
```

**Pacote (EN)**

```text
## 11. Error codes (RNF09)

Every endpoint returns `{ code, message, retryable }`. Minimum codes the app handles:

| Code | Situation | `retryable` |
|---|---|---|
| `AUTH_EXPIRED` | Session expired, re-authentication needed | no |
| `AUTH_INVALID` | Invalid credentials / biometrics | no |
| `NETWORK_TIMEOUT` | Request exceeded the time limit | yes |
| `NETWORK_OFFLINE` | No connection — action blocked (see RF04/RF06) | yes |
| `VALIDATION_ERROR` | Malformed request body | no |
| `PII_CHECK_FAILED` | PII check failed before persisting | yes |
| `EMBEDDING_FAILED` | Voyage AI unavailable / error | yes |
| `AI_GENERATION_TIMEOUT` | Claude did not respond in time (chat/insight/summary/dashboard) | yes |
| `NOT_FOUND` | Resource does not exist or does not belong to the user | no |
| `RATE_LIMITED` | Request limit exceeded | yes |

The complete, closed list of the backend's 13 codes, with HTTP statuses, is in `docs/input/backend/error-taxonomy.md`.
```

- [ ] Fiel  - [ ] Ajustar: ______

## Depois da leitura

Se tudo estiver fiel, responda "C13 requisitos: fiel". Se algo precisar de ajuste, cole o número do bloco e o que mudar — eu corrijo o pacote antes dos hashes.