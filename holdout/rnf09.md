# Suíte hold-out — 15 cenários de falha de rede (RNF09, M10)

**Destino:** `cerne-avaliacao/holdout/rnf09.md` · **Tarefa:** `C-019` · **Versão:** 23/09/2026
**Uso:** parte "cenários" da M10 (`M10_cenarios`, 0–15, só na tag `final`). Condições gerais (ambiente, proxy, contas, identificação de elementos): `holdout/cenarios.md`, seção 0.

## Mecanismo de injeção

O proxy acrescenta `X-Test-Fault: <tipo>` **só na chamada-alvo** do cenário (junto com o `X-Test-Key` de sempre). O efeito é executado pelo próprio backend, antes do handler — nenhuma escrita no banco e nenhuma chamada de IA acontecem — e fica registrado em `experiment.fault_injection_log`, o que permite conferir que cada falha foi de fato injetada. Tipos usados:

| Falha do RNF09 | `X-Test-Fault` | O que o app recebe |
|---|---|---|
| timeout | `timeout` | `504 NETWORK_TIMEOUT` |
| resposta malformada | `malformed` | corpo que não segue o contrato |
| offline | `offline` | conexão encerrada sem resposta HTTP |

**Decidido em 24/09/2026 (R30):** o mitmproxy injeta o **cabeçalho**, e o efeito é do backend — mecanismo idêntico nos dois ciclos, determinístico e auditável pelo log. A §7 do documento de métricas v1.0 foi ajustada.

## Critério de "tratado" (vale para os 15)

Um cenário passa quando as quatro condições valem:
1. **Sem quebra:** nenhum crash, nenhuma tela vermelha de erro do Flutter, nenhuma exceção não tratada no log do app.
2. **Estado de erro visível** na tela da ação, conforme a coluna "Estado esperado" — exceto no insight (RF08), cuja falha não deve aparecer como erro para o usuário.
3. **Nada perdido:** o que o usuário digitou, gravou ou escolheu continua disponível para tentar de novo.
4. **Recuperação:** removida a falha, repetir a mesma ação funciona sem reiniciar o app.

## Os 15 cenários

Conta A. F01–F12: depois dos blocos I–III de `cenarios.md` (a falha acontece antes do handler, então a chamada-alvo não toca no cache de replay nem no banco), com banco resetado ao fim. **F13–F15: dentro do Bloco I**, porque o gatilho do insight exige uma mensagem de chat bem-sucedida antes, e o chat depende do cache.

| # | Função (`x-cerne-function`) | Como provocar a chamada | Falha | Estado esperado (protótipo) |
|---|---|---|---|---|
| F01 | `entries-create` | "+" → "Texto" → digitar → "Salvar" | timeout | Modal continua aberto, texto preservado, indicação de erro com nova tentativa |
| F02 | `entries-create` | idem | malformed | idem |
| F03 | `entries-create` | idem | offline | idem (ou aviso de sem conexão) |
| F04 | `chat-messages-send` | Home → digitar → enviar | timeout | "Não foi possível enviar — toque para tentar novamente" (ou "Falha ao gerar resposta — toque para tentar novamente"); mensagem do usuário preservada |
| F05 | `chat-messages-send` | idem | malformed | idem |
| F06 | `chat-messages-send` | idem | offline | idem, ou o banner "Sem conexão — histórico disponível, novas mensagens bloqueadas" |
| F07 | `media-ocr` | "+" → "Foto" → "Galeria" → `ocr_fixture_01.png` | timeout | "Foto — Erro": "Não foi possível reconhecer o texto", "Tentar novamente", "Salvar só a foto" |
| F08 | `media-ocr` | idem | malformed | idem |
| F09 | `media-ocr` | idem | offline | idem |
| F10 | `export-summary-create` | "Meus Registros" → ícone de download → pedir exportação | timeout | Folha de exportação em estado de erro, sem PDF vazio e sem travar a lista |
| F11 | `export-summary-create` | idem | malformed | idem |
| F12 | `export-summary-create` | idem | offline | idem |
| F13 | `chat-insight-create` | "Conversa sobre o sono": enviar `rnf09_mensagem_1` e aguardar 2 min 10 s (gatilho por inatividade) | timeout | Nenhum erro visível; o chat segue funcionando (condição 2 não se aplica) |
| F14 | `chat-insight-create` | idem, com `rnf09_mensagem_2` | malformed | idem |
| F15 | `chat-insight-create` | idem, com `rnf09_mensagem_3` | offline | idem |

**Textos novos:** `rnf09_mensagem_1` a `_3` estão em `holdout/fixtures/textos-instrumento.json` (fora do pacote de entrada; o `textos.json` do handoff continua intacto), iguais nos dois ciclos.

**Conferência dos 5 endpoints:** batem com a lista congelada do backend — `entries-create`, `chat-messages-send`, `media-ocr`, `export-summary-create`, `chat-insight-create`.

**Asserções por cenário:** (proxy) a chamada-alvo recebeu o cabeçalho e o log de falhas tem a linha correspondente; (UI) capturas antes, durante e depois; (SQL, só F01–F03) nenhuma entrada nova durante a falha e exatamente uma depois da recuperação.

**Resultado:** `M10_cenarios` = número de cenários que passam (0–15). A outra parte da M10 (assinaturas de repositório fora do padrão `Either`) é estática e vem do harness.
