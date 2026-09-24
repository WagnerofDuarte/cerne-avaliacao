# Suíte hold-out — cenários dos critérios de aceite (RF01–RF10)

**Destino:** `cerne-avaliacao/holdout/cenarios.md` · **Tarefa:** `C-018` · **Versão:** 23/09/2026
**Fonte dos critérios:** `entrada/requirements.md`, seção 1 (tradução dos requisitos reconciliados `a62d8439…3db0`).
**Uso:** métricas M11 (critérios de aceite, só na tag `final`) e parte da M10. Implementação em Maestro + mitmproxy + SQL na trilha paralela (`H-005`), testada só no repositório de calibração. Este arquivo **nunca** entra num repositório de ciclo.

---

## 0. Condições gerais

**Ambiente.** Build da tag `final` do ciclo numa cópia temporária, com o `.env` do ciclo; simulador de avaliação (`sim-eval`, modelo da P11); backend do ciclo em `replay_strict`, com o cache de IA preparado conforme o `GATE-C19`.

**Reset.** O banco é resetado e populado com o seed congelado **uma única vez**, antes do início da suíte inteira (não antes de cada bloco) — todo reset, aqui ou em qualquer ponto, passa sempre por `scripts/reset-ambiente`, que reimporta o cache congelado automaticamente (`C-015`); um `db reset` isolado apagaria o cache. A ordem dos blocos (I → II → III) evita a necessidade de resets no meio, porque nenhum bloco depende de um estado que um bloco anterior tenha alterado de forma incompatível — ver a nota de cada bloco.

**Proxy (mitmproxy) em todas as requisições do app:**
- acrescenta `X-Test-Key: <TEST_FAULT_KEY>` (lido de `segredos/`) e `X-Test-Now: 2026-09-23T09:41:00Z` — a âncora do seed, para que janelas relativas do backend (ex.: `period=30d`) caiam sempre sobre os dados semeados;
- registra método, função (`x-cerne-function`), parâmetros e horário de cada chamada (asserções "proxy");
- injeta falhas só onde o cenário manda: por cabeçalho `X-Test-Fault` (`timeout`, `malformed`, `offline`, `ai_timeout`) — efeito executado pelo próprio backend e registrado em `experiment.fault_injection_log` — ou por manipulação direta do tráfego (corte de stream SSE, reescrita de resposta, resposta `401` forjada).

**Relógio do aparelho.** Não é congelado: timers do app (RF03, RF08) usam tempo real, e filtros de data calculados no aparelho usam a data real da execução. Por isso o cenário de filtros por data (H06-4) usa entradas criadas na própria execução.

**Contas do seed** (senha em `segredos/`): **A** `cenario-cheio@cerne.test` (34 entradas, 3 sessões de chat, 4 tags) · **B** `cenario-uma@cerne.test` (1 entrada) · **C** `cenario-vazio@cerne.test` (0 entradas).

**Textos literais** das mensagens e entradas novas: chaves de `holdout/fixtures/textos.json` (cópia do handoff, fora do pacote de entrada), idênticos nos dois ciclos. Mídia: `entrada/backend/fixtures/media/`.

**Identificação de elementos.** Por **texto visível do protótipo** (ex.: "Salvar", "Meus Registros"). Elementos sem texto (☰, "+", marcador de mensagem, ícones de download e funil) são identificados pela **posição no frame do protótipo** (coordenadas relativas ao frame de 390×844), iguais para os dois ciclos. Se um texto do app diferir do protótipo, o passo falha — a falha é registrada no cenário, com a divergência de texto anotada à parte (ela também é dado da M9).

**Passos específicos do app.** Onde o protótipo não define o fluxo (ex.: onde o usuário cadastra o PIN), o passo é escrito por ciclo e anotado como "específico do app". Se o fluxo não existir no app, o critério é marcado "não verificável", com justificativa.

**Ordem obrigatória (cache de replay).** Chamadas de IA cuja impressão digital depende de ids do banco (chat, insight, busca, dashboard, exportação) vêm **antes** de qualquer criação de entrada nova na conta A. Por isso os cenários rodam em blocos:
1. **Bloco I — conta A, sem escrita:** H04-1, H08-1, H04-2, H08-3, H08-4, H10-4, H08-2, F13–F15 (`rnf09.md`), H06-1, H06-2, H06-3, H07-1, H09-1 (A), H05-2.
2. **Bloco II — contas B e C:** H05-1 (C), H09-1 (B, C), H09-2 (B), H09-3 (B).
3. **Bloco III — conta A, com escrita:** H03-1, H03-2, H01-2, H01-1, H02-1, H06-4, H06-5, H10-2, H10-3.
4. **Estruturais (análise estática sobre a tag `final`):** H07-2, H07-3, H10-1.

**Resultado por cenário:** `passou` · `falhou` · `não verificável` (com justificativa). A M11 por RF = cenários que passaram ÷ cenários verificáveis do RF.

---

## RF01 — Captura multimodal

**H01-1 — As três modalidades resultam no mesmo formato de entrada**
- Conta A, Bloco III. Pré: `ocr_fixture_01.png` adicionado à galeria (`xcrun simctl addmedia`); `audio_fixture_01.wav` roteado como entrada de microfone do simulador (dispositivo de áudio virtual no Mac).
- Passos: Home → "+" → "Texto" → digitar `entrada_manual_nova` → "Salvar". "+" → "Áudio" → gravar enquanto o fixture toca → parar → aguardar o texto transcrito → "Salvar". "+" → "Foto" → "Galeria" → escolher a imagem → aguardar o texto reconhecido → "Salvar".
- Asserção (SQL + proxy): três linhas novas em `entries` da conta A, com `source` `manual`, `audio` e `photo`; nas três, o mesmo conjunto de colunas preenchidas (`content` não vazio, `embedding` não nulo, `chat_message_id` nulo); três chamadas `entries-create` com o mesmo formato de corpo, variando só `source` e `content`.
- Natureza: comportamental.

**H01-2 — Cancelar a captura no meio não cria entrada**
- Conta A, Bloco III.
- Passos: "+" → "Áudio" → gravar 3 s → fechar o modal ("x") sem parar a gravação.
- Asserção: nenhuma chamada `entries-create` no intervalo (proxy); contagem de `entries` da conta A inalterada (SQL); nenhuma entrada nova em "Meus Registros" (UI).
- Natureza: comportamental.

## RF02 — Processamento STT/OCR

**H02-1 — Quatro estados visíveis: gravando, processando, transcrito, erro**
- Conta A, Bloco III (os três primeiros estados são observados durante H01-1).
- Passos e asserções (UI, texto do protótipo):
  - gravando: cronômetro correndo na aba "Áudio";
  - processando: "Transcrevendo..." depois de parar;
  - transcrito: texto editável com a duração do áudio;
  - erro de transcrição: nova gravação de 2 s de **silêncio** (entrada de áudio mudada) → "Não foi possível transcrever" com "Tentar novamente";
  - complemento OCR: "Galeria" com `ocr_fixture_ilegivel.png` → "Reconhecendo texto..." → "Não foi possível reconhecer o texto", com "Tentar novamente" e "Salvar só a foto".
- **Ambiguidade registrada:** o critério não diz o que provoca o erro de transcrição; o silêncio é o gatilho adotado, igual nos dois ciclos. Se o app aceitar transcrição vazia como sucesso, o cenário falha.
- Natureza: comportamental.

## RF03 — Cofre de autenticação biométrica

**H03-1 — Falha biométrica oferece PIN, sem trancar o usuário fora**
- Conta A, Bloco III. Pré: Face ID cadastrado no simulador; PIN cadastrado pelo fluxo do próprio app (passo específico do app).
- Passos: bloquear o app → na tela "Toque para desbloquear", tocar e simular rosto não reconhecido (notificação de *non-matching* do simulador) → digitar o PIN.
- Asserção (UI): aparece "Não foi possível reconhecer — digite seu PIN" com o teclado numérico; depois do PIN, Home/Chat.
- Natureza: comportamental.

**H03-2 — Após 5 min em background, o app exige autenticação de novo**
- Conta A, Bloco III.
- Passos: com o app desbloqueado na Home, enviar para o background; esperar 5 min 10 s (tempo real); trazer de volta.
- Asserção (UI): tela "Toque para desbloquear" (ou PIN), não a Home.
- Natureza: comportamental.

## RF04 — Chat com memória (RAG)

**H04-1 — Três estados: processando/streaming, erro, resposta completa**
- Conta A, Bloco I.
- Passos: ☰ → "CONVERSAS" → "Conversa sobre o dia no trabalho" → enviar `sessao1_quinta_mensagem`. Depois, enviar uma nova mensagem com `X-Test-Fault: ai_timeout` na chamada `chat-messages-send`.
- Asserção: (a) streaming — capturas sucessivas mostram o texto da IA crescendo antes do fim do stream (proxy confirma eventos `token` ainda chegando); (b) completa — ao receber `done`, mensagem final sem indicação de falha; (c) erro — na mensagem com falha, indicação de falha visível ("Falha ao gerar resposta — toque para tentar novamente" ou o padrão de erro de envio do protótipo), sem crash.
- Natureza: comportamental.

**H04-2 — Stream que cai no meio deixa a mensagem parcial visível, com falha**
- Conta A, Bloco I, mesma sessão.
- Passos: enviar a mensagem seguinte do roteiro; o proxy encerra a conexão SSE depois do 3º evento `token`. Tocar na indicação de falha.
- Asserção: o texto parcial continua na tela com a indicação de falha (UI); o toque gera uma chamada `chat-messages-retry`, não um novo `chat-messages-send` (proxy); a pergunta do usuário não é duplicada (SQL: contagem de mensagens `user` da sessão +1 no total, não +2).
- Natureza: comportamental.

## RF05 — Exportação do resumo pessoal

**H05-1 — Período sem entradas devolve estado de erro tratado**
- Conta C, Bloco II.
- Passos: ☰ → "Meus Registros" → ícone de download → pedir a exportação.
- Asserção: `export-summary-create` responde `400 EXPORT_EMPTY_PERIOD` (proxy); a UI mostra o estado de período vazio ("Nenhum registro nesse período."), sem botão de download, sem PDF vazio, sem crash.
- Natureza: comportamental.

**H05-2 — Falha da narrativa ainda permite baixar os dados brutos**
- Conta A, Bloco I.
- Passos: "Meus Registros" → ícone de download → pedir a exportação com `X-Test-Fault: ai_timeout` em `export-summary-create` → aguardar o fim do job → "Baixar dados brutos".
- Asserção: `export-status-get` termina com `narrativeStatus` `failed` e `downloadAvailable` verdadeiro (proxy); a UI mostra o estado de erro com o botão "Baixar dados brutos" disponível; o toque gera `export-download-get` com resposta `302` e o arquivo é baixado.
- Natureza: comportamental.

## RF06 — Busca semântica e filtros

**H06-1 — A busca encontra entradas relacionadas sem a palavra exata**
- Conta A, Bloco I.
- Passos: "Meus Registros" → barra "Buscar nos registros..." → buscar, um por vez, os três termos de `seeded-search-entries.md`.
- Asserção: para cada termo, **toda** entrada devolvida pelo backend em `entries-search` aparece na lista da UI, e a entrada semeada correspondente aparece se o backend a devolveu (proxy × UI). A qualidade semântica é do backend; o app é avaliado por exibir o que recebe.
- Natureza: comportamental.

**H06-2 — Debounce de 300 ms: digitação rápida gera uma única consulta**
- Conta A, Bloco I.
- Passos: digitar "ansiedade" caractere a caractere, com 50 ms entre teclas.
- Asserção (proxy): exatamente uma chamada `entries-search` com `q=ansiedade`, feita ≥ 300 ms depois da última tecla; nenhuma com termo parcial.
- Natureza: comportamental.

**H06-3 — Cache local consistente com o servidor após reconectar, sem duplicar**
- Conta A, Bloco I.
- Passos: abrir "Meus Registros" com rede (lista carregada); o proxy passa a responder `offline` a todas as chamadas; sair e voltar à tela (lista vinda do cache); o proxy volta ao normal; aguardar a reconexão do app (ou puxar para atualizar, se o app oferecer).
- Asserção: número de cartões na lista = número de entradas da conta A no banco (UI × SQL); nenhuma entrada aparece duas vezes.
- Natureza: comportamental.

**H06-4 — Dois filtros ao mesmo tempo restringem com E lógico**
- Conta A, Bloco III, depois de H01-1 (usa as entradas criadas na execução, porque o filtro de data é calculado com a data real do aparelho).
- Passos: funil → "INTERVALO DE DATA: Este mês" + "TIPO DE ENTRADA: áudio" → "Aplicar".
- Asserção: a chamada leva `source=audio` e `dateFrom`/`dateTo` juntos (proxy); a lista mostra só entradas de áudio do mês corrente — exatamente as que a consulta SQL com as duas condições devolve (UI × SQL).
- Natureza: comportamental.

**H06-5 — Limpar os filtros volta à lista completa sem reiniciar a tela**
- Conta A, Bloco III, logo após H06-4.
- Passos: "Limpar filtros".
- Asserção: a lista volta ao total da conta (UI × SQL) sem navegação para outra rota (a barra de busca e o cabeçalho permanecem; nenhuma tela intermediária).
- Natureza: comportamental.

## RF07 — Histórico multi-fonte (timeline)

**H07-1 — Sessão expirada durante a visualização: novo login, sem crash, sem perder o scroll**
- Conta A, Bloco I.
- Passos: "Meus Registros" → rolar até o 15º cartão; o proxy responde `401 AUTH_EXPIRED` (resposta forjada) à próxima chamada do app e a todas as `auth-refresh` seguintes até o fim do passo; provocar uma chamada (abrir uma entrada ou atualizar a lista) → "Entrar novamente" → autenticar.
- Asserção: aparece o aviso "Sessão expirada" sobre a tela, sem crash (UI); depois da reautenticação, o primeiro cartão visível é o mesmo de antes (captura antes × depois).
- Natureza: comportamental.

**H07-2 — O selo de sincronização atualiza independentemente do stream de autenticação**
- Tag `final`, análise estática.
- Asserção: o estado do selo por entrada não é derivado do estado de autenticação — nenhuma assinatura do stream/BLoC de autenticação no componente que calcula o selo.
- **Justificativa de ser estrutural:** um teste de caixa-preta exigiria mudar o estado de sincronização e o de autenticação ao mesmo tempo, sem escrita offline (arquitetura cloud-only); a independência é verificável no código.
- Natureza: estrutural.

**H07-3 — Nenhum BLoC importa outro BLoC diretamente**
- Tag `final`, análise estática (mesmo script da M7, saída de critérios estruturais).
- Asserção: zero `import` de um arquivo de BLoC dentro de outro arquivo de BLoC.
- Natureza: estrutural.

## RF08 — Insights proativos (mecanismo)

**H08-1 — Gatilho por 5 mensagens dispara exatamente uma vez**
- Conta A, Bloco I (mesmo fluxo de H04-1: `sessao1_quinta_mensagem` é a 5ª mensagem do usuário na sessão semeada).
- Asserção: exatamente uma chamada `chat-insight-create` depois da 5ª mensagem (proxy); o cartão "INSIGHT" aparece uma vez (UI); reabrir a sessão não gera nova chamada.
- Natureza: comportamental.

**H08-2 — Gatilho por 2 min de inatividade dispara exatamente uma vez**
- Conta A, Bloco I.
- Passos: ☰ → "Conversa sobre o sono" → enviar `sessao2_mensagem_1` e `sessao2_mensagem_2` → não tocar no app por 2 min 10 s → esperar mais 2 min sem nova mensagem.
- Asserção: exatamente uma chamada `chat-insight-create` no primeiro intervalo e nenhuma no segundo (proxy).
- Natureza: comportamental.

**H08-3 — Falha na geração do insight não afeta o chat**
- Conta A, Bloco I.
- Passos: provocar um novo gatilho com `X-Test-Fault: ai_timeout` em `chat-insight-create`; em seguida, enviar uma mensagem.
- Asserção: a mensagem é enviada e respondida normalmente (proxy: stream completo; UI: resposta sem erro); nenhuma mensagem de erro de insight bloqueia a conversa.
- Natureza: comportamental.

**H08-4 — Descartar o insight não altera o scroll nem a conversa**
- Conta A, Bloco I, com um cartão "INSIGHT" visível.
- Passos: tocar no "x" do cartão.
- Asserção: a primeira mensagem visível é a mesma antes e depois (captura); a lista de mensagens tem os mesmos itens, menos o cartão.
- Natureza: comportamental.

## RF09 — Resumos temporais / dashboard

**H09-1 — Renderiza com zero, uma e mais de 30 entradas**
- Contas C e B (Bloco II) e A (Bloco I).
- Passos: ☰ → "Configurações" em cada conta.
- Asserção (UI): C — estado sem dados ("Comece a registrar para ver sua evolução aqui"); B — uma barra e "Ainda é cedo pra ver um padrão — volte em alguns dias."; A — gráfico com dados e o parágrafo de resumo. Nos três, sem crash e sem erro de layout do Flutter.
- Natureza: comportamental.

**H09-2 — A agregação recalcula após criar uma entrada**
- Conta B, Bloco II.
- Passos: "Configurações" (anotar o total mostrado) → Home → "+" → "Texto" → salvar uma entrada → voltar a "Configurações".
- Asserção: nova chamada `dashboard-aggregate-get` depois da criação (proxy) e o total exibido passa de 1 para 2 (UI). A narrativa, que depende das entradas, pode cair em `REPLAY_MISS` nesse passo; não faz parte da asserção.
- Natureza: comportamental.

**H09-3 — O texto narrativo não quebra a UI em casos extremos**
- Conta B, Bloco II.
- Passos: abrir "Configurações" duas vezes, com o proxy reescrevendo a resposta de `dashboard-narrative-get`: (a) texto de 4.000 caracteres; (b) texto vazio.
- Asserção (UI): nos dois casos, sem crash, sem erro de overflow do Flutter, gráfico visível; o conteúdo do texto não é avaliado.
- Natureza: comportamental.

## RF10 — Salvar mensagem do chat como entrada

**H10-1 — A criação passa por interface compartilhada, nunca por repositório da feature de entradas**
- Tag `final`, análise estática.
- Asserção: nenhum arquivo da feature de chat importa repositório, data source ou camada `data/` da feature de entradas.
- Natureza: estrutural.

**H10-2 — Salvar a mesma mensagem duas vezes não duplica**
- Conta A, Bloco III.
- Passos: sessão "Conversa sobre o dia no trabalho" → marcador da mensagem `sessao1_quinta_mensagem` → tocar; esperar o estado salvo; tocar de novo.
- Asserção: exatamente uma linha em `entries` com esse `chat_message_id` e `source = chat` (SQL); a segunda chamada `entries-create`, se houver, recebe `200` com `idempotentReplay` (proxy); marcador em estado salvo (UI).
- Natureza: comportamental.

**H10-3 — Falha ao salvar mantém a conversa e permite tentar de novo**
- Conta A, Bloco III.
- Passos: marcador de outra mensagem do usuário com `X-Test-Fault: offline` em `entries-create`; depois, abrir outra sessão pelo menu e voltar; remover a falha e tocar no marcador de novo.
- Asserção: marcador em estado de erro depois da falha (UI); a conversa segue navegável e o campo de mensagem habilitado; o segundo toque gera nova `entries-create` e o marcador vai para salvo (proxy + UI).
- Natureza: comportamental.

**H10-4 — Só mensagens do usuário têm o botão**
- Conta A, Bloco I, sessão "Conversa sobre o dia no trabalho".
- Asserção (UI): todos os balões do usuário visíveis têm o marcador; nenhum balão da IA tem.
- Natureza: comportamental.

---

## Cobertura

| RF | Critérios na §1 | Cenários | Estruturais |
|---|---|---|---|
| RF01 | 2 | H01-1, H01-2 | — |
| RF02 | 1 | H02-1 | — |
| RF03 | 2 | H03-1, H03-2 | — |
| RF04 | 2 | H04-1, H04-2 | — |
| RF05 | 2 | H05-1, H05-2 | — |
| RF06 | 5 | H06-1 a H06-5 | — |
| RF07 | 3 | H07-1, H07-2, H07-3 | H07-2, H07-3 |
| RF08 | 3 | H08-1 a H08-4 (o 1º critério tem dois gatilhos: H08-1 e H08-2) | — |
| RF09 | 3 | H09-1, H09-2, H09-3 | — |
| RF10 | 4 | H10-1 a H10-4 | H10-1 |
| **Total** | **27** | **28** | **3** |

Nenhum critério foi excluído. O critério do RF09 sobre edição e exclusão segue a versão corrigida: entradas são imutáveis, e o cenário H09-2 testa a recalculação após **criar** uma entrada.
