# Checklist manual roteirizado (plano B da suíte hold-out)

**Uso:** fallback do `GATE-C02` item 3 e do `GATE-H01`. Se a suíte automatizada (`H-005`) não estiver pronta e validada até a data de corte (**13/11/2026**, D-095), M10 e M11 passam a este checklist, **mecanismo H** (humano), registrado como desvio e declarado na monografia.
**Derivado de:** `holdout/cenarios.md` (28 cenários, 3 estruturais) e `holdout/rnf09.md` (15 falhas). **Não altera** nenhum dos dois: em dúvida, vale o arquivo de origem.
**Criado em:** 08/11/2026 (trilha do harness), versão `c1`. Não foi executado: **não validado em app nenhum** (regra 8).

## 0. Regras de execução (valem para todo o checklist)

1. **Só na tag `final`**, em build da cópia temporária (com o `.env` do ciclo), no aparelho de avaliação. Nunca durante um ciclo.
2. **Mesmo roteiro, mesma ordem, mesmo executor** nos dois ciclos. Faça o ciclo A inteiro e o B inteiro com intervalo curto entre eles; não ajuste o checklist depois de ver um resultado sem registrar desvio.
3. **Cegamento do executor:** se possível, quem executa não sabe qual ciclo é qual (rótulos `X`/`Y` sorteados pelo guia). Anote só `X`/`Y` no vídeo e na planilha; a tabela de correspondência fica com o guia.
4. **Gravação de tela contínua** durante cada bloco (um arquivo por bloco: `bloco-I-<X|Y>.mp4` etc.), com o relógio visível. Cada cenário começa dizendo em voz alta ou digitando numa nota o ID (`H04-1`) para ficar marcado no vídeo. Os vídeos ficam **fora de qualquer repositório de app**.
5. **Ambiente:** backend do ciclo em `replay_strict`, cache importado, banco com o seed congelado **uma vez** antes do bloco I (sempre por `scripts/reset-ambiente`, nunca `db reset` isolado — `C-015`). Contas do seed em `segredos/` (A cheia, B uma entrada, C vazia). Textos literais: `holdout/fixtures/textos.json` e `textos-instrumento.json`.
6. **Proxy (mitmproxy)** ligado em todas as requisições: acrescenta `X-Test-Key`/`X-Test-Now` e **injeta as falhas** (`X-Test-Fault`, corte de SSE, `401` forjado, reescrita de resposta). Use o addon da suíte (`holdout/proxy/cerne_holdout.py`, `--set cenario=<ID>`) se existir e estiver validado; senão injete à mão conforme a coluna "Proxy" de cada passo (ver §6). O log do proxy é a evidência das asserções "proxy".
7. **Identificação de elementos:** por texto visível do protótipo; ícones sem texto (☰, "+", marcador de mensagem, download, funil) pela posição no frame (`cenarios.md` §0).
8. **Resultado por cenário:** `passou` · `falhou` · `não verificável` (com justificativa). M11 por RF = passou ÷ verificáveis. Em dúvida entre passou e falhou, **grave o trecho, marque `falhou?` e deixe o guia decidir revendo o vídeo** — nunca arredonde a favor de um ciclo.
9. **Onde anotar:** uma planilha por ciclo, fora do repositório do app (a pasta final é decidida pelo guia na Parte IV): colunas `cenario | resultado | tempo_video (mm:ss) | arquivo_video | observacao | divergencia_de_texto`. Texto que difere do protótipo vai na coluna `divergencia_de_texto` (também é dado da M9).
10. **Ordem obrigatória (cache de replay):** blocos I → II → III; as chamadas de IA que dependem de ids do banco vêm antes de qualquer criação de entrada nova na conta A. Se precisar repetir um cenário do bloco I depois de escrever na conta A, **pare** e peça ao guia um reset pelo wrapper.

## 1. Preparação (antes de gravar)

- [ ] Tag `final` compilada na cópia temporária; app instalado no aparelho de avaliação, sem dados de uso anteriores (reset manual do aparelho conforme `C-024`).
- [ ] `scripts/reset-ambiente <ciclo>` rodado; `replay-mode <ciclo> replay_strict`.
- [ ] Proxy ligado e o aparelho apontando para ele; `X-Test-Key` carregado de `segredos/` sem aparecer na tela nem no vídeo.
- [ ] Biometria do aparelho cadastrada; PIN do app a cadastrar pelo fluxo do próprio app (passo específico do app).
- [ ] Fixtures disponíveis: `ocr_fixture_01.png` e `ocr_fixture_ilegivel.png` na galeria; `audio_fixture_01.wav` pronto para tocar perto do microfone (caixa de som/Mac) e um trecho de **silêncio** de 2 s.
- [ ] Gravação de tela ligada; relógio visível.

## 2. Bloco I — conta A, sem escrita

Entrar com a conta **A** (`cenario-cheio`). Ordem: H04-1, H08-1, H04-2, H08-3, H08-4, H10-4, H08-2, F13–F15, H06-1, H06-2, H06-3, H07-1, H09-1 (A), H05-2.

| ID | Passos | Proxy | Conferir (UI/proxy) | Gravar |
|---|---|---|---|---|
| **H04-1** | ☰ → "CONVERSAS" → "Conversa sobre o dia no trabalho" → enviar `sessao1_quinta_mensagem`. Depois enviar nova mensagem com falha. | 2ª mensagem: `X-Test-Fault: ai_timeout` em `chat-messages-send` | (a) texto da IA **cresce** antes do fim (proxy: eventos `token` ainda chegando); (b) ao `done`, mensagem final sem sinal de falha; (c) na mensagem com falha, indicação de falha visível ("Falha ao gerar resposta — toque para tentar novamente" ou padrão do protótipo), sem crash | Todo o envio, com a tela rolando o streaming |
| **H08-1** | Mesmo fluxo do H04-1 (a `sessao1_quinta_mensagem` é a 5ª do usuário) | — | Exatamente **uma** `chat-insight-create` após a 5ª mensagem; cartão "INSIGHT" aparece **uma** vez; reabrir a sessão **não** gera nova chamada | Cartão + log do proxy |
| **H04-2** | Mesma sessão: enviar a mensagem seguinte do roteiro; tocar na indicação de falha | Encerrar a conexão SSE após o **3º** evento `token` | Texto parcial **permanece** com indicação de falha; o toque gera `chat-messages-retry` (não novo `chat-messages-send`); mensagens `user` da sessão: **+1** no total, não +2 (contagem no app ou SQL do guia) | Corte e toque |
| **H08-3** | Provocar novo gatilho com falha no insight; depois enviar uma mensagem | `X-Test-Fault: ai_timeout` em `chat-insight-create` | Mensagem enviada e respondida normalmente (stream completo); nenhum erro de insight bloqueia a conversa | Envio pós-falha |
| **H08-4** | Com um cartão "INSIGHT" visível, tocar no "x" | — | A **primeira mensagem visível** é a mesma antes e depois (print/frames); lista igual, menos o cartão | Antes e depois, mesma rolagem |
| **H10-4** | Sessão "Conversa sobre o dia no trabalho" | — | **Todos** os balões do usuário visíveis têm o marcador; **nenhum** balão da IA tem (rolar a sessão toda) | Rolagem completa |
| **H08-2** | ☰ → "Conversa sobre o sono" → enviar `sessao2_mensagem_1` e `sessao2_mensagem_2` → **não tocar no app por 2 min 10 s** → esperar mais 2 min sem nova mensagem | — | Exatamente **uma** `chat-insight-create` no 1º intervalo e **nenhuma** no 2º (cronômetro visível no vídeo) | Relógio + tela parada |
| **F13–F15** | "Conversa sobre o sono": enviar `rnf09_mensagem_1` (F13), `_2` (F14), `_3` (F15); aguardar 2 min 10 s em cada (gatilho por inatividade) | `X-Test-Fault` em `chat-insight-create`: `timeout` (F13), `malformed` (F14), `offline` (F15) | Condições 1, 3 e 4 do critério "tratado" (`rnf09.md`): **nenhum erro visível ao usuário**, chat segue funcionando; log de falhas do backend tem a linha da injeção | Espera + chat funcionando depois |
| **H06-1** | "Meus Registros" → barra "Buscar nos registros..." → buscar, **um por vez**, os três termos de `seeded-search-entries.md` | — | Para cada termo, **toda** entrada devolvida em `entries-search` (proxy) aparece na lista da UI; a entrada semeada correspondente aparece se o backend a devolveu | Cada busca + corpo da resposta no proxy |
| **H06-2** | Digitar "ansiedade" caractere a caractere, ~50 ms entre teclas (digitar rápido; usar teclado de sobreposição se preciso) | Contagem de requisições | **Exatamente 1** `entries-search` com `q=ansiedade`, ≥ 300 ms após a última tecla; nenhuma com termo parcial | Digitação + log do proxy |
| **H06-3** | Abrir "Meus Registros" com rede (lista carregada); proxy passa a responder `offline` a tudo; sair e voltar à tela; proxy volta ao normal; aguardar reconexão (ou puxar para atualizar) | `offline` em todas as chamadas, depois normal | Nº de cartões = nº de entradas da conta A no banco (guia confere o `count`); **nenhuma entrada duplicada** | Transições + contagem |
| **H07-1** | "Meus Registros" → rolar até o **15º cartão** → provocar uma chamada (abrir entrada ou atualizar) → "Entrar novamente" → autenticar | `401 AUTH_EXPIRED` forjado na próxima chamada **e** em todas as `auth-refresh` seguintes até o fim do passo | Aparece o aviso "Sessão expirada" sobre a tela, **sem crash**; depois do login, o primeiro cartão visível é o **mesmo** de antes (print antes × depois) | Todo o passo |
| **H09-1 (A)** | ☰ → "Configurações" | — | Gráfico com dados e parágrafo de resumo; **sem crash e sem erro de layout do Flutter** (tela vermelha/overflow) | Tela inteira |
| **H05-2** | "Meus Registros" → ícone de download → pedir a exportação → aguardar o fim → "Baixar dados brutos" | `X-Test-Fault: ai_timeout` em `export-summary-create` | `export-status-get` termina com `narrativeStatus` `failed` e `downloadAvailable` verdadeiro; UI em estado de erro **com** o botão "Baixar dados brutos"; o toque gera `export-download-get` com `302` e o arquivo baixa | Todo o fluxo + resposta no proxy |

## 3. Bloco II — contas B e C

Sair e entrar com a conta **C** (`cenario-vazio`) e depois **B** (`cenario-uma`). Ordem: H05-1 (C), H09-1 (C, B), H09-2 (B), H09-3 (B).

| ID | Passos | Proxy | Conferir | Gravar |
|---|---|---|---|---|
| **H05-1** | Conta C: ☰ → "Meus Registros" → ícone de download → pedir a exportação | — | `export-summary-create` responde `400 EXPORT_EMPTY_PERIOD` (proxy); UI mostra "Nenhum registro nesse período.", **sem** botão de download, **sem** PDF vazio, sem crash | Fluxo + resposta |
| **H09-1 (C)** | Conta C: ☰ → "Configurações" | — | "Comece a registrar para ver sua evolução aqui"; sem crash/erro de layout | Tela |
| **H09-1 (B)** | Conta B: ☰ → "Configurações" | — | Uma barra e "Ainda é cedo pra ver um padrão — volte em alguns dias."; sem crash/erro de layout | Tela |
| **H09-2** | Conta B: "Configurações" (**anotar o total mostrado**) → Home → "+" → "Texto" → salvar uma entrada → voltar a "Configurações" | — | Nova `dashboard-aggregate-get` **após** a criação (proxy) e o total passa de **1 para 2**. (A narrativa pode cair em `REPLAY_MISS`: não faz parte da asserção.) | Antes, criação, depois |
| **H09-3** | Conta B: abrir "Configurações" **duas vezes** | Reescrever a resposta de `dashboard-narrative-get`: (a) texto de **4.000 caracteres**; (b) texto **vazio** | Nos dois casos: sem crash, sem overflow do Flutter, **gráfico visível** (o conteúdo do texto não é avaliado) | As duas aberturas |

## 4. Bloco III — conta A, com escrita

Voltar à conta **A**. Ordem: H03-1, H03-2, H01-2, H01-1, H02-1, H06-4, H06-5, H10-2, H10-3 (e, **depois** destes, os estados do §7 que dependem de escrita).

| ID | Passos | Proxy | Conferir | Gravar |
|---|---|---|---|---|
| **H03-1** | Bloquear o app → "Toque para desbloquear" → tocar e **simular rosto não reconhecido** (cobrir a câmera/olhar para o outro lado) → digitar o PIN (cadastrado pelo fluxo do app) | — | Aparece "Não foi possível reconhecer — digite seu PIN" com teclado numérico; após o PIN, Home/Chat | Todo o fluxo |
| **H03-2** | Com o app desbloqueado na Home, enviar para background; **esperar 5 min 10 s** (tempo real); voltar | — | Tela "Toque para desbloquear" (ou PIN), **não** a Home | Relógio + retorno |
| **H01-2** | "+" → "Áudio" → gravar 3 s → **fechar o modal ("x") sem parar a gravação** | — | **Nenhuma** `entries-create` no intervalo (proxy); contagem de `entries` da conta A **inalterada** (guia confere); nada novo em "Meus Registros" | Fluxo + lista |
| **H01-1** | Home → "+" → "Texto" → digitar `entrada_manual_nova` → "Salvar". "+" → "Áudio" → gravar enquanto o fixture toca → parar → aguardar texto transcrito → "Salvar". "+" → "Foto" → "Galeria" (ou câmera, se o aparelho for físico — **mesma escolha nos dois ciclos**) → imagem → aguardar texto → "Salvar" | — | Três linhas novas em `entries`, `source` = `manual`, `audio`, `photo`; nas três o mesmo conjunto de colunas preenchidas (`content` não vazio, `embedding` não nulo, `chat_message_id` nulo); três `entries-create` com o mesmo formato de corpo (guia confere por SQL) | Os três fluxos |
| **H02-1** | Durante o H01-1 observar: **gravando** (cronômetro correndo), **processando** ("Transcrevendo..." depois de parar), **transcrito** (texto editável com a duração). Depois: nova gravação de 2 s de **silêncio**; depois OCR com `ocr_fixture_ilegivel.png` | — | Silêncio → "Não foi possível transcrever" com "Tentar novamente". OCR → "Reconhecendo texto..." → "Não foi possível reconhecer o texto", com "Tentar novamente" e "Salvar só a foto". **Se o app aceitar transcrição vazia como sucesso, o cenário falha** | Os 5 estados |
| **H06-4** | (Depois do H01-1.) "Meus Registros" → funil → "INTERVALO DE DATA: Este mês" + "TIPO DE ENTRADA: áudio" → "Aplicar" | — | A chamada leva `source=audio` e `dateFrom`/`dateTo` **juntos** (proxy); a lista mostra só áudios do mês corrente, **exatamente** os que a consulta SQL com as duas condições devolve (guia) | Sheet + lista |
| **H06-5** | "Limpar filtros" | — | A lista volta ao total da conta (guia confere), **sem navegar** para outra rota (barra de busca e cabeçalho permanecem) | Clique + lista |
| **H10-2** | Sessão "Conversa sobre o dia no trabalho" → marcador da mensagem `sessao1_quinta_mensagem` → tocar; esperar o estado salvo; **tocar de novo** | — | Exatamente **uma** linha em `entries` com esse `chat_message_id` e `source = chat` (guia por SQL); a 2ª `entries-create`, se houver, recebe `200` com `idempotentReplay`; marcador em estado salvo | Os dois toques |
| **H10-3** | Marcador de **outra** mensagem do usuário; depois abrir outra sessão pelo menu e voltar; remover a falha e tocar de novo | `X-Test-Fault: offline` em `entries-create` (1º toque); depois sem falha | Marcador em estado de **erro** após a falha; conversa navegável e campo de mensagem habilitado; o 2º toque gera nova `entries-create` e o marcador vai para **salvo** | Todo o passo |

## 5. Estruturais (revisão do código da tag `final`, sem executar o app)

Feitos por **leitura** do código, de preferência pelo script (`harness/estatico/m7_camadas.py`, saídas `rf07_*` e `rf10_*`) e conferidos por uma leitura rápida dos arquivos apontados.

| ID | O que verificar | Como |
|---|---|---|
| **H07-2** | O selo de sincronização por entrada **não** é derivado do estado de autenticação: nenhuma assinatura do stream/BLoC de autenticação no componente que calcula o selo | Leitura: localizar o componente do selo (`sync-badge.md` do pacote de entrada) e listar seus imports/assinaturas. **Sem módulo automático** (não está no escopo do H-002) |
| **H07-3** | Nenhum BLoC importa outro BLoC | `python3 -m harness.estatico.m7_camadas ... ` → `rf07_bloc_importa_bloc` vazio = passou |
| **H10-1** | Nenhum arquivo da feature de chat importa repositório, data source ou camada `data/` da feature de entradas | Idem → `rf10_chat_importa_entradas` vazio = passou. Os nomes das features (`--chat-feature`, `--entries-feature`) são os do app medido |

## 6. Falhas de rede do RNF09 (M10 `cenarios`, 15 cenários)

Conta A, depois dos blocos I–III (F13–F15 já foram no bloco I, §2). O proxy injeta `X-Test-Fault` **só na chamada-alvo**; o efeito é do backend e fica em `experiment.fault_injection_log` (o guia confere a linha da injeção). Critério de "tratado" (quatro condições — todas): **(1)** sem quebra (sem crash/tela vermelha); **(2)** estado de erro visível na tela da ação (exceto insight); **(3)** nada perdido (texto/gravação/escolha preservados para repetir); **(4)** recuperação: removida a falha, repetir a ação funciona **sem reiniciar o app**.

| ID | Chamada-alvo | Como provocar | Falha | Estado esperado |
|---|---|---|---|---|
| F01–F03 | `entries-create` | "+" → "Texto" → digitar → "Salvar" | `timeout`, `malformed`, `offline` | Modal **continua aberto**, texto preservado, indicação de erro com nova tentativa (F03: ou aviso de sem conexão). **SQL (guia):** nenhuma entrada nova durante a falha e exatamente uma após a recuperação |
| F04–F06 | `chat-messages-send` | Home → digitar → enviar | `timeout`, `malformed`, `offline` | "Não foi possível enviar — toque para tentar novamente" (ou "Falha ao gerar resposta — toque para tentar novamente"); mensagem do usuário preservada (F06: ou banner "Sem conexão — histórico disponível, novas mensagens bloqueadas") |
| F07–F09 | `media-ocr` | "+" → "Foto" → "Galeria" → `ocr_fixture_01.png` | `timeout`, `malformed`, `offline` | "Foto — Erro": "Não foi possível reconhecer o texto", "Tentar novamente", "Salvar só a foto" |
| F10–F12 | `export-summary-create` | "Meus Registros" → download → pedir exportação | `timeout`, `malformed`, `offline` | Folha de exportação em estado de erro, **sem PDF vazio** e **sem travar a lista** |
| F13–F15 | `chat-insight-create` | feitos no bloco I (§2) | `timeout`, `malformed`, `offline` | Nenhum erro visível; chat segue funcionando |

Para cada um dos 12 primeiros: gravar (a) a falha acontecendo, (b) o estado de erro, (c) a **recuperação** (remover a falha e repetir a ação sem reiniciar). `M10_cenarios` = número de cenários (de 15) em que as quatro condições valeram.

## 7. Estados da M9 (31) — captura para o avaliador visual e para as partes D

Fonte: `holdout/estados-m9.md` (a tabela de 31 estados com caminho e conta). Para cada estado: **screenshot** (não só vídeo) no tamanho nativo do aparelho, nomeado `<X|Y>-<estado_id>.png` (ex.: `X-t2audio_error.png`), no momento certo; estados transitórios (processando/streaming) são congelados pelo proxy (segurar a resposta durante a captura); estado inalcançável = score 0 com justificativa. Ordem: os que chamam IA na conta A (6, 17, 22–25, 27, 30) **dentro do Bloco I** (antes de qualquer escrita); 7–15 no Bloco III; os de conta B/C (19, 26, 28, 29) no Bloco II.

- [ ] Registrar também, para o H-003/H-004 (partes D da M9), a fonte e a cor **na árvore de widgets** se o executor tiver o teste de introspecção; sem ele, a tipografia fica com o avaliador visual (decisão do guia).
- [ ] Lista de controle: marcar os 31 `estado_id` capturados por ciclo: `splash, bio, login, pinInicial, pinErro, home, t2texto, t2audio_recording, t2audio_processing, t2audio_transcribed, t2audio_error, t2foto_idle, t2foto_processing, t2foto_recognized, t2foto_error, menu, sessao, registros, vazio, filtro, filtrosAtivos, exp_pending, exp_processing, exp_done, exp_error, exp_empty, config, dashZero, dashUma, dashNarrativeError, excluir`.

## 8. Fechamento

- [ ] Cada cenário (28 + 15, com os 3 estruturais) tem uma linha na planilha do ciclo, com resultado e arquivo/tempo de vídeo.
- [ ] `REPLAY_MISS` em qualquer cenário: registrar como achado sobre o app, rerodar **só aquele cenário** em `replay` e marcar "IA ao vivo" (regra do `V-002`, passo 5).
- [ ] Entregar ao guia: planilhas, vídeos, screenshots, log do proxy (sem a chave). Nada disso entra em repositório de app.
- [ ] Declarar na monografia: M10 (cenários) e M11 medidas por **mecanismo H** (checklist), com a data de corte e o motivo (D-095).

## 9. Cobertura em relação aos arquivos de origem

28 cenários de `cenarios.md` (H01-1, H01-2, H02-1, H03-1, H03-2, H04-1, H04-2, H05-1, H05-2, H06-1…H06-5, H07-1…H07-3, H08-1…H08-4, H09-1…H09-3, H10-1…H10-4) + 15 de `rnf09.md` (F01…F15, dos quais F13–F15 estão no bloco I) + 31 estados de `estados-m9.md`.
