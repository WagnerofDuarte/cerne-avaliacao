# Plano de execução — Ciclo A (GitHub Spec Kit v1.0.10)

**Projeto:** TCC Wagner Duarte — Spec Kit × BMAD-METHOD (veículo: app Cerne)
**Versão deste documento:** 1.2 — 07/10/2026 (seção 3 e A0 executadas; ajustes do que foi aprendido na execução e desvios D-009/D-010). Versão 1.1: 01/10/2026, decisões D-001 a D-008
**Base:** protocolo congelado (tag `protocolo-v1.0` em `cerne-avaliacao`) — `docs/protocolo.md`, `docs/Metricas_e_Skills_Ciclos.md` v1.0, `prompts/`, `entrada/`, `scripts/`, `skills/coletar-sessao/`.
**Conferido contra:** Spec Kit v1.0.10 reinstalado em pasta descartável (texto real de cada comando); `cerne-backend` (commit `5a0f809`); `cerne-backend-handoff` (commit `fa998d9`); `cerne-ciclo-a` no GitHub (vazio em 01/10/2026).
**Precedência:** protocolo congelado > comportamento real das ferramentas > este documento > `plano-ciclos.md` Parte II. Onde este documento corrige a Parte II, a correção está listada no Apêndice B.

> **Situação da execução (11/10/2026):**
> | Etapa | Situação | Evidência |
> |---|---|---|
> | Seção 3 — preparação única | ✅ concluída | Achados viraram D-009 (tema no `settings.json`; skills da conta só no `cfg-ciclo-a`, removidas) e D-010 (macOS 27.0.1 `26A434` e iOS 27.0.1 `24A446`; atualizações automáticas desligadas). `abrir-ciclo` substituído. Assinatura: plano **Pro** |
> | Pré-voo de 08/10 | ✅ ambiente igual após reinício; **D-011** (gitignore global para `.DS_Store`) e **D-012** (sincronização de skills/plugins da conta desligada nos dois `settings.json`) e, em 11/10, **D-013** (conectores do claude.ai desligados; hash vigente `0112786e…f393`) | `desvios.md` |
> | `A-001` baseline | ✅ | `cicloA/baseline` em `1cd770a` |
> | `GATE-A01` Spec Kit | ✅ (5 s, M1) | `cicloA/instalado` em `28ef31d` |
> | `GATE-A02` largada | ✅ | `dados/evidencias/gate-a02-ciclo-a.png` |
> | `GATE-A02b` reconferência pós-D-012 (7.3b) | ✅ (08/10; disco conferido em 11/10) | `dados/evidencias/gate-a02b-pos-d012-ciclo-a.png` |
> | `GATE-A02c` reconferência pós-D-013 (7.3c) | ✅ (11/10) | `dados/evidencias/gate-a02c-ciclo-a.png` |
> | Coletor OTel e plano Pro (P13) | ✅ (11/10) | `dados/evidencias/plano-pro-pagina-de-planos-2026-10-11.png` |
> | `A1` `A-002` sessão `SETUP` + coleta + tag `cicloA/setup-done` | ✅ (11/10) | Commit `e1f8057`, tag `cicloA/setup-done`; 0 intervenções, 0 `PROCESSO:`. **D-014:** invocação (comando digitado + argumento colado) e detecção de fase do coletor corrigidas; dados commitados em `cerne-avaliacao` (`3caeb1a`); falta repetir o check 8.5 depois do primeiro `/speckit-specify` (A2) |
> | A2 F000 — sessão 1 (`specify`) + check 8.5 | ✅ (11/10) | `ESPEC,speckit-specify` reconhecido; sem perguntas; 0/0 |
> | A2 F000 — sessão 2 (`clarify`) | ✅ (11/10) | 1 pergunta, resposta padrão por *Other*; **D-015:** o coletor não lia respostas do painel (`n_processo=0`); corrigido, sessão re-derivada na Parte IV |
> | A2 F000 — sessão 3 aberta como `/speckit-checklist` (11/10) | ⚠️ interrompida | O script exige `plan.md`; **D-016:** ordem passa a `plan` → `checklist`; 1 intervenção `esclarecimento não solicitado` ("Stop here"); coletada como `F000` (1 intervenção reconhecida; alerta `div_otel` anotado, sem investigar) |
> | A2 F000 — sessão 4 (`plan`) | ✅ (11/10) | 0 intervenções, 0 `PROCESSO:` |
> | A2 F000 — sessão 5 (`checklist`) | ✅ (11/10) | 3 `PROCESSO:` reconhecidos (painel de 3 abas), 0 intervenções |
> | A2 F000 — sessão 6 (`tasks`) | ✅ (11/10) | 0 intervenções, 0 `PROCESSO:`; alerta `div_otel` anotado |
> | A2 F000 — sessão 7 (`analyze`) | ✅ (11/10) | 1 `PROCESSO:` reconhecido; **RDR nº 1** gravado |
> | A2 F000 — sessão 8 (`implement`) | ✅ (11/10) | 1 `PROCESSO:` (**RDR nº 2**); agente usou simulador por conta própria (anotado) |
> | A2 F000 — sessão 9 (`converge`) | ✅ (11/10) | Não convergiu; 0 intervenções, 0 `PROCESSO:`; alerta `div_otel` anotado |
> | A2 F000 — sessão 10 (`implement`, 2º) | ✅ (11/10) | 1 `PROCESSO: yes` (texto do RDR nº 2) |
> | A2 F000 — sessão 11 (`converge`) ✅ *Converged*; P6 (b)(c) ok; (d) falhou em 2 itens | ⚠️ | splash branca (S2); criar conta "sem conexão" (S3); ambiente descartado |
> | A2 F000 — sessão 12 (correção) | ✅ (11/10) | 2 intervenções; **D-017:** cadastro por e-mail desligado no Supabase (ambiente, 3.7.1), corrigido nos dois projetos; só a splash mudou código |
> | A2 F000 — sessão 13 (correção) e P6 | ⚠️ (11/10) | **D-018:** chave anon mascarada nos `.env` (ambiente), corrigida; cadastro e splash OK; item 5 revelou defeito: sessão inválida (401 `AUTH_INVALID`) deixa o app preso na splash |
> | **A2 F000 concluída (12/10)** | ✅ | Commit `2c5d84b`, tag `cicloA/f000-done`; dados em `2520e9e`; P6 ok (item 6 n/a) |
> | A3 RF03 — sessão 1 (`specify`, 12/10) | ✅ | Sessão `b17926dd`; coletada como `RF03`; 0 intervenções, 0 `PROCESSO:`; aviso de subagentes (esperado) |
> | A3 RF03 — sessão 2 (`clarify`, 12/10) | ✅ | Sessão `1e1d1d9b`; 1 `PROCESSO:` reconhecido; 0 intervenções |
> | A3 RF03 — sessão 3 (`plan`, 12/10) | ✅ | Sessão `5500fd78`; 0 intervenções, 0 `PROCESSO:`; alerta `div_otel` anotado (sem investigar) |
> | A3 RF03 — sessão 4 (`checklist`, 12/10) | ✅ | Sessão `a2816ab4`; 2 `PROCESSO:` reconhecidos (painel de 2 perguntas), 0 intervenções; alerta `div_otel` anotado (sem investigar) |
> | A3 RF03 — sessão 5 (`tasks`, 12/10) | ✅ | Sessão `678c334f`; 0 intervenções, 0 `PROCESSO:`; alerta `div_otel` anotado (sem investigar) |
> | A3 RF03 — sessão 6 (`analyze`, 12/10) | ✅ | Sessão `697c3db0`; 0 intervenções, 0 `PROCESSO:` (sem resposta registrada à oferta de remediação); sem alerta `div_otel` |
> | A3 RF03 — sessão 7 (`implement`, 12/10) | ✅ | Sessão `9b85d456`; 1 `PROCESSO: yes` (texto do RDR nº 2, sem linha nova); 0 intervenções |
> | A3 RF03 — sessão 8 (`converge`, 12/10) | ✅ *Converged* | Sessão `423f1e59`; convergiu na 1ª rodada do laço; 0 intervenções, 0 `PROCESSO:` |
> | A3 RF03 — P6 (12/10) | ⚠️ em andamento | (a) *Converged*; (b) `analyze` sem problemas; (c) 130 testes passam; (d) itens do roteiro (PIN, falha do Face ID, 5 min 15 s em segundo plano) ok no iPhone; o pesquisador anotou diferenças de tela em relação ao protótipo → sessão de correção (9.4) |
> | A3 RF03 — sessões 9 a 12 (correção, 12 a 13/10) | ✅ coletadas | 4 sessões de correção, uma por tela, com 1 intervenção `correção` cada (splash `S1`, login `S2`, biometria `S2`, PIN `S1`; **D-019**) |
> | A3 RF03 — nova P6 após a correção (13/10) | ✅ | `analyze`, `test` e roteiro completo no iPhone (4 telas corrigidas, Face ID/PIN, 5 min 15 s em segundo plano, login e senha errada) passaram, segundo o pesquisador |
> | **A3 RF03 concluída (13/10)** | ✅ | Commit `98f1bea`, tag `cicloA/rf03-done`; dados em `3180308`; 12 sessões (8 do fluxo + 4 de correção, uma por tela — D-019); P6 ok |
> | A4 RF01 — sessões 1 a 7 (`specify`, `clarify`, `plan`, `checklist`, `tasks`, `analyze`, `implement`) (13/10) | ✅ coletadas | `implement` terminou com 70 de 71 tarefas (a T071 é manual, da P6(d)); contagens a conferir no `sessoes.csv` no fechamento |
> | A4 RF01 — sessão 8 (`converge`, 13/10) | ✅ *Converged* | 1ª rodada, sem lacunas; achado de escopo (STT e OCR já na RF01): decidido não intervir, só anotar |
> | A4 RF01 — P6 (13/10) | ⚠️ (d) falhou | (b) e (c) ok; no iPhone o teclado cobre o modal de inserção e o botão de salvar fica inalcançável |
> | A4 RF01 — sessão 9 (correção, 13/10) | ✅ coletada | 2 intervenções `correção|S2|prd` na mesma sessão (Texto/teclado; Áudio sem estado inicial); contagens a conferir no fechamento |
> | A4 RF01 — nova P6 após a correção (13/10) | ✅ | `analyze`, `test` e roteiro completo no iPhone passaram, segundo o pesquisador |
> | A4 RF01 — sessão 10 (correção de design do modal, 13/10) | ✅ coletada | 1 intervenção enviada colada e não reconhecida pelo coletor (**D-020**); P6: `analyze` e 196 testes ok, mais discrepâncias de design no iPhone |
> | A4 RF01 — sessão 11 (correção do Áudio, 14/10) e nova P6 | ✅ | 1 intervenção `S1|prd` colada, não reconhecida pelo coletor (**D-020**, 2ª ocorrência); P6 aprovada, segundo o pesquisador; a revisão da transcrição fica para a RF02 |
> | **A4 RF01 concluída (14/10)** | ✅ | Commit `80486e5`, tag `cicloA/rf01-done`, dados em `64f9f0a`; 13 sessões (8 do fluxo, 2º laço de `implement`/`converge`, 3 de correção; D-019, D-020); push do ciclo na 2ª tentativa |
> | A5 RF02 — sessões 1 a 8 (`specify` a `converge`, 13 a 14/10) | ✅ coletadas | *Converged* na 1ª rodada; `analyze` com 2 `PROCESSO:` (**D-022**: a 2ª devia ser neutra) |
> | A5 RF02 — P6 e 2 sessões de correção de design (17/10) | ✅ | 2 intervenções `correção|S2|prd` digitadas e reconhecidas; P6 aprovada na 3ª rodada, segundo o pesquisador |
> | **A5 RF02 concluída (17/10)** | ✅ | Commit `dfdac64`, tag `cicloA/rf02-done`, dados em `50dab1f`; 10 sessões (8 do fluxo, 1 laço, 2 de correção); push do ciclo na 1ª tentativa |
> | A6 RF07 — sessões 1 `specify`, 2 `clarify`, 3 `plan`, 4 `checklist`, 5 `tasks` e 6 `analyze` (17/10) | ✅ coletadas | 0 intervenções; `PROCESSO:` 0/0/0/3/0/1 (`checklist` e `analyze`); timebox < 50%; `div_otel` nas sessões 1, 2, 4 e 6 (anotado); `analyze` sem CRITICAL (1 HIGH, 1 MEDIUM) |
> | A6 RF07 — sessão 7 `implement` (17/10) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); 39 de 41 tarefas (T037 e T041 são manuais, do pesquisador); 264 testes passam, `analyze` limpo; timebox < 50% |
> | A6 RF07 — sessão 8 `converge` (17/10) | ✅ coletada | **Converged na 1ª rodada**; 0 intervenções, 0 `PROCESSO:`; timebox < 50% |
> | A6 RF07 — P6 rodada 1 (17/10) | ⚠️ funcional passou; design com 6 diferenças na Tela 4 | Sessão expirada "verificada em parte" e sem gesto de "puxar para atualizar" (**D-023**); Vazio (opcional) não testado |
> | A6 RF07 — sessão 9, correção de design da Tela 4 (17/10) | ✅ coletada | Intervenção `correção|S2|prd` **colada**, coletor com 0 (esperado 1): 3ª ocorrência do **D-020**, conta como 1 |
> | A6 RF07 — P6 rodada 2 (17/10) | ✅ | Aprovada, segundo o pesquisador; sessão expirada "verificada em parte" (D-023) |
> | **A6 RF07 concluída (17/10)** | ✅ | Commit `72847f9`, tag `cicloA/rf07-done`, dados em `ddf09fb`; 9 sessões (8 do fluxo, 1 laço, 1 de correção; D-020 3ª ocorrência, D-023); push do ciclo na 1ª tentativa |
> | A7 RF06 — sessões 1 `specify` e 2 `clarify` (17/10) | ✅ coletadas | 0 intervenções; `PROCESSO:` 0 e 1; timebox < 50%; sem `div_otel` |
> | A7 RF06 — sessão 3 `plan` (17/10, coletada em 18/10) | ✅ coletada | 0 intervenções, 0 `PROCESSO:`; faixa `atingido` indevida por coleta tardia (**D-024**): coletor corrigido, `retempos` aplicado (dados `bba6080`), faixa da RF06 `abaixo de 50%` |
> | A7 RF06 — sessão 4 `checklist` (18/10) | ✅ coletada | 0 intervenções, 3 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A7 RF06 — sessão 5 `tasks` (18/10) | ✅ coletada | 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | A7 RF06 — sessão 6 `analyze` (18/10) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 1); timebox < 50%; `div_otel` anotado |
> | A7 RF06 — sessão 7 `implement` (18/10) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); timebox < 50%; sem `div_otel` |
> | A7 RF06 — sessão 8 `converge` (19/10) | ✅ coletada | **Converged na 1ª rodada**; 0 intervenções, 0 `PROCESSO:`; timebox < 50% |
> | A7 RF06 — P6 rodada 1 (19/10) | ⚠️ 3 critérios passaram; cache offline falhou; design com 5 grupos de diferenças | C1, C4, C5 passaram; C2 e categorias só anotados; C3 falhou em parte (S2) |
> | A7 RF06 — sessão 9, correção (19/10) | ✅ coletada | 2 intervenções `correção|S2|prd` digitadas e reconhecidas |
> | A7 RF06 — P6 rodada 2 (19/10) | ⚠️ cache offline passou; sheet com novas diferenças | Regra nova: elemento só do resumo e que o app oferece é diferença (S2) |
> | A7 RF06 — sessão 10, 2ª correção (19/10) | ✅ coletada | 3 intervenções (2 `correção|S2|prd` + 1 `esclarecimento não solicitado`); o agente manteve "Salvar só a foto" por conflito com o pacote |
> | A7 RF06 — P6 rodada 3 (19/10) | ✅ | Aprovada, segundo o pesquisador |
> | **A7 RF06 concluída (19/10)** | ✅ | Commit `0d5c0f2`, tag `cicloA/rf06-done`, dados em `cf9d730`; 10 sessões (8 do fluxo, 1 laço, 2 de correção; 4 `correção|S2|prd` + 1 `esclarecimento não solicitado`; D-024); push do ciclo na 1ª tentativa |
> | A8 RF04 — sessões 1 `specify`, 2 `clarify`, 3 `plan`, 4 `checklist` e 5 `tasks` | ✅ coletadas | 0 intervenções; `PROCESSO:` 0/1/0/3/0; timebox < 50%; sem `div_otel` |
> | A8 RF04 — sessão 6 `analyze` | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 1); relatório com 1 CRITICAL e 1 HIGH, remediados na sessão (54 tarefas); timebox < 50% |
> | A8 RF04 — sessão 7 `implement` | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); timebox < 50%; sem `div_otel` |
> | A8 RF04 — sessão 8 `converge` | ✅ coletada | **Sem *Converged***: 2 lacunas (1 HIGH, 1 MEDIUM), T055 e T056 anexadas; 0 intervenções, 0 `PROCESSO:`; timebox < 50% |
> | A8 RF04 — sessão 9 `implement` (2ª rodada) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); timebox < 50%; `div_otel` anotado |
> | A8 RF04 — sessão 10 `converge` (2ª rodada) | ✅ coletada | **Sem *Converged***: 3 lacunas (1 HIGH, 2 MEDIUM), T057 a T059 anexadas; 0 intervenções, 0 `PROCESSO:`; timebox < 50% |
> | A8 RF04 — sessão 11 `implement` (3ª rodada) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); 58 de 59 tarefas (T054 é manual, do pesquisador); 401 testes passam; timebox < 50%; `div_otel` anotado |
> | A8 RF04 — sessão 12 `converge` (3ª rodada) | ✅ coletada | **Sem *Converged***: 1 lacuna (MEDIUM, falta um teste), T060 anexada; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A8 RF04 — sessão 13 `implement` (4ª rodada) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); 59 de 60 tarefas (T054 é manual, do pesquisador); 402 testes passam; timebox < 50%; `div_otel` anotado |
> | A8 RF04 — sessão 14 `converge` (4ª rodada) | ✅ coletada | **Sem *Converged***: 1 lacuna (HIGH, quadro SSE malformado sem tratamento), T061 anexada; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A8 RF04 — sessão 15 `implement` (5ª rodada) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); 60 de 61 tarefas (T054 é manual, do pesquisador); timebox < 50%; sem `div_otel` |
> | A8 RF04 — sessão 16 `converge` (5ª rodada) | ✅ coletada | **Sem *Converged***: 1 lacuna (HIGH, falta um teste de cenário do contrato), T062 anexada; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | A8 RF04 — sessão 17 `implement` (6ª rodada) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); 61 de 62 tarefas (T054 é manual, do pesquisador); 405 testes passam; timebox < 50%; sem `div_otel` |
> | A8 RF04 — sessão 18 `converge` (6ª rodada) | ✅ coletada | **Sem *Converged***: 1 lacuna (MEDIUM, só falta teste de widget da `HomeChatShellPage`), T063 anexada; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A8 RF04 — sessão 19 `implement` (7ª rodada) | ✅ coletada | 0 intervenções, 1 `PROCESSO:` (RDR nº 2); 62 de 63 tarefas (T054 é manual, do pesquisador); 413 testes passam; timebox < 50%; sem `div_otel` |
> | A8 RF04 — sessão 20 `converge` (7ª rodada) | ✅ coletada | **Converged na 7ª rodada** (7 rodadas `implement`/`converge`); 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A8 RF04 — P6 rodada 1 (20/10) | ⚠️ falhou | (a)–(c) ok; (d): resposta nova do chat falha ao vivo (S3, D16: backend ok), horário do histórico em UTC e diferenças de design das Telas 1 e 3 → sessão de correção (9.4) |
> | A8 RF04 — sessão 21 (correção, 20/10) | ✅ coletada | Sessão `4b6255e3`; 5 intervenções reconhecidas (4 mensagens + 1 esclarecimento não solicitado, §2.4), 0 `PROCESSO:`; timebox < 50%; aviso de subagentes (esperado). Nova P6 pendente |
> | A8 RF04 — P6 rodada 2 (20/10) | ⚠️ falhou | Resposta nova do chat ainda falha ao vivo (celular e Wi-Fi); resíduos de design da Tela 1; D-025 (frase de investigação) → sessão de correção 22 |
> | A8 RF04 — sessão 22 (correção, 20/10) | ✅ coletada | Sessão `812c5b61`; 2 intervenções (a resposta nova do chat ao vivo, S3, com a frase do D-025, e design da Tela 1); 0 `PROCESSO:`; timebox 50–80%; o defeito S3 foi resolvido |
> | A8 RF04 — sessão 23 (correção) | ✅ coletada | Sessão `8c4394a3`; 2 intervenções (Tela 3 design `S2` e esclarecimento); **a mensagem do Modo Avião não foi enviada** (D-027); 0 `PROCESSO:`; `div_otel` anotado |
> | A8 RF04 — sessão 24 (correção) | ✅ coletada | Sessão `ed8c084a`; Modo Avião `S2` com a frase do D-025; a falha passou a aparecer, mas "tentar novamente" não funciona; 1 aviso de prefixo (D-027: valem 3 intervenções); 1 `PROCESSO:` |
> | A8 RF04 — sessões 25 e 26 (correção) | ✅ coletadas | `63691097` (Tela 1, cursor do carregamento, `S2`) e `39a9982a` (Tela 3, ícone, `S1`); 1 intervenção cada; enviadas em sessões separadas (D-028) |
> | A8 RF04 — fechamento (20/10) | ⚠️ `rf-incompleto` | Por decisão do pesquisador (D-026): critério 2 (nova tentativa depois da falha) não atendido. Commit `564dd97`, tag `cicloA/rf04-incompleto` |
> | A9 RF10 — sessão 1 `specify` (21/10) | ✅ coletada | Sessão `38f3d474`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | A9 RF10 — sessão 2 `clarify` (21/10) | ✅ coletada | Sessão `afa2a73b`; 1 intervenção (`esclarecimento não solicitado`, pergunta de preferência sobre o toque no botão já salvo; esperado `PROCESSO:` com a frase padrão, §5.3: D-030), 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A9 RF10 — sessão 3 `plan` (21/10) | ✅ coletada | Sessão `55aaefc3`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | A9 RF10 — sessão 4 `checklist` (21/10) | ✅ coletada | Sessão `ee379333`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel`; 22 itens (CHK001–CHK022) |
> | A9 RF10 — sessão 5 `tasks` (21/10) | ✅ coletada | Sessão `13d3f6b3`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado; 46 tarefas em 7 fases |
> | A9 RF10 — sessão 6 `analyze` (21/10) | ✅ coletada | Sessão `f244d4d2`; 0 intervenções, 1 `PROCESSO:` (oferta de remediação, resposta `Yes, proceed` em vez do texto do RDR nº 1: D-029); timebox < 50%; `div_otel` anotado. Relatório: 10 FR, 5 SC, 46 tarefas, **0 CRITICAL, 1 HIGH, 1 MEDIUM, 1 LOW**; C1 e I1 remediados na sessão (T024a–T024d e novo teste de arquitetura), E1 sem remediação |
> | A9 RF10 — sessão 7 `implement` (1ª rodada, 21/10) | ✅ coletada | Sessão `f88b5459`; 0 intervenções, 1 `PROCESSO:` (RDR nº 2); timebox < 50%; sem `div_otel`; 468 testes passam; abertas as tarefas manuais T027, T031, T037, T040 e T045 (do pesquisador, P6(d)) |
> | A9 RF10 — sessão 8 `converge` (1ª rodada, 22/10) | ✅ coletada | Sessão `778aacfa`; **Converged na 1ª rodada** (1 rodada `implement`/`converge`); 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | A9 RF10 — P6 rodada 1 | ⚠️ (b), (c) e (d) 1–4 OK; design com diferença | Botão de salvar encostado na borda da tela (spinner cortado) e rente à base do balão; estado salvo e mensagem longa conferidos: balão do usuário com a mesma largura do balão da IA → 1 sessão de correção, 1 intervenção (D-019) |
> | A9 RF10 — sessão 9 (correção, 22/10) | ✅ coletada | Sessão `51413b81`; 1 intervenção (`correção|S2|prd`, Tela 1: posição do botão e largura do balão), 0 `PROCESSO:`; timebox < 50%. Nova P6 pendente |
> | A9 RF10 — P6 rodada 2 | ✅ passou tudo | Segundo o pesquisador; prints da conferência de design dispensados por ele |
> | **A9 RF10 concluída (22/10)** | ✅ | HEAD do ciclo `6ac66b8`, tag `cicloA/rf10-done` (já existia quando o `concluir-rf` rodou de novo; registro único), dados em `c7b4cb5`; 9 sessões (6 do fluxo, 1 laço de 1 rodada, 1 de correção; 1 `esclarecimento não solicitado` + 1 `correção|S2|prd`; D-029) |
> | A10 RF08 — sessão 1 `specify` | ✅ coletada | Sessão `eb886618`; 0 intervenções, 0 `PROCESSO:` (o agente não fez perguntas Q1–Q3: resolveu 3 ambiguidades por conta própria e as documentou no `spec.md`); timebox < 50%; `div_otel` anotado. `specs/009-chat-proactive-insight` |
> | A10 RF08 — sessão 2 `clarify` | ✅ coletada | Sessão `37b48e43`; 0 perguntas, `spec.md` sem alteração; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado |
> | A10 RF08 — sessão 3 `plan` | ✅ coletada | Sessão `d88818e5`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel`; 13 decisões de pesquisa, 2 contratos, 6 cenários manuais |
> | A10 RF08 — sessão 4 `checklist` (22/10) | ✅ coletada (⚠️ D-030) | Sessão `323de508`; 2 intervenções `esclarecimento não solicitado` (perguntas de preferência do painel; esperado `PROCESSO:` com a frase padrão, §5.3), 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | A10 RF08 — sessão 5 `tasks` (22/10) | ✅ coletada | Sessão `3b6b3789`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel`; 42 tarefas em 7 fases (T001–T042) |
> | A10 RF08 — sessão 6 `analyze` (22/10) | ✅ coletada | Sessão `e1a34582`; 0 intervenções, 1 `PROCESSO:` (oferta de remediação, RDR nº 1; texto exato e resposta à pergunta seguinte a confirmar); timebox < 50%; `div_otel` anotado. Relatório: 17 requisitos, 42 tarefas, **1 CRITICAL, 1 MEDIUM, 1 LOW**; D1 (desvio documentado do RNF01: sem indicador de carregamento no insight) e F1 remediados na sessão, E1 (checklist desmarcado, 28 itens) sem remediação |
> | A10 RF08 — sessão 7 `implement` (1ª rodada, 22/10) | ✅ coletada (⚠️ D-031) | Sessão `2ddfbaf0`; 0 intervenções, 1 `PROCESSO:` (RDR nº 2; texto exato a conferir no fechamento); timebox < 50%; 517 testes passam; aberta a tarefa manual T042 (6 cenários no aparelho, do pesquisador, P6(d)); coleta chamada duas vezes por engano (D-031) |
> | A10 RF08 — sessão 8 `converge` (1ª rodada, 23/10) | ✅ coletada | Sessão `412b8a9f`; **Converged na 1ª rodada** (1 rodada `implement`/`converge`); 0 intervenções, 0 `PROCESSO:`; timebox < 50% (faixa possivelmente superestimada: D-031); sem `div_otel` |
> | A10 RF08 — P6 rodada 1 (24/10) | ⚠️ (a)–(c) OK; (d) 1, 3 e 4 OK, **2 falhou** | O cartão do insight não apareceu na espera de 2 min (critério falha em parte; o item 3 fica inconclusivo até o disparo por inatividade funcionar); design: lombada ocre reta fora dos cantos arredondados do cartão (S1) |
> | A10 RF08 — sessão de correção `f6f50aaf` (24/10) | ❌ não medida (D-032) | Aberta fora do `CLAUDE_CONFIG_DIR` do ciclo; não coletada; código desfeito pelo *rewind* (conferido: 517 testes, mesmas 20 entradas no `git status`); correção refeita em sessão válida |
> | A10 RF08 — sessão 9 (correção, 24/10) | ✅ coletada | Sessão `20f022dc`; 2 intervenções (`correção|S2|prd`: gatilho por inatividade na 1ª mensagem de conversa nova; `correção|S1|prd`: lombada do cartão), 0 `PROCESSO:`; timebox < 50%. Nova P6 pendente |
> | A10 RF08 — P6 rodada 2 (24/10) | ✅ passou tudo | Segundo o pesquisador; design do cartão (lombada nos cantos) conferido por mim no print |
> | **A10 RF08 concluída (24/10)** | ✅ | HEAD do ciclo `deb8c00`, tag `cicloA/rf08-done`, dados em `ca65282`; 9 sessões medidas (6 do fluxo, 1 laço de 1 rodada, 1 de correção) + 1 sessão de correção não medida (D-032); 4 intervenções (2 `esclarecimento não solicitado` no `checklist` e 2 `correção`); D-030, D-031, D-032, D-033 |
> | A11 RF05 — sessão 1 `specify` | ✅ coletada | Sessão `4890c50d`; 0 intervenções, 0 `PROCESSO:` (o agente não fez perguntas Q1–Q3: resolveu 1 ambiguidade por conta própria e a deixou nas premissas); timebox < 50%; sem `div_otel`. `specs/010-personal-summary-export` |
> | A11 RF05 — sessão 2 `clarify` | ✅ coletada | Identificador a conferir nos dados; 1 pergunta (estado de falha definitiva da folha de exportação), 1 `PROCESSO:` (texto exato a conferir), 0 intervenções; o agente encerrou o laço depois da frase padrão (método); timebox < 50%; `div_otel` anotado |
> | A11 RF05 — sessão 3 `plan` | ✅ coletada | Sessão `bd697138`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; `div_otel` anotado; 8 decisões de pesquisa, 4 contratos, dependência nova `share_plus`, sexto estado da folha |
> | A11 RF05 — sessão 4 `checklist` | ✅ coletada | Sessão `a2d891ce`; 0 intervenções, 2 `PROCESSO:` (preferência, frase padrão; texto exato a conferir); timebox < 50%; sem `div_otel`; 27 itens (CHK001–CHK027); 2 achados do agente no `spec.md` ("cinco estados" contra o sexto estado; toque repetido com dois comportamentos) |
> | A11 RF05 — sessão 5 `tasks` | ✅ coletada | Sessão `339c17a6`; 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel`; 48 tarefas em 6 fases (T001–T048) |
> | A11 RF05 — sessão 6 `analyze` | ✅ coletada | Sessão `2b706648`; 0 intervenções, 1 `PROCESSO:` (oferta de remediação, RDR nº 1; texto exato a conferir); timebox < 50%; sem `div_otel`. Relatório: 13 FR, 5 SC, 48 tarefas, **1 CRITICAL, 1 HIGH, 1 MEDIUM**; os três remediados na sessão (agora 50 tarefas); sem pergunta espontânea depois |
> | A11 RF05 — sessão 7 `implement` (1ª rodada) | ✅ coletada | Identificador a conferir; 0 intervenções, 1 `PROCESSO:` (RDR nº 2; texto exato a conferir); timebox < 50%; 586 testes passam; dependência nova `share_plus`; abertas as tarefas manuais T032, T041, T044 e T048 (do pesquisador, P6(d)) |
> | A11 RF05 — sessão 8 `converge` (1ª rodada) | ✅ coletada | Sessão `d6c75ef4`; **Converged na 1ª rodada** (1 rodada `implement`/`converge`); 0 intervenções, 0 `PROCESSO:`; timebox < 50%; sem `div_otel` |
> | **Próximo:** A11 — RF05, P6 (a)–(d) | — | — |

> **Onde este documento mora:** fora do VS Code do ciclo (celular, navegador ou outro editor). Ele descreve métricas e protocolo — **nunca** pode ser aberto, colado ou citado dentro de uma sessão medida.

---

## Sumário

0. Como usar este documento
1. Mapa dos repositórios e ambientes
2. Antes de começar — decisões e correções necessárias
3. Preparação única (antes do `A-001`)
4. Anatomia de uma sessão medida
5. Como escrever ao agente
6. Tempo, timebox e pausas
7. A0 — Instalação e baseline
8. A1 — Setup (constitution)
9. Bloco-padrão de unidade
10. Fichas das unidades (A2–A12)
11. Matriz de métricas — o que é coletado, quando e por quem
12. Git, tags e backup
13. Exceções e recuperação
14. Encerramento do Ciclo A
15. Transição A → B
16. Calendário
- Apêndice A — Comandos prontos
- Apêndice B — Correções em relação ao `plano-ciclos.md` (Parte II)
- Apêndice C — Pendências abertas que afetam o ciclo ou a Parte IV
- Apêndice D — Textos propostos para `docs/desvios.md` e `docs/rdr.md`

---

## 0. Como usar este documento

### 0.1 Legenda de responsabilidade

| Marca | Quem faz | Onde |
|---|---|---|
| 🧑 **[MANUAL]** | Você (Wagner), à mão | Terminal do Mac, painel do Supabase, iPhone |
| 🤖 **[AGENTE]** | O agente medido (Claude Code com `claude-sonnet-5`), dentro da sessão | VS Code aberto por `abrir-ciclo a` |
| ⚙️ **[SCRIPT]** | Um script de `cerne-avaliacao/scripts/`, rodado por você no terminal | Terminal do Mac |
| 📏 **[COLETA]** | Ato que grava dado do experimento (`/coletar-sessao`, tag, registro em `tags.csv`) | Sessão ou terminal |
| 🧪 **[SESSÃO]** | Sessão medida: tudo o que acontece nela vira dado | VS Code do ciclo |
| 🔴 **[PORTÃO]** | Parar e conferir antes de seguir | — |
| ⚠️ | Armadilha conhecida | — |

**Ninguém além do agente medido trabalha dentro das sessões.** Nenhum outro agente (inclusive o Claude de `cerne-avaliacao`) participa, sugere texto para o chat da sessão ou lê o código do ciclo durante o ciclo. O que vier de fora entra só pelas regras da seção 5 (pacote de entrada, RDR, sintomas).

### 0.2 As três peças que você toca em todo dia de ciclo

1. **Terminal do Mac** — scripts, `git`, `fvm flutter`, coletor OTel.
2. **VS Code do ciclo** — aberto só por `abrir-ciclo a`; nele só existe o painel do Claude Code com a sessão medida.
3. **iPhone 16 Pro** (`00008140-000125D13C2A801C`) — verificação de "concluído" (P6).

### 0.3 IDs de coleta usados no Ciclo A

| ID | Quando |
|---|---|
| `SETUP` | Sessão do `/speckit-constitution` (A1) |
| `F000` | Todas as sessões da fundação (A2) |
| `RF01`…`RF10` | Todas as sessões da unidade do RF, inclusive correções |
| `PLAN` | **Nunca** no Ciclo A (linha zerada por construção) |

---

## 1. Mapa dos repositórios e ambientes

```
cerne-backend ──► cerne-backend-handoff ──► cerne-avaliacao (laboratório)
 (código,          (só documentação)          │  entrada/ ──cópia──► cerne-ciclo-a/docs/input/
  congelado)                                  │  prompts/ ──colados no chat (tabela de entrega)
     │                                        │  scripts/ ──operam cerne-ciclo-a e o Supabase
     │ deploy                                 │  dados/cicloA/ ◄── /coletar-sessao e scripts
     ▼                                        ▼
 Supabase "ciclo-a" (fgzqqkwxwfxlxbdktwzo) ◄── app do cerne-ciclo-a (chamadas HTTP) 
```

| Peça | Papel no Ciclo A | Quem toca | Pode / não pode |
|---|---|---|---|
| `cerne-backend` (`$CERNE_BACKEND_DIR`) | Fonte dos scripts usados por `reset-ambiente` (seed, worker, cache) | ⚙️ wrappers | **Nunca** alterar (D1–D18, `backend-v1.0-frozen`). Defeito → política D16 (seção 13) |
| `cerne-backend-handoff` | Documentação original (pt-BR). Já traduzida e neutralizada em `entrada/backend/` | ninguém | Não entra no ciclo |
| `cerne-avaliacao` (`$AVAL`) | Laboratório: scripts, skill, prompts, dados, RDR, desvios | 🧑 terminal | **Nunca** aberto no VS Code do ciclo nem citado numa sessão |
| `cerne-ciclo-a` (`$CERNE_CICLO_A_DIR`) | O app. O agente trabalha só aqui | 🤖 + ⚙️ | Você não edita nenhum arquivo (seção 5.6) |
| Supabase `ciclo-a` | Backend hospedado do ciclo (23 Edge Functions + Postgres), `REPLAY_MODE=replay` | o app; ⚙️ wrappers | Não rodar `reset-ambiente` durante o ciclo (apaga suas entradas de teste) |
| `~/cerne/cfg-ciclo-a/` | `CLAUDE_CONFIG_DIR` do ciclo: `settings.json` congelado + skill `coletar-sessao`; transcripts em `projects/` | Claude Code | Não editar durante o ciclo |
| `~/cerne/otelcol/` | Coletor OpenTelemetry local (conferência da M3) | 🧑 inicia | Deve estar rodando durante as sessões |
| iPhone 16 Pro | Ambiente único de desenvolvimento e verificação (P11 revisado) | 🧑 | **Sem** certificado do mitmproxy e **sem** proxy no Wi-Fi durante o ciclo (`C-024`) |

**Fluxo de dados de uma sessão:** sessão no VS Code → `/coletar-sessao <ID>` → `scripts/coletar_sessao.py` lê o transcript em `~/cerne/cfg-ciclo-a/projects/<slug-do-repo>/<sessão>.jsonl` (+ subagentes) e `~/cerne/otelcol/output.jsonl` → grava `dados/cicloA/{sessoes,segmentos,intervencoes,revisoes_processo,avisos_coleta}.csv` e copia os JSONL para `dados/cicloA/brutos/`. Tags → `dados/cicloA/tags.csv`.

---

## 2. Antes de começar — decisões e correções necessárias

A conferência deste plano contra as ferramentas e os repositórios reais encontrou seis pontos em que seguir o plano como estava **não daria certo**. **Todos foram decididos por você em 01/10/2026 (opção ⭐ em todos) e já estão registrados em `docs/desvios.md` (D-001 a D-008) e aplicados no repositório** — commit `6c9686d`, branch `claude/wizardly-clarke-xj5ade`. O texto abaixo explica cada um.

Na execução da seção 3 (07/10/2026) apareceram mais dois achados, também decididos e registrados: **D-009** (o Claude Code gravou `"theme": "dark"` nos dois `settings.json` — hash novo `db5d321b…91e2`; skills da conta do claude.ai sincronizadas só no `cfg-ciclo-a`, removidas) e **D-010** (macOS e iOS 27.0.1 adotados; atualizações automáticas desligadas no Mac, na App Store e no iPhone).

No pré-voo de 08/10/2026 apareceram mais dois: **D-011** (`.DS_Store` criados pelo Finder sujavam o `git status` e entrariam nos commits de fechamento; gitignore global da máquina) e **D-012** (as pastas `synced` de skills e plugins da conta voltaram ao `cfg-ciclo-a` durante o `GATE-A02`; a sincronização é desligada nos dois `settings.json`, novo hash `3904700b…5922`; reconferência `GATE-A02b`, seção 7.3b).

Em 11/10/2026: **D-013** (os conectores do claude.ai — linha `MCP tools` do `/context`, 634 tokens: Claude Docs, Gmail, Google Calendar — também chegam ao contexto do agente medido; `"disableClaudeAiConnectors": true` nos dois `settings.json`, hash vigente `0112786e…f393`; reconferência `GATE-A02c`, seção 7.3c).

### 2.1 🔴 BLOQUEANTE — `P-SETUP` contradiz o contrato da API (autenticação) — ✅ decidido

**Achado.** O `P-SETUP` (congelado) diz ao agente: *"Send `SUPABASE_ANON_KEY` as the `Authorization: Bearer <key>` header … on every call … After login, keep using the same anon key for Edge Function invocation; the user's own session token is a separate concern"*. Mas o contrato entregue (`docs/input/backend/api/openapi.yaml`) marca **20 dos 23 endpoints** com `bearerAuth` (JWT do usuário), e o gateway do backend (`_shared/gateway.ts`, `authenticate()`) lê **só** o `Authorization` para identificar o usuário. Seguindo o `P-SETUP` ao pé da letra, toda chamada autenticada recebe `AUTH_INVALID`. Só `auth-signup`, `auth-login` e `auth-refresh` são públicos. (O `GATE-C18` já tinha confirmado na prática: `entries-list` só respondeu 200 com o token do usuário.)

**Por que importa:** o `P-SETUP` vira a constitution na A1 e as regras do `bmad-project-context` na B1. Um erro do instrumento viraria intervenções `ctx` atribuídas aos agentes, nos dois ciclos.

- ⭐ **Corrigir agora, antes da A1** — nenhuma sessão rodou, então os dois ciclos recebem o mesmo texto corrigido (paridade preservada). Registrar o desvio D-001 (Apêndice D), editar o parágrafo, recalcular o hash de `prompts/` em `hashes-congelamento.md`. Texto proposto para o item "Backend" do `P-SETUP`:
  > Backend: already built and frozen. The app consumes its API as documented in `docs/input/backend/`. All AI features, including semantic search, are provided by the backend. Configuration and credentials come from a `.env` file at the project root, with exactly two variables: `FUNCTIONS_BASE_URL` and `SUPABASE_ANON_KEY`. Every call to `{FUNCTIONS_BASE_URL}/<function>` carries the header `apikey: <SUPABASE_ANON_KEY>`. The `Authorization: Bearer` header carries `SUPABASE_ANON_KEY` on the operations that need no user session (sign-up, login, refresh) and the user's access token on every operation marked `bearerAuth` in `docs/input/backend/api/openapi.yaml`.
- Alternativa: manter como está e declarar na monografia como armadilha simétrica do instrumento.

### 2.2 🔴 BLOQUEANTE — ninguém faz commit do trabalho do Ciclo A — ✅ decidido

**Achado.** No Spec Kit v1.0.10, criação de branch e commits ficam numa **extensão `git` opcional** (`specify init --extension git`), que não é instalada — e o protocolo proíbe extensões (§4, `GATE-C08`). Conferido no texto do `speckit-specify`: *"Branch creation is handled by the `before_specify` hook (git extension)"*; sem `.specify/extensions.yml`, nada acontece. O diretório da unidade é resolvido por `.specify/feature.json`, então todo o Ciclo A roda em `main`, **sem commits**. E `concluir-rf` só faz merge (se houver branch) e `git tag` no `HEAD`: a tag `cicloA/f000-done` apontaria para o commit `instalado`, **sem o código da unidade**. Toda a Parte IV (M4, M6, M7, M8, M12, M13, M14, M15, hold-out) lê as tags.

- ⭐ **"Commit de fechamento"**: antes de **toda** tag (`setup-done`, cada unidade, `final`), você grava o estado atual do repositório num commit, sem alterar conteúdo (seção 12.2). Equivale ao merge que o `concluir-rf` já faz e que o protocolo diz não ser intervenção (§3.5, regra 25). Registrar uma vez como procedimento acrescentado (D-002).
- Alternativa: instalar a extensão `git` do Spec Kit (contraria `GATE-C08`, reabre decisão congelada — não recomendado).

### 2.3 🔴 BLOQUEANTE — `concluir-rf a SETUP` falha; não há script para `setup-done` e `final`

`validar_id_rf` só aceita `F000`/`RF01`–`RF10`. **Decidido por você (01/10/2026): documentar o contorno, sem mexer em script congelado.** Comandos na seção 8.4 e 14 (`git tag` + `scripts/registrar_tag.py --tipo setup-done|final`, que já aceita esses tipos).

### 2.4 Perguntas espontâneas do agente que pedem informação ou escolha — ✅ decidido

**Lacuna do protocolo.** P5b só dispensa prefixo para **confirmações** ("sim", "pode seguir") e para colar um erro pedido. Respostas a pausas **previstas** levam `PROCESSO:`. Uma pergunta **espontânea** que pede informação ou escolha ("Should I use go_router or auto_route?") não cabe em nenhuma das duas — pela regra, vira intervenção.

- ⭐ Regra operacional (registrar uma vez como interpretação, D-003):
  1. Se a pergunta admite confirmação ("Shall I proceed with X?"): resposta neutra, sem prefixo: `Yes, proceed.`
  2. Se pede escolha de preferência: `INTERVENÇÃO [esclarecimento não solicitado]: Use your technical judgment, following the input package.`
  3. Se pede informação: responder pelo pacote/RDR (seção 5.4), com o mesmo prefixo do item 2, e acrescentar ao RDR.
  4. **Não vale para as pausas previstas da tabela do §5.3** (perguntas do `specify`, `clarify` e `checklist`): lá a preferência é `PROCESSO: Use your technical judgment, following the input package.` (D-030).

### 2.5 Modo de permissão do Claude Code

O `settings.json` congelado tem `permissions.allow: []`. Logo, **todo** comando de terminal, toda edição de arquivo e a própria coleta pedem permissão. P3 manda aprovar "só desta vez" e proíbe "não perguntar de novo".
- ⭐ Manter o modo padrão nos dois ciclos: **não** ativar "Auto-accept edits", "Bypass permissions" nem Plan mode (Shift+Tab). Cada aprovação é um clique em **Yes**. Fique perto do Mac durante as sessões longas (`implement`): a espera por você conta como tempo ativo até 30 min por intervalo (P5c).

### 2.6 Não bloqueantes, mas conhecidos (detalhe no Apêndice C)

- O script grava a fase das **sessões de correção** como `SETUP` (o protocolo diz `IMPL`). Os JSONL brutos ficam preservados, então dá para re-segmentar na Parte IV. Nada muda no ciclo.
- O nome com que o transcript registra os comandos do Spec Kit (`speckit-specify` × `/speckit-specify`) nunca foi visto numa sessão real. Se não bater com a tabela de fases, a segmentação sai toda `SETUP`. Há uma checagem única, cega a números, depois da A1 (seção 8.5).
- O modo `manual` do coletor ignora `--session-id` e pega o transcript **mais recente** do diretório atual (seção 4.6).
- A saída da coleta pode conter `Aviso: divergência com o OpenTelemetry acima da tolerância`. Isso é esperado: anote nas notas da unidade e não faça nada.

---

## 3. Preparação única (antes do `A-001`)

Tudo 🧑 [MANUAL], no terminal do Mac. Faça na ordem e marque cada item. Nenhuma sessão do Claude Code nesta seção.

### 3.1 `cerne-avaliacao` local na versão congelada

Os desvios e os planos chegam à `main` por PR (os de 01/10 e 07/10 já foram mesclados: #3, #4, #5). Antes de cada dia de ciclo, basta manter o `main` local igual ao GitHub:

```bash
TCC="/Users/wagnerduarte/Documents/Faculdade/2026.2/TCC"
AVAL="$TCC/cerne-avaliacao"
cd "$AVAL"
git checkout main
git pull origin main
git fetch --tags
git tag --list 'protocolo-v1.0'          # deve imprimir: protocolo-v1.0
git diff --stat protocolo-v1.0 -- docs/protocolo.md docs/Metricas_e_Skills_Ciclos.md entrada prompts holdout harness scripts skills
```
**Critério:** o último comando lista **só** `prompts/P-SETUP.md` (D-001) e `scripts/faixa-plan` (D-004) — as duas diferenças documentadas em `desvios.md`. Conferir também: `shasum -a 256 prompts/P-SETUP.md` → `6c040ea1852cfaccb77c59cd9091435a98695b081de8d4e0f5f2109faecbca65` e `"$AVAL/scripts/faixa-plan"` → `Timebox do planejamento (B2–B4): abaixo de 50%.` (✅ conferido em 07/10/2026)

### 3.2 Variáveis de ambiente permanentes

```bash
ls -d "$TCC"/cerne-ciclo-a "$TCC"/cerne-ciclo-b "$TCC"/cerne-backend   # os três devem existir
```
Se algum não existir nesse caminho, use o caminho real onde você clonou (no `GATE-C17`) nos comandos abaixo.
```bash
cat >> ~/.zshrc <<'EOF'
# --- TCC Cerne: ciclos comparativos ---
export TCC="/Users/wagnerduarte/Documents/Faculdade/2026.2/TCC"
export AVAL="$TCC/cerne-avaliacao"
export CERNE_CICLO_A_DIR="$TCC/cerne-ciclo-a"
export CERNE_CICLO_B_DIR="$TCC/cerne-ciclo-b"
export CERNE_BACKEND_DIR="$TCC/cerne-backend"
export IPHONE="00008140-000125D13C2A801C"
EOF
source ~/.zshrc
echo "$CERNE_CICLO_A_DIR"; git -C "$CERNE_CICLO_A_DIR" log --oneline 2>&1 | head -3
```
**Critério:** o caminho aparece; o `git log` diz que não há commits (`does not have any commits yet`). Se já houver commits (por exemplo, se você rodou `iniciar-ciclo` antes deste documento), pare e me diga — não siga.

### 3.3 `abrir-ciclo` aponta para o repositório real

O comando é **`abrir-ciclo a`** (com espaço: `a` é o argumento), não `abrir-ciclo-a`. Ele (1) recusa rodar com o VS Code aberto, (2) exporta `CLAUDE_CONFIG_DIR=~/cerne/cfg-ciclo-a` e (3) abre o VS Code na pasta `cerne-ciclo-a`. Abrir o VS Code de outro jeito (Dock, `code .`) faria o Claude Code usar a sua configuração pessoal (`~/.claude`): modelo, raciocínio e permissões errados e transcripts num lugar onde a coleta não acha.

> **Achado de 07/10/2026:** a versão antiga procurava o repositório em `~/cerne/cerne-ciclo-a` (não existe) e, sem achar, rodava `code -n .` — abriria **a pasta corrente do terminal**. Rodada de dentro de `cerne-avaliacao`, a sessão medida teria aberto no laboratório. Substituída pela versão abaixo (✅ 07/10/2026).

O `abrir-ciclo` foi escrito na Fase 4, **antes** de `cerne-ciclo-a` existir, com um modo de "cai para `code -n .`". Ele nunca foi testado contra o repositório real.
```bash
cat ~/cerne/bin/abrir-ciclo
```
⭐ Substituir pela versão abaixo (não é arquivo congelado), que usa as variáveis da 3.2 e falha alto se algo estiver errado:
```bash
cat > ~/cerne/bin/abrir-ciclo <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
CICLO="${1:-}"
case "$CICLO" in
  a) DIR="${CERNE_CICLO_A_DIR:?defina CERNE_CICLO_A_DIR}"; CFG="$HOME/cerne/cfg-ciclo-a" ;;
  b) DIR="${CERNE_CICLO_B_DIR:?defina CERNE_CICLO_B_DIR}"; CFG="$HOME/cerne/cfg-ciclo-b" ;;
  *) echo "uso: abrir-ciclo <a|b>" >&2; exit 1 ;;
esac
[[ -d "$DIR/.git" ]] || { echo "Repositório não encontrado: $DIR" >&2; exit 1; }
[[ -f "$CFG/settings.json" ]] || { echo "settings.json ausente em $CFG" >&2; exit 1; }
if pgrep -x "Code" >/dev/null || pgrep -f "Visual Studio Code.app/Contents/MacOS" >/dev/null; then
  echo "O VS Code já está aberto. Feche-o por completo (Cmd+Q) e rode de novo." >&2; exit 1
fi
export CLAUDE_CONFIG_DIR="$CFG"
echo "Abrindo $DIR com CLAUDE_CONFIG_DIR=$CFG"
exec code -n "$DIR"
EOF
chmod +x ~/cerne/bin/abrir-ciclo
```
**Por que exigir o VS Code fechado:** uma janela nova num VS Code que já está aberto pode herdar o ambiente do processo antigo, sem o `CLAUDE_CONFIG_DIR` do ciclo. Isso misturaria as configurações, que deveriam ficar isoladas (P2).

### 3.4 Skill de coleta atualizada nos dois diretórios de config

```bash
diff "$AVAL/skills/coletar-sessao/SKILL.md" ~/cerne/cfg-ciclo-a/skills/coletar-sessao/SKILL.md && echo OK-a
diff "$AVAL/skills/coletar-sessao/SKILL.md" ~/cerne/cfg-ciclo-b/skills/coletar-sessao/SKILL.md && echo OK-b
```
**Critério:** `OK-a` e `OK-b`. Se houver diferença, copie de novo: `cp "$AVAL/skills/coletar-sessao/SKILL.md" ~/cerne/cfg-ciclo-a/skills/coletar-sessao/SKILL.md` (idem `cfg-ciclo-b`).

**Skills da conta (D-009).** A conta do claude.ai sincroniza skills próprias (`aula`, `docs`, `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`…) para dentro do diretório de configuração. Em 07/10/2026 elas estavam só no `cfg-ciclo-a` (assimetria). Os dois diretórios só podem ter a `coletar-sessao`:
```bash
ls ~/cerne/cfg-ciclo-a/skills ~/cerne/cfg-ciclo-b/skills      # só coletar-sessao nos dois
ls ~/cerne/cfg-ciclo-a/plugins ~/cerne/cfg-ciclo-b/plugins    # sem pasta synced
```
Se aparecer `synced`, **pare**. A pasta já voltou uma vez sozinha (criada durante a sessão do `GATE-A02`, porque o Claude Code baixa as skills da conta em segundo plano a cada início de sessão; o painel do `/context` mostra só categorias, sem nomes, e não prova ausência). A solução vigente é o **D-012**: os dois `settings.json` têm `"syncClaudeAiSkills": false` e `"syncClaudeAiPlugins": false`. Desligar skills na conta **não** resolve (`pdf` e `xlsx` sincronizam sempre). A pasta `.trash` que o Claude Code cria ao mover o que já tinha baixado não é problema: nada ali é carregado.

### 3.5 `settings.json` intacto

```bash
shasum -a 256 ~/cerne/cfg-ciclo-a/settings.json ~/cerne/cfg-ciclo-b/settings.json
```
**Critério:** os dois `0112786e12fbe0917221c8d09f17f9f4b9c022d5ef811b9123b9fb9b0a62f393` (hash vigente desde o D-013, 11/10/2026: o de 08/10, `3904700b…5922` (D-012), mais `"disableClaudeAiConnectors": true`; antes disso `db5d321b…91e2` (D-009); o original congelado era `fdb46287…5369`).

### 3.6 Versões travadas (P8, §6 do protocolo)

```bash
sw_vers -productVersion        # 27.0.1 (build 26A434; D-010 — era 27.0)
xcodebuild -version            # Xcode 27.0 / Build version 27A266a
fvm flutter --version          # Flutter 3.47.5 • channel stable … Dart 3.13.4
claude --version               # 2.1.282
code --version | head -1       # 1.139.1
specify version 2>/dev/null | grep -i "cli version" ; which specify   # 1.0.10 ; ~/.local/bin/specify
uv --version                   # uv 0.12.19
node -v                        # v26.10.0
```
**Critério:** todos iguais. Qualquer diferença: **parar** (atualização acidental muda o ambiente entre ciclos). O aviso "A new version of Flutter is available!" é esperado: **nunca** rode `flutter upgrade`.

Avisos de versão nova do **Supabase CLI** (ex.: "v2.120.0 available") também são ignorados: nada é atualizado até 13/11.

**Atualizações automáticas desligadas (D-010)** — conferir:
```bash
defaults read /Library/Preferences/com.apple.SoftwareUpdate | grep -E "AutomaticCheckEnabled|AutomaticDownload|AutomaticallyInstallMacOSUpdates|CriticalUpdateInstall|ConfigDataInstall"   # todas = 0
defaults read /Library/Preferences/com.apple.commerce AutoUpdate     # 0 (App Store, inclui o Xcode)
```

### 3.7 Backend `ciclo-a`

1. **"Confirm email" desligado.** Painel do Supabase → projeto `ciclo-a` → Authentication → Providers (ou Sign In / Providers) → Email → **Confirm email: OFF**. Sem isso, o cadastro da F000 não devolve sessão: o agente receberia um sintoma que não é culpa dele. (Achado do roteiro de congelamento do backend, Passo 5.) Faça o mesmo no projeto `ciclo-b` agora, para não esquecer.
2. **`REPLAY_MODE=replay`** (estratégia do `GATE-C19` para o desenvolvimento). Já foi definido em 29/09; para garantir:
   ```bash
   cd "$AVAL" && scripts/replay-mode a replay      # digite: sim
   ```
3. **Não** rodar `reset-ambiente` agora: o `ciclo-a` está no estado do seed desde 29/09 (`C-015`).

### 3.8 iPhone no estado de desenvolvimento (`C-024`, sentido "desenvolvimento")

- Ajustes → Wi-Fi → (i) da rede → Configurar Proxy: **Desligado**.
- Ajustes → Geral → VPN e Gerenciamento de Dispositivo: **nenhum** perfil do mitmproxy (só o certificado de desenvolvedor "Apple Development: wagnerofduarte@gmail.com").
- Modo Desenvolvedor ligado; cabo conectado ou pareamento sem fio ativo.
```bash
fvm flutter devices | grep -i "$IPHONE"
```
**Critério:** o iPhone aparece na lista, com **iOS 27.0.1 (24A446)** (D-010). Atualizações automáticas do iOS desligadas: Ajustes → Geral → Atualização de Software → Atualizações Automáticas (todas desligadas).

### 3.9 Coletor OpenTelemetry

**O que é:** durante as sessões, o Claude Code envia sozinho a sua telemetria (contagens de tokens e eventos) para `localhost:4317` — está ligado no `settings.json` dos dois ciclos. O coletor (`otelcol-contrib`, instalado no `C-013`) recebe esses dados e grava em `~/cerne/otelcol/output.jsonl`. A fonte principal da M3 é o transcript; o OTel é a **segunda fonte, de conferência**: a coleta compara as duas e grava a diferença (`div_otel`), o que acusa, por exemplo, tokens de subagente não contados (`GATE-C03`).

**Antes de cada dia de sessões**, numa janela própria do Terminal (deixe aberta enquanto houver sessões; reinício do Mac ou janela fechada → rode de novo):
```bash
~/cerne/otelcol/otelcol-contrib --config ~/cerne/otelcol/config.yaml
```
Conferir se está ligado: `lsof -nP -iTCP:4317 -sTCP:LISTEN` → uma linha `otelcol-c … 127.0.0.1:4317 (LISTEN)` (✅ 07/10/2026). O coletor só serve de conferência (`div_otel`). Se ele não estiver rodando, a coleta funciona do mesmo jeito, com `div_otel` vazio — anote o dia nas notas. Nunca abra `~/cerne/otelcol/output.jsonl` (tem números de tokens).

### 3.10 Registro da assinatura (P13)

Anote em `plano-ciclos.md`, na A0: o plano da assinatura do Claude e os limites vigentes hoje (texto da página de uso/planos). Só o plano e os limites, nunca o consumo. ✅ 07/10/2026: plano **Pro**. ✅ 11/10/2026: a página de planos traz só "More usage*" (sem tipos de limite); registrado em `plano-ciclos.md` com o print em `dados/evidencias/`. Os limites que cortarem sessões entram nas notas das unidades.

### 3.11 Decisões da seção 2 registradas

- [x] D-001 a D-010 decididos e registrados em `desvios.md`; `P-SETUP` corrigido; hashes atualizados; tudo na `main`.
- [x] Seções 3.1–3.10 conferidas com as saídas reais da máquina (07/10/2026).
- [ ] Este documento aberto **fora** do VS Code (navegador ou celular, pelo GitHub).

---

## 4. Anatomia de uma sessão medida

Esta é a rotina de **toda** sessão 🧑🤖🧪 do ciclo, inclusive as de correção.

### 4.1 Antes de abrir

1. 🧑 Coletor OTel rodando (3.9).
2. 🧑 VS Code **fechado** por completo (Cmd+Q).
3. 🧑 No terminal: `abrir-ciclo a` (com espaço; seção 3.3).
4. 🧑 No VS Code: abrir o painel do Claude Code e começar uma **conversa nova**. Nunca usar "continuar" ou retomar uma conversa anterior.
5. 🧑 Fechar **todos** os editores (Cmd+K W) e **desligar o anexo de contexto** (ícone de olho no campo de mensagem). Isso vale antes de **cada** mensagem (P2). Se o VS Code reabrir arquivos sozinho, feche-os de novo.

### 4.2 Durante

6. 🧑 Primeira mensagem = o comando da etapa, com o argumento indicado (seções 8–10). **Um comando por sessão** (P4). Nada antes do comando, nem "olá". ⚠️ **Forma (D-014):** **digite** `/speckit-<comando> ` à mão (com o espaço) e **depois cole** só o argumento (`cat prompts/P-….md | pbcopy`, Cmd+V). Nunca cole a mensagem inteira com o comando dentro: a extensão envolve a colagem em `<pasted_content>`, o comando não é expandido como slash command e o agente chama a skill por conta própria. Comandos sem argumento (`/speckit-tasks`) são só digitados.
7. 🤖 O agente trabalha. A cada pedido de permissão: 🧑 **Yes** ("só desta vez"). Nunca "Yes, and don't ask again". Se você precisar negar, a mensagem seguinte é `INTERVENÇÃO [permissão negada]: <o que foi negado e por quê>`.
8. 🧑 Quando o agente pausar: responder pelas regras da seção 5. ⚠️ **Se a pergunta vier no painel de opções (D-015):** **não clique** numa opção. Clique em **Other** e **digite** a resposta com `PROCESSO:` no início (ou `INTERVENÇÃO […]:` se for o caso). Opção clicada não tem prefixo e não conta como `PROCESSO:` nem como intervenção.
9. 🚫 Proibido na sessão: `/clear`, `/compact`, `/model`, `/effort`, `ultrathink`, Option+T, editar qualquer arquivo no editor, colar trechos deste documento, citar métricas, "o outro ciclo" ou `cerne-avaliacao`.
10. Compactação **automática** é permitida (o coletor registra). Não interfira.

### 4.3 Encerramento (📏 [COLETA])

11. 🧑 Quando o comando terminar (o agente dá o resumo final ou a pausa que encerra o comando), a **última** mensagem é exatamente:
    ```
    /coletar-sessao <ID>
    ```
    com o ID da unidade (`SETUP`, `F000`, `RF03`…). Sempre com o ID, nunca sem.
12. 🤖 A skill pede permissão para rodar `python3 …/coletar_sessao.py …` → 🧑 **Yes**. (Essa aprovação vem depois do corte e não entra nos dados.)
13. 🧑 Conferir a saída, que deve ser só isto:
    ```
    Registrado. Intervenções reconhecidas: N.
    Respostas PROCESSO reconhecidas: M.
    Timebox da unidade: abaixo de 50%.
    ```
    - `N` e `M` devem bater com as mensagens prefixadas que você digitou nesta sessão.
    - `Avisos (prefixo mal formado): K.` significa que uma mensagem sua começou com `INTERVEN…`/`PROCESSO…` e não foi lida. Anote nas notas da unidade (o texto fica em `avisos_coleta.csv`) e tenha cuidado nas próximas.
    - Se a skill **perguntar o ID**, responda só com o ID (por exemplo, `RF03`).
14. 🧑 Fechar a conversa/aba. **Nunca** retomar uma sessão em que a coleta rodou (`--continue`/`--resume` proibidos).

### 4.4 Depois

15. 🧑 Anotar nas notas da unidade (seção 9.6): data, comando, ID e algo que tenha chamado a atenção (sem números).
16. 🧑 Ao fim do dia: commit dos dados em `cerne-avaliacao`, **sem olhar o conteúdo** (seção 12.4).

### 4.5 Se o comando não terminar na sessão

Pode acontecer por limite de uso, queda da extensão ou o agente encerrar a vez sem concluir. Se a sessão ainda responde, colete normalmente (`/coletar-sessao <ID>`). A **próxima** sessão repete o **mesmo** comando (P4/P13). O Spec Kit retoma pelos artefatos em disco.

### 4.6 Sessão em que a skill não pode rodar (modo `manual`, P13)

Use quando o limite de uso foi atingido, a extensão travou ou você fechou a aba sem coletar. Rode no terminal **antes de abrir qualquer outra sessão no ciclo**: o script pega o transcript **mais recente** do repositório.
```bash
cd "$CERNE_CICLO_A_DIR"
ls -t ~/cerne/cfg-ciclo-a/projects/*/*.jsonl | head -1      # o nome do arquivo (sem .jsonl) é o session-id
CLAUDE_CONFIG_DIR=~/cerne/cfg-ciclo-a python3 "$AVAL/scripts/coletar_sessao.py" manual <ID> \
  --ciclo a --session-id <session-id> --motivo-fim <limite_uso|falha> \
  --versao-claude-code "$(claude --version)" --config-raciocinio high \
  --otel-output ~/cerne/otelcol/output.jsonl
```
- `limite_uso`: o limite da assinatura foi atingido.
- `falha`: queda, travamento ou esquecimento. Se foi esquecimento, anote isso nas notas da unidade.

No modo manual o corte é a **última** mensagem da sessão, e não há mensagem de invocação a excluir.

---

## 5. Como escrever ao agente

Toda mensagem sua numa sessão cai em **exatamente uma** destas categorias:

| Categoria | Quando | Forma | Conta como |
|---|---|---|---|
| **Comando** | Primeira mensagem da sessão | `/speckit-<comando> [argumento]`: comando **digitado**, argumento **colado** (D-014) | Marca a fase |
| **Neutra** (P5b) | Confirmar uma pausa **espontânea** do agente; colar um erro que ele pediu | Sem prefixo: `Yes, proceed.` / saída do erro | Nada |
| **PROCESSO** | Responder a uma pausa **prevista** pelo comando (lista 5.3) | `PROCESSO: <resposta em inglês>` | M5b (`revisoes_processo.csv`) |
| **INTERVENÇÃO** | Qualquer outra coisa | `INTERVENÇÃO [tipo\|campos]: <corpo em inglês>` | M5 (`intervencoes.csv`) |
| **Coleta** | Última mensagem | `/coletar-sessao <ID>` | Corte |

⚠️ O prefixo tem que ser o **início exato** da mensagem: maiúsculas, com `Ç` e `Ã`, colchetes, dois-pontos. `INTERVENÇÃO` e `PROCESSO:` ficam em português; o corpo vai em inglês (P12).

### 5.1 Formato da intervenção

`INTERVENÇÃO [tipo|campos]: <corpo>` — os campos são separados por `|`, nesta ordem:

| Tipo | Severidade (`S1`–`S3`) | Nível (`N1`/`N2`) | Causa |
|---|---|---|---|
| `correção` | obrigatória | — | obrigatória |
| `edição manual` | — | obrigatório | obrigatória |
| `redirecionamento` | — | — | obrigatória |
| `permissão negada` | — | — | opcional |
| `interrupção` | — | — | opcional |
| `esclarecimento não solicitado` | — | — | opcional |

- **Severidade:** `S1` cosmético (nenhum critério afetado) · `S2` funcional com contorno (critério falha em parte, fluxo utilizável) · `S3` bloqueante (critério impossível, crash ou perda de dados).
- **Nível:** `N1` ≤ 10% das linhas da mudança do agente que você corrigiu · `N2` > 10%.
- **Causa:** `ctx` incompatível com o repositório ou o backend (API, caminho, pacote ou convenção inexistente) · `chk` falha em teste, lint, análise ou build · `inc` implementação incompleta ou tarefa abandonada · `prd` desvio de requisito ou decisão de produto · `amb` ambiente, permissão ou ferramenta · `out` outra (descrever).

⚠️ O tipo tem que ser **uma** destas strings exatas, em minúsculas e com acento: `correção` · `edição manual` · `redirecionamento` · `permissão negada` · `interrupção` · `esclarecimento não solicitado`. Qualquer variação (`correcao`, `Correção`, `edicao manual`) não é reconhecida e vira só um aviso na coleta.

Exemplos válidos:
```
INTERVENÇÃO [correção|S2|prd]: On "Meus Registros", applying the "Áudio" filter and a date range shows entries of every type. Expected: only audio entries inside the range.
INTERVENÇÃO [redirecionamento|prd]: Section 2 of docs/input/requirements.md says the Action Plans screen receives no functional implementation.
INTERVENÇÃO [interrupção]: I pressed Esc because the session was stuck repeating the same failing command for 10 minutes.
```
Interrupção por Esc, edição manual ou permissão negada são ações fora do chat. **Sempre** mande uma mensagem prefixada logo depois, descrevendo o que aconteceu.

### 5.2 Correções: descrever o sintoma, nunca a solução (regra 10)

Modelo:
```
INTERVENÇÃO [correção|S<n>|<causa>]: Expected: <o que o critério ou o protótipo diz>. Actual: <o que acontece>. Where: <tela "texto do protótipo"> → <ação>. Error: <mensagem exata, se houver>.
```
Nunca nomeie arquivo, classe, pacote, método ou abordagem. "The app crashes when I tap 'Gravar'; Xcode shows: <erro>" está certo. "Add NSMicrophoneUsageDescription to Info.plist" está **errado** (dita a solução).

### 5.3 Pausas previstas do Spec Kit v1.0.10 (gatilhos `PROCESSO`)

Conferidas no texto dos comandos instalados:

| Comando | Pausa (texto real) | Como responder |
|---|---|---|
| `constitution` | Pode pedir valores que o `P-SETUP` não trouxe (ex.: data de ratificação: *"if unknown ask or mark TODO"*) | Pacote → RDR → decidir. Sugestão de RDR para a data: `PROCESSO: Use today's date.` |
| `specify` | Até 3 perguntas `[NEEDS CLARIFICATION]`, apresentadas juntas: *"Q1: A, Q2: Custom - …"* | Responder todas numa mensagem: `PROCESSO: Q1: A (requirements.md §1, RF04). Q2: …`. Se for preferência: `PROCESSO: Q1: Use your technical judgment, following the input package.` |
| `clarify` | **Uma pergunta por vez**, até 5. Múltipla escolha com `**Recommended:** Option X`, ou resposta curta (≤ 5 palavras) com `**Suggested:**` | Uma mensagem `PROCESSO:` por pergunta. Pacote cobre → a letra ou a resposta, citando a seção. Preferência → `PROCESSO: Use your technical judgment, following the input package.` (se o agente pedir para desambiguar, a próxima resposta é neutra: `recommended`). Para encerrar cedo, não diga "done" por conta própria: deixe o comando decidir |
| `checklist` (roda **depois** do `plan`, D-016) | Até 3 perguntas iniciais (Q1–Q3) sobre foco, profundidade e público, mais até 2 extras (Q4/Q5) | `PROCESSO:` com as respostas. Foco e profundidade são preferência → frase padrão |
| `analyze` | Fim do relatório: *"Would you like me to suggest concrete remediation edits for the top N issues?"* | ⭐ Sugestão de RDR: `PROCESSO: Yes.` Se o agente então perguntar **espontaneamente** se aplica as sugestões: neutra `Yes, proceed.` |
| `implement` | Se algum checklist tiver itens não marcados: *"Some checklists have unchecked items. Do you want to proceed with implementation anyway? (yes/no)"*. **Acontecerá em toda unidade**: os checklists do `/speckit-checklist` nascem desmarcados e você não pode editá-los | ⭐ Sugestão de RDR: `PROCESSO: yes` |
| `plan`, `tasks` | Nenhuma pausa prevista | Pausa espontânea → seção 2.4 |
| `converge` | **Não é gatilho** na v1.0.10. Só imprime o resumo e grava (ou reporta *Converged*) | — |

### 5.4 Respostas às pausas previstas — o RDR (regras 16–23, `GATE-C11`)

1. Toda resposta a uma pausa prevista começa com `PROCESSO:` e é em inglês.
2. Responder **só** com o que está no pacote (`docs/input/`), citando a seção.
3. Se o pacote não cobre: procurar uma pergunta equivalente em `$AVAL/docs/rdr.md`. Abra o RDR **no terminal ou noutro editor**, nunca no VS Code do ciclo. Se houver uma, usar **o mesmo texto**.
4. Se nem o pacote nem o RDR cobrem: decidir na hora, responder com uma frase curta, e **logo depois da sessão** acrescentar uma linha ao RDR (data, ciclo, unidade, comando, pergunta, fonte, resposta exata).
5. Pergunta de preferência ("A or B?"): `PROCESSO: Use your technical judgment, following the input package.`
7. **Painel de perguntas (D-015).** O Spec Kit pergunta, quase sempre, por um painel com opções e *Other*. Responda **sempre** por *Other*, digitando à mão `PROCESSO: …` (nunca clicando numa opção, nunca colando). O coletor lê essas respostas do campo `toolUseResult.answers` do transcript. Nas perguntas de preferência, a frase padrão pode levar o agente a encerrar o Q&A (visto no `clarify` da F000): isso é do método, não é intervenção.
6. As respostas sugeridas na 5.3 marcadas como "sugestão de RDR" só viram regra quando você as grava no RDR na primeira ocorrência. Depois disso, o mesmo texto vale para o resto do Ciclo A **e** para perguntas equivalentes do Ciclo B.

### 5.5 Se o agente começar algo fora do escopo

- Tela de extensão (Planos de Ação, seletor de persona, tags manuais): **uma** `INTERVENÇÃO [redirecionamento|prd]` apontando a §2 de `requirements.md` (P10).
- Alteração do backend, chamada direta a provedor de IA, valor visual fora de `design_tokens.dart` visto durante a sessão: `INTERVENÇÃO [redirecionamento|prd]` citando o item do `P-SETUP` ("Do not").

### 5.6 O que você nunca faz fora da sessão

- Editar arquivos do ciclo, inclusive `CLAUDE.md`, `.specify/`, `specs/`, `pubspec.yaml`, configurações do Xcode e `.gitignore`. Se for inevitável: `INTERVENÇÃO [edição manual|N1/N2|causa]` na sessão seguinte, descrevendo a edição (P5, regra 24).
- Rodar métrica: nada de `flutter test --coverage`, lints de arquitetura ou scripts do harness no código do ciclo.
- Olhar números: `sessoes.csv`, `segmentos.csv`, `custo_usd`, `output.jsonl` do OTel, painéis de uso do Claude (regra 15, cegamento).

---

## 6. Tempo, timebox e pausas

- **Tempo ativo (P5c):** soma dos intervalos do transcript. Os que terminam numa ação do agente contam inteiros. As esperas por você contam até **30 min** cada; o excedente vai para `pausa_s`. Pausas longas (almoço, noite) não estouram a timebox, mas também não feche uma sessão no meio de um comando por isso: colete antes de sair, se for passar muitas horas fora.
- **Timebox (P7):** 12 h para a F000 e 8 h por RF, somando **todas** as sessões da unidade (correções incluídas).
- **Como você acompanha:** a última linha de cada coleta traz a faixa — `abaixo de 50%` · `50-80%` · `acima de 80%` · `atingido`.
  - `acima de 80%`: priorize terminar o laço `implement` → `converge` e verificar a P6.
  - `atingido`: a unidade termina **agora**. Commit de fechamento → `rf-incompleto a <ID>` → a próxima unidade começa (seção 9.5). As unidades dependentes são tentadas mesmo assim; o bloqueio vai para as notas.
- **Tempo de calendário:** vem das tags (`tags.csv`). A verificação de "concluído" fora de sessão só aparece aqui.
- **Limite de uso da assinatura (P13):** o corte aparece como sessão `manual` com `limite_uso`. Anote a data e a hora do corte nas notas: as datas dos cortes vão para a monografia.

---

## 7. A0 — Instalação e baseline

**Data proposta:** 01/10/2026. **Executada em 07/10/2026** (✅ `A-001`, `GATE-A01`, `GATE-A02`).

### 7.1 `A-001` ⚙️📏 Baseline

```bash
cd "$AVAL"
scripts/iniciar-ciclo a
```
O script copia `entrada/` → `docs/input/` (15 arquivos) e `segredos/.env.ciclo-a` → `.env`, cria o `.gitignore` de uma linha (`.env`), confere os hashes arquivo a arquivo, faz o commit `Baseline: copy input package and .env scaffold`, cria a tag `cicloA/baseline` e registra em `dados/cicloA/tags.csv`.

**Critério:** termina com `== iniciar-ciclo a concluído: tag cicloA/baseline em <sha> ==` e `Hashes conferidos: 15 arquivos, todos idênticos.`
```bash
git -C "$CERNE_CICLO_A_DIR" ls-files | head -20     # docs/input/... e .gitignore; o .env NÃO aparece
grep -c "SUPABASE_ANON_KEY\|FUNCTIONS_BASE_URL" "$CERNE_CICLO_A_DIR/.env"   # 2
grep -c "service_role" "$CERNE_CICLO_A_DIR/.env"                             # 0
```

### 7.2 🔴 `GATE-A01` ⚙️📏 Instalar o Spec Kit (M1, parte "instalação")

Fora de qualquer sessão, no terminal:
```bash
cd "$AVAL"
scripts/instalar-metodologia a
```
Roda `specify init --here --force --non-interactive --integration claude` dentro de `cerne-ciclo-a`, cronometra, faz o commit `Install Spec Kit v1.0.10 scaffolding`, cria a tag `cicloA/instalado` e grava uma linha em `sessoes.csv` (`tipo_sessao=instalacao`, `modo_coleta=script`).

**Critério:**
```bash
ls "$CERNE_CICLO_A_DIR/.claude/skills"     # 10 pastas speckit-* (analyze, checklist, clarify, constitution, converge, implement, plan, specify, tasks, taskstoissues)
ls "$CERNE_CICLO_A_DIR/.specify"           # init-options.json integration.json integrations memory scripts templates workflows
test -f "$CERNE_CICLO_A_DIR/.specify/extensions.yml" && echo "ATENÇÃO: extensões presentes" || echo "sem extensões (correto)"
test -e "$CERNE_CICLO_A_DIR/CLAUDE.md" && echo "ATENÇÃO: CLAUDE.md existe" || echo "sem CLAUDE.md (correto)"
git -C "$CERNE_CICLO_A_DIR" tag             # cicloA/baseline cicloA/instalado
git -C "$CERNE_CICLO_A_DIR" status --short  # vazio
cut -d, -f2,4,5 "$AVAL/dados/cicloA/sessoes.csv"   # SETUP,instalacao,script (só colunas sem números)
```
`speckit-taskstoissues` vem instalado, mas fica **fora do fluxo** (§4.2) e nunca é chamado.

**Avisos esperados na saída do `specify init` (não são problema):**
- *"Current directory is not empty (4 items)"* — são `docs/`, `.gitignore`, `.env` e `.git`, do baseline.
- *"Consider adding .claude/ (or parts of it) to .gitignore"* — sugestão genérica. **Não** faça: mexer no `.gitignore` é edição manual.

Se o script der erro, **não rode de novo** (uma segunda execução duplica a linha de instalação da M1): guarde a saída e resolva antes.

### 7.2b 📏 Backup da A0

```bash
git -C "$CERNE_CICLO_A_DIR" push origin main --tags
cd "$AVAL" && git add dados && git commit -m "Ciclo A: baseline e instalação (<data>)" && git push origin main
```
O primeiro push cria `main`, `cicloA/baseline` e `cicloA/instalado` no GitHub (✅ 07/10/2026).

### 7.3 🔴 `GATE-A02` 🧑 Conferência de largada (sessão **não** medida)

1. `abrir-ciclo a` → painel do Claude Code → conversa nova.
2. Digitar só `/context` (nenhuma outra mensagem).
3. Conferir:
   - modelo `claude-sonnet-5`. Se aparecer outro, o `CLAUDE_CONFIG_DIR` não pegou: **pare**, revise 3.3;
   - skills: **só** `speckit-*` — nenhuma skill da conta (`aula`, `docs`, `pdf`…). Se aparecer alguma, a sincronização da conta voltou: **pare** (D-009, seção 3.4);
   - `coletar-sessao` **ausente**;
   - nenhum `CLAUDE.md`/memória de projeto.
4. **Screenshot novo** (os do `GATE-C20` eram de um repositório descartável): Cmd+Shift+4 sobre o painel do Claude Code. O arquivo vai para a Mesa; mova e versione:
   ```bash
   mv "$(ls -t ~/Desktop/Screenshot*.png ~/Desktop/Captura*.png 2>/dev/null | head -1)" "$AVAL/dados/evidencias/gate-a02-ciclo-a.png"
   cd "$AVAL" && git add dados/evidencias/gate-a02-ciclo-a.png && git commit -m "Ciclo A: evidência do GATE-A02" && git push origin main
   ```
   (O nome do arquivo depende do idioma do macOS: `Screenshot…` em inglês, `Captura de Tela…` em português.)
5. **Fechar** = encerrar essa conversa: fechar a aba do painel ou Cmd+Q no VS Code. **Sem** `/coletar-sessao` — só houve `/context` (comando local, não é mensagem ao agente), então não há o que medir. Uma sessão só com `/context` **não grava transcript** (confirmado em 11/10/2026: a pasta do projeto do ciclo não tem `.jsonl`), então não há o que coletar nem o que justificar no `A-003`. Nunca reabrir essa conversa; a A1 começa numa conversa nova.
6. Registrar no `plano-ciclos.md`: `A-001`, `GATE-A01`, `GATE-A02` com data.

✅ Executado em 07/10/2026: modelo `claude-sonnet-5`, só `speckit-*`, `coletar-sessao` ausente. ⚠️ **Limite desta evidência (achado de 08/10, D-012):** o painel do `/context` mostra só categorias e tokens, sem nomes de skills; a pasta `skills/synced` foi criada durante essa sessão. Por isso o `GATE-A02b` repete a conferência com a sincronização desligada.

### 7.3b 🔴 `GATE-A02b` 🧑 Reconferência de largada (D-012; sessão **não** medida)

1. VS Code fechado (Cmd+Q). `abrir-ciclo a` → painel do Claude Code → conversa nova.
2. Digitar só `/context` (nenhuma outra mensagem) e conferir: modelo `claude-sonnet-5`; nenhuma skill da conta (o painel só mostra a linha `Skills` em tokens; as skills embutidas do Claude Code aparecem nos dois ciclos, a prova de ausência das da conta é o `ls` do passo 5); `coletar-sessao` fora da lista do modelo (ela continua **invocável** por você com `/`, é assim que o protocolo a usa); nenhum `CLAUDE.md`/memória de projeto.
3. Screenshot do painel → `$AVAL/dados/evidencias/gate-a02b-ciclo-a.png` (mesmo procedimento do `GATE-A02`).
4. **Deixar a sessão aberta por 2 minutos** (a sincronização em segundo plano, se estivesse ativa, rodaria nesse intervalo) e fechar com Cmd+Q, **sem** `/coletar-sessao`.
5. Conferir que as pastas **não voltaram**:
   ```bash
   ls ~/cerne/cfg-ciclo-a/skills ~/cerne/cfg-ciclo-a/plugins     # skills: só coletar-sessao; plugins: sem synced
   shasum -a 256 ~/cerne/cfg-ciclo-a/settings.json ~/cerne/cfg-ciclo-b/settings.json   # 3904700b…5922 nos dois
   ```
6. Sessão só com `/context` não grava transcript: nada a registrar no `A-003`. Nunca reabrir essa conversa.

✅ Executado em 08/10/2026 (`/context` sem nomes de skills; evidência `dados/evidencias/gate-a02b-pos-d012-ciclo-a.png`). Disco conferido em 11/10: sem `synced` em `skills` e `plugins`; `skills/.trash` só com pastas de 30/09; hash `3904700b…5922`. O mesmo `/context` mostrou a linha `MCP tools` (634 tokens), que levou à D-013.

### 7.3c 🔴 `GATE-A02c` 🧑 Reconferência de largada (D-013; sessão **não** medida)

1. VS Code fechado (Cmd+Q). `abrir-ciclo a` → painel do Claude Code → conversa nova.
2. Digitar só `/context` e conferir: modelo `claude-sonnet-5`; linha `MCP tools` **zerada ou ausente** (antes: 634 tokens); linha `Skills` no mesmo patamar de 08/10 (~2,8k: embutidas do Claude Code + `speckit-*`); `coletar-sessao` fora da lista do modelo (continua invocável por você com `/`); nenhum `CLAUDE.md`/memória.
3. Screenshot do painel (Cmd+Shift+4). Depois mova pelo nome real do arquivo: `ls -t ~/Desktop | head -3` e `mv ~/Desktop/"<nome do arquivo>" "$AVAL/dados/evidencias/gate-a02c-ciclo-a.png"`.
4. **Esperar 2 minutos** com a sessão aberta e fechar com Cmd+Q, **sem** `/coletar-sessao`.
5. Conferir no Terminal:
   ```bash
   ls -a ~/cerne/cfg-ciclo-a/skills ~/cerne/cfg-ciclo-a/plugins     # sem synced
   shasum -a 256 ~/cerne/cfg-ciclo-a/settings.json ~/cerne/cfg-ciclo-b/settings.json   # 0112786e…f393 nos dois
   git -C "$CERNE_CICLO_A_DIR" status --short                      # vazio
   ```

✅ Executado em 11/10/2026: `/context` sem a linha `MCP tools` (antes 634 tokens), `Skills` ~2,8k, modelo `claude-sonnet-5`, sem memória/`CLAUDE.md`; depois de 2 min e do Cmd+Q, sem `synced` em `skills` e `plugins`, hash `0112786e…f393` nos dois, ciclo limpo. Evidência: `dados/evidencias/gate-a02c-ciclo-a.png`.

---

## 8. A1 — Setup (constitution)

**Data proposta:** 01 a 02/10/2026 · **ID:** `SETUP` · **Fase:** `ESPEC` · **Métrica principal:** M1 (parte "sessão")

### 8.1 🧪 `A-002` Sessão `/speckit-constitution` com o `P-SETUP`

Primeira (e única) mensagem de comando: o comando **digitado** (`/speckit-constitution`, um espaço) e, logo depois, o texto inteiro de `prompts/P-SETUP.md` **colado** (D-014; o bloco abaixo mostra como a mensagem completa fica). O texto abaixo já é o do arquivo corrigido pelo D-001 (hash `6c040ea1…ca65`); gere sempre a partir do arquivo, nunca reescreva à mão.

````text
/speckit-constitution # P-SETUP — Project principles

Use the principles below as the governing rules for all work in this repository.

## Product and sources

- This repository builds **Cerne**, a mobile reflective-journaling app with an AI assistant.
- The product input is in `docs/input/`:
  - `requirements.md` — functional and quality requirements, screens, API, delivery order and technical constraints;
  - `prototype/` — the frozen visual prototype and its extract (visual tokens, list of states);
  - `backend/` — documentation of the existing backend: API, error taxonomy, screen-state map, sync-badge semantics and fixtures.
- These documents are the source of truth for the product. Where they are silent, make a reasonable technical decision.

## Fixed technical stack

- Flutter and Dart at the version pinned for this repository (fvm).
- State management: `flutter_bloc`.
- Clean Architecture, three layers per feature.
- Error handling: `fpdart`; repositories return `Either<Failure, T>`.
- Test doubles: `mocktail`.
- On-device speech-to-text: `whisper_ggml`. Audio never goes to the backend.
- Visual tokens: `lib/core/design_tokens.dart` is the single source of colors, typography, spacing and radii.
- Platform: iOS.
- Backend: already built and frozen. The app consumes its API as documented in `docs/input/backend/`. All AI features, including semantic search, are provided by the backend. Configuration and credentials come from a `.env` file at the project root, with exactly two variables: `FUNCTIONS_BASE_URL` and `SUPABASE_ANON_KEY`. Every call to `{FUNCTIONS_BASE_URL}/<function>` carries the header `apikey: <SUPABASE_ANON_KEY>`. The `Authorization: Bearer` header carries `SUPABASE_ANON_KEY` on the operations that need no user session (sign-up, login, refresh) and the user's access token on every operation marked `bearerAuth` in `docs/input/backend/api/openapi.yaml`.
- Everything else — routing, HTTP client, local cache, dependency injection, secure storage, biometrics, charts — is your choice.

## Folder convention

```
lib/
  core/
  features/
    <feature>/
      data/
      domain/
      presentation/
```

## Quality

- Meet the quality requirements RNF01–RNF09 in `docs/input/requirements.md`.
- The domain layer follows RNF06.

## User interface

- The UI is faithful to the prototype in `docs/input/prototype/`.
- UI text is in **Portuguese**, exactly as written in the prototype.
- Code identifiers, comments and project documentation are in English.

## Scope

- Implement the functional requirements in the delivery order given in `docs/input/requirements.md`.
- Extension features (section 2 of `requirements.md`) are not implemented. A menu entry may exist as a placeholder.

## Do not

- Change the backend, its API contract or its configuration.
- Call AI providers directly from the app.
- Write visual values (colors, font sizes, spacing, radii) outside `design_tokens.dart`.
- Implement extension features.
- Commit `.env` or any credential.
- Edit the files in `docs/input/`.
````

⚠️ Acima está o texto atual do arquivo (com o D-001). O argumento **não se digita à mão**: gere-o a partir do arquivo e cole depois de digitar o comando. Não cole o comando junto (D-014):
```bash
{ cat "$AVAL/prompts/P-SETUP.md"; } | pbcopy   # só o argumento: digite `/speckit-constitution ` à mão (com o espaço) e cole depois (D-014); depois Cmd+V no campo do Claude Code
```

🤖 O agente resolve o template, preenche os princípios e grava `.specify/memory/constitution.md`, com o "Sync Impact Report" num comentário HTML no topo. Esse comentário **não** é removido por você.

Pausas possíveis: valores ausentes (5.3), por exemplo a data de ratificação.

> ✅ **Execução (11/10/2026):** sessão `f2b3d499`. O agente não pausou (0 `PROCESSO:`, 0 intervenções); a data de ratificação não foi pedida, e o RDR continua vazio. A mensagem foi colada inteira, com o comando dentro: a extensão a envolveu em `<pasted_content>` e o agente chamou a skill sozinho. **D-014** corrige a forma para as próximas sessões (comando digitado + argumento colado).

### 8.2 📏 Coleta

`/coletar-sessao SETUP` → aprovar a permissão → conferir a saída → fechar a sessão.

> ✅ **Execução (11/10/2026):** `Registrado. Intervenções reconhecidas: 0. Respostas PROCESSO reconhecidas: 0. Timebox da unidade: abaixo de 50%.` Mais um aviso do coletor: diretório de subagentes não encontrado, esperado (a sessão não usou subagente). Contagens batem com o que foi digitado (nada).

### 8.3 🧑 Conferência rápida (fora da sessão, sem editar)

```bash
cd "$CERNE_CICLO_A_DIR" && git status --short
```
Deve aparecer `.specify/memory/constitution.md` modificado (e, possivelmente, outros arquivos). Você não abre o arquivo para revisar conteúdo: não há P6 para o setup.

> ✅ **Execução (11/10/2026):** `git status --short` mostrou só `M .specify/memory/constitution.md`.

### 8.4 📏 Commit de fechamento + tag `cicloA/setup-done` (contorno documentado, seção 2.3)

```bash
cd "$CERNE_CICLO_A_DIR"
git add -A
git commit -m "SETUP: closing snapshot (constitution)"
git tag cicloA/setup-done
python3 "$AVAL/scripts/registrar_tag.py" --ciclo a --tag cicloA/setup-done --tipo setup-done \
  --commit "$(git rev-parse HEAD)" --data "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
git push origin main --tags
```
O M1 (calendário) vai do início da instalação até esta tag.

> ✅ **Execução (11/10/2026):** commit `e1f8057` (1 arquivo, +163/−35), tag `cicloA/setup-done`, push de `main` e da tag para `cerne-ciclo-a`; `registrar_tag.py` sem saída (esperado).

### 8.5 🔴 Checagem única de parse (cega a números)

Só depois da **primeira** sessão real, para confirmar que o coletor reconheceu o comando do Spec Kit. O comando mostra **apenas** as colunas `fase` e `marcador_origem`, sem nenhum número:
```bash
cut -d, -f4,5 "$AVAL/dados/cicloA/segmentos.csv" | sort -u
```
- **Esperado:** uma linha `ESPEC,speckit-constitution` (pode haver também `SETUP,(nenhum)` para o trecho antes do comando).
- **Se só aparecer `SETUP,(nenhum)`:** o nome do comando no transcript não bate com a tabela de fases. **Não corrija nada.** Os brutos estão preservados e a fase é re-derivada na Parte IV. Anote o achado e me avise numa sessão de `cerne-avaliacao` (fora do ciclo).

Repita a mesma checagem uma vez depois do primeiro `/speckit-specify` (A2).

> ⚠️ **Resultado (11/10/2026):** só apareceu `SETUP,(nenhum)`, o caso previsto acima. Causa (ensaio `/tmp/ensaio-invocacao`, 3 sessões não medidas): o transcript não grava `system/local_command`; grava, na mensagem humana, `<command-name>/nome</command-name>`, e uma mensagem inteira colada nem chega a ser expandida (o agente chama a skill). **D-014** corrige o coletor (lê `<command-name>`) e a forma de invocação. As linhas do `SETUP` são re-derivadas dos brutos na Parte IV. **Depois do primeiro `/speckit-specify` (A2) o resultado esperado passa a ser `ESPEC,speckit-specify`**; se não aparecer, **não corrija nada** e me avise.

---

## 9. Bloco-padrão de unidade

Vale para **todas** as unidades A2–A12. As fichas da seção 10 só acrescentam o que é próprio de cada uma.

### 9.1 Sequência de sessões (`GATE-C09`, §4.2) — uma sessão por linha

| # | Sessão 🧪 — primeira mensagem | Argumento | Fase | Pausas previstas → resposta | Coleta | Artefato esperado 🤖 |
|---|---|---|---|---|---|---|
| 1 | `/speckit-specify <prompt>` | `P-RFxx` da unidade (na F000: `P-F000` + `P-GLOBAL`, seção 10.1) | `ESPEC` | Até 3 perguntas Q1–Q3 → `PROCESSO:` (5.3) | `/coletar-sessao <ID>` | `specs/NNN-<nome>/spec.md`, `.specify/feature.json` apontando para ele |
| 2 | `/speckit-clarify` | nenhum | `ESPEC` | Até 5 perguntas, uma por vez → um `PROCESSO:` por pergunta | idem | Seção `## Clarifications` no `spec.md` |
| 3 | `/speckit-plan <P-TECH>` | `P-TECH` (seção 9.2) | `ESPEC` | nenhuma prevista | idem | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md` |
| 4 | `/speckit-checklist` | nenhum | `VALID` | Q1–Q3 (+ Q4/Q5) → `PROCESSO:` | idem | `specs/NNN-*/checklists/*.md` (itens desmarcados), agora com `plan.md` disponível (D-016) |
| 5 | `/speckit-tasks` | nenhum | `ESPEC` | nenhuma prevista | idem | `tasks.md` com itens `- [ ] T001 …` |
| 6 | `/speckit-analyze` | nenhum | `VALID` | Oferta de remediação → `PROCESSO: Yes.` (sugestão de RDR) | idem | Relatório no chat; ajustes nos artefatos, se aceitos |
| 7 | `/speckit-implement` | nenhum | `IMPL` | Checklists incompletos → `PROCESSO: yes` (sugestão de RDR) | idem | Código em `lib/`, testes; tarefas marcadas `[X]` em `tasks.md` |
| 8 | `/speckit-converge` | nenhum | `VALID` | nenhuma (não é gatilho) | idem | Ou anexa `## Phase N: Convergence` em `tasks.md`, ou reporta **"✅ Converged — the implementation satisfies the spec, plan, and tasks."** |
| 9 | Se o passo 8 **não** reportou *Converged*: nova sessão `/speckit-implement`, depois nova sessão `/speckit-converge` | — | `IMPL` / `VALID` | idem 7 e 8 | idem | Repetir 7 → 8 até *Converged* ou até a timebox |

Notas:
- **Ordem fixa (D-016, 11/10/2026).** O `checklist` vem **depois do `plan` e antes do `tasks`**. A decisão original (R22) o punha antes do `plan`, mas o script do `speckit-checklist` exige `plan.md` e o agente para (visto na F000); o CLI também o sugere depois do `plan`. Se uma sessão `/speckit-checklist` for aberta **antes** do `plan` por engano, o agente vai parar e perguntar: responda por *Other* `INTERVENÇÃO [esclarecimento não solicitado]: Stop here. Do not generate the checklist in this session.`, colete e siga com o `plan`.
- No passo 6, se o relatório trouxer problemas **CRITICAL** e sugerir rodar de novo um comando anterior ("Run /speckit-specify with refinement"), **não** volte na sequência. Siga para o passo 7. A remediação aceita na própria sessão do `analyze` é o caminho do método.
- **Memória do agente (D-033).** Depois de cada `/coletar-sessao`, rode `ls ~/cerne/cfg-ciclo-a/projects/*/memory/`. Tem que estar vazio ou inexistente. Se houver arquivo (o agente grava memória por conta própria), cole a listagem no chat antes da próxima sessão: o guia registra o conteúdo e a sessão de origem, você remove os arquivos e abre-se um desvio.
- O `implement` pode parar sozinho se uma tarefa falhar (*"Halt execution if any non-parallel task fails"*). Colete e abra nova sessão com `/speckit-implement` (4.5).

### 9.2 Textos literais dos argumentos

**`P-TECH`** (passo 3, em toda unidade; D-016):
```text
/speckit-plan # P-TECH — Technical instruction

Follow the technical constraints in `docs/input/requirements.md` and the architecture already in place in the project.
```
Atalho: `{ cat "$AVAL/prompts/P-TECH.md"; } | pbcopy` — antes disso, digite `/speckit-plan ` à mão; depois cole o argumento (D-014)

**`P-RFxx`** (passo 1): `{ cat "$AVAL/prompts/P-RF03.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014) (troque o número). Os textos completos estão em cada ficha (seção 10).

### 9.3 🔴 Verificação de "concluído" (P6) — 🧑 fora de sessão

Só depois que um `converge` reportar *Converged*. Os quatro critérios precisam valer **juntos**:

| | Critério | Como verificar |
|---|---|---|
| (a) | O agente declarou pronto | O último `/speckit-converge` reportou "✅ Converged — …" |
| (b) | `flutter analyze` sem erros | `cd "$CERNE_CICLO_A_DIR" && fvm flutter analyze` → nenhuma linha `error •` (infos e warnings não reprovam) |
| (c) | Testes do agente passam | `fvm flutter test` → `All tests passed!`. **Nunca** com `--coverage`, que é medição (M8). Interpretação registrada: só a pasta padrão `test/`; se existir `integration_test/`, ela não entra na P6 |
| (d) | Você percorre os critérios de aceite da §1 no iPhone | `fvm flutter run -d "$IPHONE"` e seguir o roteiro da ficha da unidade (seção 10) |

O que **não** entra na P6: a suíte hold-out (nunca durante o ciclo), cobertura, lint de arquitetura e qualidade de texto gerado por IA.

### 9.4 🧪 Sessão de correção (se a P6 falhar)

1. Sessão nova (`abrir-ciclo a`). A **primeira mensagem** é a própria intervenção, sem comando do Spec Kit:
   ```
   INTERVENÇÃO [correção|S<n>|<causa>]: Expected: … Actual: … Where: … Error: …
   ```
   Um sintoma por mensagem. Se houver vários, mande-os na mesma sessão, um de cada vez, cada um com seu prefixo.
   **Diferenças de tela em relação ao protótipo (D-019):** uma intervenção **por tela**, listando as diferenças da tela, com a severidade da mais grave (`S2` se falta ou difere texto, estado ou elemento do protótipo; `S1` se só o estilo difere). Descreva em termos qualitativos citando o estado do protótipo; sem valores numéricos de estilo nem código. Diferença vista em tela de unidade já fechada entra na correção da unidade atual (a unidade fechada não é reaberta).
   **Repetição de sintoma (D-025):** se a mensagem repete um sintoma que a sessão de correção anterior não resolveu, diga isso ("same symptom as a previous correction session, which did not change the behavior") e termine a mensagem com a frase fixa: `Investigate the root cause first, explain what you found, and only then fix it; confirm the fix end to end with a new question, not only with unit tests.` Só nesse caso; sem nomear arquivo, classe, pacote, método ou abordagem.
2. 🤖 O agente corrige (fase `IMPL` pelo protocolo; ver Apêndice C sobre a segmentação).
3. `/coletar-sessao <ID>`.
4. Repetir a P6. Repetir 9.4 até passar ou até a timebox, que soma todas as sessões da unidade.

### 9.5 📏 Fechamento da unidade

**Unidade concluída (P6 passou):**
```bash
cd "$CERNE_CICLO_A_DIR"
# 1) commit de fechamento (seção 12.2)
git status --short | head -40
git add -A -- . ':(exclude)build/' ':(exclude).dart_tool/' ':(exclude)ios/Pods/' ':(exclude)ios/.symlinks/' ':(exclude)ios/Flutter/ephemeral/' ':(exclude).flutter-plugins' ':(exclude).flutter-plugins-dependencies'
git commit -m "<ID>: closing snapshot at unit completion"
# 2) tag + registro
cd "$AVAL" && scripts/concluir-rf a <ID>
# 3) backup
git -C "$CERNE_CICLO_A_DIR" push origin main --tags
```
**Encerramento antecipado (D-026):** se o pesquisador decidir parar de corrigir um critério que continua falhando, antes de a timebox acabar, a unidade fecha como a da timebox, com `scripts/rf-incompleto a <ID>`. Não há número mínimo de sessões de correção: a decisão é discricionária e vai sempre registrada no `desvios.md` (critério, número de sessões de correção desse critério e faixa da timebox), igual nos dois ciclos. `concluir-rf` fica reservado ao caso em que a P6 passou inteira.
**Timebox atingido:** igual, trocando o passo 2 por `scripts/rf-incompleto a <ID>`. Se o `git commit` disser `nothing to commit`, siga normalmente: o agente já tinha commitado.

### 9.6 🧑 Notas de encerramento da unidade

Em `$AVAL/docs/plano-ciclos.md`, na unidade correspondente. **Sem números de métrica.**
- datas de início e fim; número de sessões, com quais comandos e quantos laços `implement`/`converge`;
- intervenções marcantes (tipo, causa, sintoma em uma linha);
- respostas novas no RDR (números das linhas);
- bloqueios, cortes por limite de uso (data e hora), avisos de coleta, achados de ambiente;
- critérios da P6 verificados só em parte, e por quê.

---

## 10. Fichas das unidades (A2–A12)

Ordem congelada (P9): **F000 → RF03 → RF01 → RF02 → RF07 → RF06 → RF04 → RF10 → RF08 → RF05 → RF09**. Cada ficha traz: prompt literal do `specify`, dependências (do próprio prompt), escopo, roteiro da P6 no iPhone e armadilhas. Na P6, o roteiro usa a **sua conta de desenvolvimento do ciclo** (criada na F000), nunca as contas do seed (`cenario-*@cerne.test`).

### 10.1 A2 — F000 Fundação

**Datas:** 02 a 04/10 · **Timebox:** 12 h · **ID:** `F000`

**Mensagem do passo 1** (`P-F000` + `P-GLOBAL`, nessa ordem; tabela de entrega, §5). Gere com:
```bash
{ cat "$AVAL/prompts/P-F000.md"; printf '\n\n'; cat "$AVAL/prompts/P-GLOBAL.md"; } | pbcopy   # só o argumento: digite `/speckit-specify ` à mão (com o espaço) e cole depois (D-014)
```
Conteúdo resultante:
```text
/speckit-specify # P-F000 — Foundation

Build the foundation that every later unit uses, as described in `docs/input/requirements.md`, section 12:

- Project scaffold following the technical constraints (section 13), including the folder convention.
- `lib/core/design_tokens.dart` with the visual tokens of the prototype (`docs/input/prototype/prototype-extract.md`, section 3).
- An HTTP client for the backend that returns `Either<Failure, T>` and maps the error contract `{ code, message, retryable }` (requirements, section 11; `docs/input/backend/error-taxonomy.md`). Real URLs are built as described in `docs/input/backend/README.md`.
- Login and sign-up — prototype state "Tela 0.1a" (Entrar / Criar conta) — with `POST /auth/signup`, `POST /auth/login`, `POST /auth/refresh`, `GET /auth/session`.
- Splash (Tela 0) and base navigation between the main screens (Home/Chat, side menu, Meus Registros, Configurações), with placeholders where later units will add content.
- Expired-session handling: the "Sessão expirada" overlay over the current screen, keeping its state (prototype extract, section 4).

## Do not

- Implement the features of RF01–RF10 now; leave clear places for them.
- Hardcode visual values outside `design_tokens.dart`.
- Change the backend.

# P-GLOBAL — Product vision

**Cerne** is a mobile reflective-journaling app with an AI assistant. The user records their day by text, audio or photo; a conversational agent consults those records through semantic search to answer with context and to offer proactive insights. The app also keeps a timeline of all records, lets the user search and filter them, exports a personal summary and shows an evolution dashboard. Access is protected by biometrics or PIN.

## Scope

The functional requirements RF01–RF10 in `docs/input/requirements.md`, section 1:
- RF01 — Multimodal capture (text / audio / photo)
- RF02 — Speech-to-text / OCR processing
- RF03 — Biometric authentication vault
- RF04 — Interactive chat with memory (RAG)
- RF05 — Personal summary export
- RF06 — Semantic search / filter over journal entries
- RF07 — Multi-source history (timeline)
- RF08 — Proactive insights (mechanism)
- RF09 — Temporal summaries / dashboard
- RF10 — Save a chat message as an entry

Plus the quality requirements RNF01–RNF09 (sections 3 and 4) and a foundation unit (F000). Delivery order: section 12.

## Out of scope

The extension features of section 2 (manual tags, action plans, persona): no functional implementation; a menu entry may exist as a placeholder. The backend already exists and is not changed.

## Where everything is

- `docs/input/requirements.md` — requirements, screens, endpoints, delivery order, technical constraints.
- `docs/input/prototype/` — the visual prototype (`cerne-prototype.html`) and its extract.
- `docs/input/backend/` — API contract and backend documentation.

## Do not

- Build extension features.
- Change the backend.
- Add features that are not in `requirements.md`.
```

**Escopo:** scaffold Flutter com `lib/core/` + `lib/features/<feature>/{data,domain,presentation}/`; `design_tokens.dart`; cliente HTTP com `Either` e os 13 códigos; Tela 0 (splash); Tela 0.1a (Entrar / Criar conta); navegação base (Home/Chat, menu lateral, Meus Registros, Configurações) com placeholders; overlay "Sessão expirada".
**Backend:** `auth-signup`, `auth-login`, `auth-refresh`, `auth-session`.

**Roteiro da P6(d) no iPhone:**
1. O app abre na splash (Tela 0) e chega a Entrar / Criar conta (Tela 0.1a), com os textos do protótipo em português.
2. **Criar a conta de desenvolvimento do ciclo:** e-mail `dev-cicloa@cerne.test` e uma senha sua. Guarde a senha em `$AVAL/segredos/` (nunca no chat). A conta entra direto, sem confirmação de e-mail; se pedir confirmação, é o item 3.7.1 (ambiente), não defeito do app.
3. Sair e entrar de novo com a mesma conta → chega ao Home/Chat.
4. Navegar pelo menu lateral → Meus Registros e Configurações abrem como placeholders. Planos de Ação pode existir só como item de menu (P10).
5. Erro de login (senha errada) mostra um estado tratado, sem crash.
6. "Sessão expirada": o comportamento completo é verificado no RF07 (10.5). Aqui, basta o overlay existir no fluxo de 401/`AUTH_EXPIRED`, se for possível provocá-lo.

**Armadilhas:**
- ⚠️ **Assinatura no iPhone.** Se o projeto ficar com o bundle id padrão `com.example.*`, o Xcode recusa instalar no aparelho ("namespace reservado", achado do `GATE-C16`). Isso é sintoma: `INTERVENÇÃO [correção|S3|amb]: The app cannot be installed on the iPhone. Error: <mensagem exata do flutter run/Xcode>.` Você **não** muda o bundle id à mão. A escolha do time de desenvolvimento, quando o Flutter perguntar no terminal, é ação de ambiente sua e não edita o projeto.
- ⚠️ Se o seu primeiro `fvm flutter run` pedir para confiar no desenvolvedor no iPhone: Ajustes → Geral → VPN e Gerenciamento de Dispositivo → confiar (ambiente, sem intervenção).
- O `.env` está no `.gitignore` e só tem `FUNCTIONS_BASE_URL` e `SUPABASE_ANON_KEY`. Não acrescente nada.

### 10.2 A3 — RF03 Cofre de autenticação biométrica

**Datas:** 04 a 05/10 · **Timebox:** 8 h · **ID:** `RF03` · **Depende de:** F000

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF03.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF03 — Biometric authentication vault

Protect access to the user's data with a Face ID / Touch ID / PIN barrier, validated on the device.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF03; parameter: section 10.
- Prototype states: "Tela 0.1 — Biometria", "Tela 0.1b — PIN inicial", "Tela 0.1c — PIN após falha" (prototype extract, section 2.1).
- Backend: no biometric endpoint (requirements, section 6.1). The biometrics preference is stored via `PATCH /account/settings`; the session is renewed with `POST /auth/refresh` or `POST /auth/login`; `POST /auth/logout`.
- Depends on: F000 (session, login).

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Critérios de aceite (§1) e roteiro da P6(d)**, com Face ID **real** do aparelho (o menu Features do simulador não existe mais):

| Critério | Como verificar no iPhone |
|---|---|
| Falha biométrica oferece PIN, sem trancar o usuário fora | Na Tela 0.1, provocar falha do Face ID: cobrir a câmera TrueDepth com a mão ou virar o rosto até o iOS desistir. O app deve oferecer o PIN (Tela 0.1c) e, com o PIN certo, entrar |
| Em segundo plano por 5 min, ao voltar exige autenticação de novo (fixo, não configurável) | Desbloquear o app → ir para a tela inicial do iOS → **esperar 5 min e 15 s no cronômetro** → voltar ao app: deve pedir autenticação. Opcional: com < 5 min, não deve pedir |
| (estados) Tela 0.1, 0.1b (PIN inicial), 0.1c (PIN após falha) existem com os textos do protótipo | Percorrer o cadastro do PIN e a falha |

**Armadilhas:**
- ⚠️ Se o app fechar ao chamar o Face ID, é sintoma (`S3`): descreva "app closes when the Face ID prompt should appear", com o log do `flutter run`. Nunca diga qual chave do `Info.plist` falta.
- ⚠️ A espera real de 5 min é obrigatória na P6. Não encurte.

### 10.3 A4 — RF01 Captura multimodal

**Datas:** 05 a 07/10 · **Timebox:** 8 h · **ID:** `RF01` · **Depende de:** F000, RF03

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF01.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF01 — Multimodal capture

Let the user create a journal entry by text, audio recording or photo, from the Insertion Modal.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF01.
- Prototype states: Insertion modal — "Texto", "Áudio — Gravando", "Foto — Captura" (prototype extract, section 2.3); opened by the "+" button of Home/Chat.
- Backend: `POST /entries` with `source` `manual`/`audio`/`photo`.
- Depends on: F000, RF03.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d)** (câmera e microfone **reais** do iPhone; a regra antiga de "foto pela galeria / microfone do Mac" não vale mais):

| Critério | Como verificar |
|---|---|
| As três modalidades geram o mesmo formato de entrada persistida | Pelo "+" do Home/Chat, criar uma entrada de texto, uma de áudio (o microfone pede permissão na 1ª vez) e uma de foto (câmera; a galeria também vale). A Timeline (RF07) ainda não existe, então confira no Supabase → `ciclo-a` → SQL Editor:<br>`select source, left(content,50), created_at from entries where user_id = (select id from auth.users where email='dev-cicloa@cerne.test') order by created_at desc limit 5;`<br>Três linhas, mesma estrutura, só o `source` muda |
| Cancelar no meio (ex.: interromper a gravação) não cria entrada parcial nem vazia | Começar uma gravação e cancelar; começar uma foto e cancelar. Rodar a mesma consulta: nenhuma linha nova |

> Consultar o banco do seu próprio ambiente de desenvolvimento é verificação sua, fora do agente. Não é métrica nem intervenção. Nunca rode SQL de escrita.

**Armadilhas:**
- O conteúdo do áudio nesta unidade depende do RF02 (STT), que vem em seguida. Como cada unidade tem o seu prompt, não peça transcrição aqui.
- ⚠️ Permissões de câmera e microfone negadas por engano no iOS: Ajustes → Cerne (ou o nome do app) → reativar. Isso é ambiente, sem intervenção.

### 10.4 A5 — RF02 Processamento STT/OCR

**Datas:** 07 a 08/10 · **Timebox:** 8 h · **ID:** `RF02` · **Depende de:** RF01

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF02.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF02 — Speech-to-text / OCR processing

Turn captured audio into text on the device, and photos into text through the backend, before saving the entry.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF02.
- Prototype states: "Áudio — Processando / Transcrito / Erro" and "Foto — Processando OCR / Reconhecido / Erro" (prototype extract, sections 2.3 and 4).
- On-device speech-to-text with `whisper_ggml` (audio never goes to the backend); OCR with `POST /media/ocr`; then `POST /entries`.
- Test material: `docs/input/backend/fixtures/`.
- Depends on: RF01.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):** o critério é "quatro estados visíveis: gravando, processando, transcrito, erro de transcrição".
- **Áudio:** gravar falando (ou tocando `docs/input/backend/fixtures/media/audio_fixture_01.wav` no Mac, perto do iPhone) → ver "Gravando" → "Processando" → "Transcrito" com o texto. Para o estado de erro, gravar **silêncio** por alguns segundos (gatilho adotado pela hold-out para "erro de transcrição"). Se o app não mostrar erro com silêncio, anote o que acontece.
- **Foto (OCR):** passar `ocr_fixture_01.png` e `ocr_fixture_ilegivel.png` (de `docs/input/backend/fixtures/media/`) para o iPhone por AirDrop, escolher pela galeria → "Processando OCR" → "Reconhecido" (texto) / "Erro" (ilegível).

**Armadilhas (este é o RF de maior risco técnico):**
- ⚠️ `whisper_ggml` **não compila para o simulador** (`GATE-C16`). Se o agente tentar rodar no simulador e travar em erro de linker do `ffmpegkit`, isso faz parte do experimento: você **não** conta ao agente que existe um iPhone físico. Só se ele perguntar onde rodar é que vale a seção 2.4. Na P6, o build é no aparelho, por você.
- ⚠️ O modelo do Whisper pode ser baixado em tempo de execução (rede) ou empacotado como asset. Asset > 100 MB impede o `git push` (limite do GitHub): veja a seção 13 ("push recusado").
- O primeiro build com `whisper_ggml` é lento (CocoaPods + FFmpeg). Não interrompa.

### 10.5 A6 — RF07 Histórico multi-fonte (timeline)

**Datas:** 08 a 10/10 · **Timebox:** 8 h · **ID:** `RF07` · **Depende de:** F000, RF01

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF07.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF07 — Multi-source history (timeline)

Show all the user's entries in a timeline, whatever their origin, with a per-entry synchronization badge.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF07.
- Prototype states: "Tela 4 — Meus Registros" (default) and "Tela 4 — Vazio" (prototype extract, section 2.4); the "Sessão expirada" overlay (section 4).
- Badge semantics: `docs/input/backend/sync-badge.md`.
- Backend: `GET /entries`, `GET /entries/:id`, `GET /auth/session`, `POST /auth/refresh`.
- Depends on: F000, RF01.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):**

| Critério | Como verificar |
|---|---|
| Sessão expirada durante a visualização → pede novo login, sem crash e sem perder a posição de rolagem | Procedimento abaixo |
| O selo de sincronização por entrada atualiza independentemente do fluxo de autenticação | Criar uma entrada nova e ver o selo dela mudar de estado (ex.: pendente → sincronizada, conforme `sync-badge.md`) sem relogar |
| Nenhum BLoC importa outro BLoC | Critério **estrutural**: não é verificado à mão na P6 (é medido na Parte IV, M11). Não abra o código |
| Tela 4 "Vazio" | Opcional: uma segunda conta nova, sem entradas |

**Como provocar "sessão expirada" no aparelho (sem proxy):** o logout do backend revoga **todas** as sessões da conta (escopo global do GoTrue). O token de acesso do aparelho vale até 60 min.
1. No iPhone: abrir o app, logar, ir a Meus Registros e rolar até o meio da lista. Anote a hora.
2. No Mac, logar como a mesma conta e fazer logout global:
   ```bash
   set -a; source "$AVAL/segredos/.env.ciclo-a"; set +a
   TOKEN=$(curl -s -X POST "$FUNCTIONS_BASE_URL/auth-login" \
     -H "Authorization: Bearer $SUPABASE_ANON_KEY" -H "apikey: $SUPABASE_ANON_KEY" -H "Content-Type: application/json" \
     -d '{"email":"dev-cicloa@cerne.test","password":"<sua senha>"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["data"]["session"]["accessToken"])')
   curl -s -X POST "$FUNCTIONS_BASE_URL/auth-logout" -H "Authorization: Bearer $TOKEN" -H "apikey: $SUPABASE_ANON_KEY"
   ```
3. Deixar o app aberto na timeline até passar **60 min** do login do passo 1. Depois, fazer qualquer ação que chame o backend (reabrir Meus Registros, rolar até carregar mais ou voltar do modal de inserção; o protótipo não tem gesto de "puxar para atualizar", D-023). Deve aparecer o overlay "Sessão expirada" sobre a tela, com a rolagem preservada e sem crash.
4. Se não for possível reproduzir, registre nas notas "critério verificado em parte — limitação do ambiente de desenvolvimento" e faça o mesmo nas duas pontas (Ciclo B igual). A hold-out cobre isso na Parte IV com 401 forjado.

### 10.6 A7 — RF06 Busca semântica e filtros

**Datas:** 10 a 11/10 · **Timebox:** 8 h · **ID:** `RF06` · **Depende de:** RF07

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF06.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF06 — Semantic search / filter

Let the user find entries by meaning and narrow them with filters, on the My Records screen.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF06; parameter: section 10.
- Prototype states: search bar of "Tela 4 — Meus Registros", "Tela 4 — Sheet de filtro", "Tela 4 — Filtros ativos" (prototype extract, section 2.4, including the note on categories).
- Backend: `GET /entries/search`, `GET /entries`.
- Test material: `docs/input/backend/fixtures/seeded-search-entries.md`.
- Depends on: RF07.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d)** (na sua conta de desenvolvimento, crie antes as entradas de teste com os textos de `docs/input/backend/fixtures/seeded-search-entries.md`, pelo modal do RF01):

| Critério | Como verificar |
|---|---|
| Busca semântica acha entradas relacionadas sem a palavra exata ("ansiedade" → entrada que só fala "nervosismo") | Buscar o termo do fixture e ver a entrada relacionada |
| Debounce de 300 ms: digitar rápido dispara **uma** consulta | Sem proxy, não dá para contar requisições com precisão. Observe que a lista não "pisca" a cada tecla; a medição exata é da hold-out (mitmproxy). Anote como verificação parcial |
| Cache local consistente com o servidor após reconexão, sem duplicar itens | Modo Avião ligado → abrir Meus Registros (só leitura do cache) → desligar o Modo Avião → a lista se atualiza sem itens repetidos |
| Dois filtros (`source` + datas) restringem com E, não OU | Filtro "Áudio" + período: só áudios dentro do período |
| Limpar filtros volta à lista completa sem reiniciar a tela | Limpar e conferir |

**Armadilha:** não existe filtro por tag ou categoria (o backend não implementa). Se o app oferecer isso de verdade, é escopo de extensão → `INTERVENÇÃO [redirecionamento|prd]`.

### 10.7 A8 — RF04 Chat interativo com memória (RAG)

**Datas:** 11 a 13/10 · **Timebox:** 8 h · **ID:** `RF04` · **Depende de:** F000, RF03 (do prompt)

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF04.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF04 — Interactive chat with memory (RAG)

Build the conversation with the AI agent, which answers with context from the user's previous entries.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF04.
- Prototype states: "Tela 1 — Home/Chat" (default), "Streaming", "Falha ao gerar resposta", "Offline"; "Tela 3 — Menu lateral" with the session list and the new-conversation action (prototype extract, sections 2.2 and 4).
- Backend: `POST /chat/sessions`, `GET /chat/sessions`, `GET /chat/sessions/:id/messages`, `POST /chat/sessions/:id/messages` (SSE), `POST /chat/sessions/:id/messages/:userMessageId/retry` (requirements, section 6.3).
- Depends on: F000, RF03.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):**

| Critério | Como verificar |
|---|---|
| Três estados de UI: processando/streaming, erro, resposta completa | Mandar uma pergunta sobre algo das suas entradas: ver o streaming e a resposta completa. Erro: ver abaixo |
| Se o stream cair no meio, a mensagem parcial fica visível com indicação de falha | Mandar uma pergunta longa e, durante o streaming, ligar o Modo Avião. A parcial deve ficar com a indicação de falha e uma forma de tentar de novo (`retry`) |
| Mensagens do chat **não** criam entradas | Depois de conversar, conferir no SQL Editor (consulta da 10.3) que nenhuma entrada nova apareceu |
| Menu lateral: lista de sessões e "Novo Chat" | Abrir o menu, ver as sessões, tocar "Novo Chat" → Home vazia |

**Armadilhas:** o backend usa IA real em `REPLAY_MODE=replay` (chama o provedor e grava no cache). Respostas lentas são normais. Se houver `AI_GENERATION_TIMEOUT` recorrente, é ambiente/backend → seção 13 (D16).

### 10.8 A9 — RF10 Salvar mensagem do chat como entrada

**Datas:** 13 a 14/10 · **Timebox:** 8 h · **ID:** `RF10` · **Depende de:** RF01, RF04

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF10.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF10 — Save a chat message as an entry

Let the user turn one of their own chat messages into a journal entry.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF10.
- Prototype state: "Tela 1 — Bookmark", with its sub-states (prototype extract, section 2.2).
- Backend: `POST /entries` with `source` `chat` and `chatMessageId`.
- Depends on: RF01, RF04.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):**

| Critério | Como verificar |
|---|---|
| Só mensagens do **usuário** têm o botão | Conferir no chat: respostas da IA sem botão |
| Salvar a mesma mensagem duas vezes não duplica (idempotência) | Salvar e tocar de novo → SQL Editor: uma única entrada com `source='chat'` para aquela mensagem |
| Falha ao salvar (sem rede) mantém a conversa funcionando e o botão volta a permitir nova tentativa | Modo Avião → tocar salvar → erro tratado; desligar o Modo Avião → tentar de novo → salva |
| O chat não importa repositório/data source da feature de entradas | **Estrutural**: não verificar à mão (M11/M7, Parte IV) |

### 10.9 A10 — RF08 Insights proativos

**Datas:** 14 a 16/10 · **Timebox:** 8 h · **ID:** `RF08` · **Depende de:** RF04

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF08.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF08 — Proactive insights (mechanism)

Insert an AI suggestion into the chat without the user asking for it.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF08; parameter: section 10.
- Prototype state: "Tela 1 — Insight" (prototype extract, section 2.2).
- Backend: `POST /chat/sessions/:id/insight`.
- Depends on: RF04.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):**

| Critério | Como verificar |
|---|---|
| Disparo após N = 5 mensagens do usuário **ou** T = 2 min de inatividade, exatamente uma vez por condição satisfeita | (1) Numa conversa nova, mandar 5 mensagens: o insight aparece uma vez. (2) Noutra conversa, mandar 1 mensagem e ficar **2 min e 10 s** parado (cronômetro): o insight aparece uma vez e não repete |
| Falha do insight não afeta o chat principal | Modo Avião logo antes do disparo → o chat continua utilizável depois de voltar a rede |
| Dispensar o insight não muda a rolagem nem o estado da conversa | Rolar um pouco, dispensar o insight, conferir a posição |

A espera real de 2 min é obrigatória.

### 10.10 A11 — RF05 Exportação de resumo pessoal

**Datas:** 16 a 18/10 · **Timebox:** 8 h · **ID:** `RF05` · **Depende de:** RF07

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF05.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF05 — Personal summary export

Let the user export a narrative summary of their entries as PDF, and always be able to download the raw data.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF05.
- Prototype states: the export sheet — "Pendente", "Processando", "Concluído", "Erro", "Período vazio" (prototype extract, section 2.5); opened by the download icon of Meus Registros.
- Screen ↔ job status mapping: `docs/input/backend/export-screen-states.md`.
- Backend: `POST /export/summary`, `GET /export/:jobId/status`, `GET /export/:jobId/download`.
- Depends on: RF07.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):**

| Critério | Como verificar |
|---|---|
| Job com zero entradas no período → estado de erro tratado ("Período vazio"), nem PDF vazio nem crash | Escolher um período sem entradas |
| Falha da narrativa (timeout do modelo) ainda permite baixar os dados brutos | Sem proxy não dá para forçar o `ai_timeout`. Verificar que a opção de dados brutos existe e funciona num job normal; o caso de falha é coberto pela hold-out. Anotar como verificação parcial |
| Estados Pendente → Processando → Concluído | Exportar um período com entradas e acompanhar; baixar o PDF |

**Armadilha:** o worker de exportação depende de `experiment.worker_config`, configurado em 29/09 (`C-015`). Job preso em "Pendente" por vários minutos é ambiente/backend, não app → seção 13. Antes de culpar o app, confira no SQL Editor: `select status, created_at from export_jobs order by created_at desc limit 3;`

### 10.11 A12 — RF09 Resumos temporais / dashboard

**Datas:** 18 a 20/10 · **Timebox:** 8 h · **ID:** `RF09` · **Depende de:** F000, RF01 (do prompt)

**Mensagem do passo 1:** `{ cat "$AVAL/prompts/P-RF09.md"; } | pbcopy` — antes disso, digite `/speckit-specify ` à mão; depois cole o argumento (D-014)
```text
/speckit-specify # P-RF09 — Temporal summaries / dashboard

Build the Settings screen with the evolution dashboard, and the profile and account actions that live on it.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF09; RNF05 (section 4) for account deletion.
- Prototype states: "Tela 6 — Configurações" in its four dashboard variations and "Tela 6 — Confirmar exclusão de conta" (prototype extract, section 2.6); profile name editing, "Sair" and "Apagar conta".
- Backend: `GET /dashboard/aggregate`, `GET /dashboard/narrative`, `PATCH /account/settings`, `DELETE /account`, `POST /auth/logout`.
- Depends on: F000, RF01.

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
```

**Roteiro da P6(d):**

| Critério | Como verificar |
|---|---|
| Renderiza com 0, 1 e > 30 entradas | 0: criar uma conta nova `dev-cicloa-vazia@cerne.test`. 1: na mesma conta, criar uma entrada. > 30: na conta principal, ter mais de 30 entradas (crie as que faltarem pelo modal; não use contas do seed) |
| Agregação recalcula após criar uma entrada | Abrir Configurações, anotar o gráfico, criar uma entrada, voltar: o gráfico muda |
| Texto da narrativa não quebra a UI em casos extremos | Só checar que não quebra; conteúdo nunca é avaliado |
| "Sair" e "Apagar conta" (RNF05) | Sair → volta ao login. **Apagar conta só numa conta descartável** (ex.: a conta "vazia"), nunca na principal |

**Armadilhas:**
- O seletor de persona é extensão (P10): no máximo um toggle cosmético. Se for construído com lógica → `INTERVENÇÃO [redirecionamento|prd]`.
- ⚠️ Achado do `C-014` (28/09): `dashboard-aggregate-get` devolveu `404 NOT_FOUND "perfil do usuário autenticado não encontrado"` para uma conta do **seed**. Contas criadas pelo cadastro do app têm perfil (trigger `on_auth_user_created`), então isso não deve ocorrer na sua conta. Se ocorrer, é defeito de backend → seção 13 (D16), não do app.

---

## 11. Matriz de métricas — o que é coletado, quando e por quem

Durante o ciclo você **grava** dados, mas não **olha** nenhum número (cegamento, P7 das métricas). A tabela diz onde cada métrica nasce no Ciclo A e o que precisa estar preservado para a Parte IV.

| Métrica | O que é | Onde nasce no Ciclo A | Quem/quando | Arquivo | O que você precisa garantir |
|---|---|---|---|---|---|
| **M1** Setup | Instalação + sessões `SETUP` + calendário | A0 (`instalar-metodologia`) e A1 | ⚙️ script; 📏 `/coletar-sessao SETUP`; tags `instalado`/`setup-done` | `sessoes.csv`, `tags.csv` | Sessão A1 coletada com `SETUP`; tag `setup-done` só depois dela |
| **M2** Tempo | Tempo ativo por sessão, unidade e fase; calendário por tags | Toda sessão | 📏 coleta; tags | `sessoes.csv`, `segmentos.csv`, `tags.csv` | ID certo em toda coleta; `concluir-rf`/`rf-incompleto` no dia em que a unidade acaba |
| **M3** Tokens/custo | Tokens principal + subagentes; USD pela tabela congelada | Toda sessão | 📏 coleta; OTel como conferência | `sessoes.csv`, `segmentos.csv`, `brutos/` | Coletor OTel rodando; nunca apagar `~/cerne/cfg-ciclo-a/projects/` |
| **M4** Artefatos | Arquivos do Spec Kit por tipo | `specs/NNN-*/`, `.specify/memory/` | 🤖 gera; Parte IV conta nas tags | (Parte IV) | Commit de fechamento antes de cada tag; nunca apagar `specs/` |
| **M5** Intervenções | Mensagens `INTERVENÇÃO [...]` por tipo, causa, severidade e nível | Toda sessão | 🧑 digita; 📏 coleta extrai | `intervencoes.csv`, `avisos_coleta.csv` | Prefixo exato; ação fora do chat seguida de mensagem |
| **M5b** Revisão exigida pelo processo | Respostas `PROCESSO:` | Pausas previstas (5.3) | 🧑 digita | `revisoes_processo.csv` | Prefixo só nas pausas previstas |
| **D16** Severidade | `Sn` nas correções | Sessões de correção | 🧑 classifica no momento | `intervencoes.csv` | Escala S1–S3 (5.1) |
| **M6** Aderência ao plano | `tasks.md` marcado; `plan.md` × diff; referências inexistentes; divergências (J) | `specs/NNN-*/` + diff entre tags | Parte IV | `rf.csv`, `julgamentos.jsonl` | Uma tag por unidade, com o código da unidade (commit de fechamento) |
| **M7** Camadas | Imports proibidos no domínio | Código em cada tag | Parte IV | `rf.csv` | Idem |
| **M8 / M8b** Cobertura / mutação | Domínio | Testes do agente nas tags | Parte IV | `rf.csv` | **Nunca** rodar `--coverage` durante o ciclo |
| **M9** Fidelidade visual | Hardcodes (tags); cor, tipografia e espaçamento (`final`) | Código e screenshots da `final` | Parte IV | `rf.csv`, `estados_m9.csv` | Textos do protótipo intocados (você nunca "corrige" texto) |
| **M10** Erro de rede | Assinaturas `Either` (tags); 15 cenários (`final`) | Código | Parte IV (hold-out, mitmproxy) | `rf.csv`, `ciclo.csv` | Nada de proxy durante o ciclo (`C-024`) |
| **M11** Critérios de aceite | Hold-out na `final` | App da tag `final` | Parte IV | `rf.csv` | A hold-out nunca roda durante o ciclo |
| **M12** Complexidade | Domínio | Tags | Parte IV | `rf.csv` | — |
| **M13** Regressão | Testes do agente tag a tag, com apagados | Tags | Parte IV | `rf.csv` | Uma tag por unidade, na ordem |
| **M14** Handoff | Decisões da constitution + `plan.md` da F000, verificadas na `final` | `.specify/memory/constitution.md`, `specs/<F000>/plan.md` | Parte IV | `ciclo.csv` | Nunca editar esses arquivos |
| **M15** Padrões | Convenções da feature do RF01 (tag `rf01-done`) × demais na `final` | Código | Parte IV | `ciclo.csv` | Tag `cicloA/rf01-done` com o código do RF01 |
| `n_msgs_contexto_ide` | Mensagens com `<ide_selection>` injetado | Toda sessão | 📏 coleta | `sessoes.csv` | Editores fechados e olho desligado antes de cada mensagem |

**Nunca abrir:** `sessoes.csv`, `segmentos.csv`, `intervencoes.csv`, `revisoes_processo.csv` (têm tempos ou números), `output.jsonl` do OTel, painel de uso do Claude. A única exceção é a checagem cega da seção 8.5, que mostra só as colunas `fase` e `marcador_origem`.

---

## 12. Git, tags e backup

### 12.1 Tags do Ciclo A, em ordem

| Tag | Quando | Como |
|---|---|---|
| `cicloA/baseline` | A0 | `scripts/iniciar-ciclo a` |
| `cicloA/instalado` | A0 | `scripts/instalar-metodologia a` |
| `cicloA/setup-done` | Fim da A1 | Manual (8.4) |
| `cicloA/f000-done` … `cicloA/rf09-done`, ou `-incompleto` | Fim de cada unidade | Commit de fechamento + `scripts/concluir-rf a <ID>` / `rf-incompleto a <ID>` |
| `cicloA/final` | Encerramento | Manual (14.2) |

Nenhuma tag é movida nem apagada depois de criada. Tag criada por engano: **não** apague. Registre em `desvios.md` e crie a certa.

### 12.2 Commit de fechamento (D-002)

- **Quando:** imediatamente antes de cada tag (`setup-done`, unidade, `final`), fora de sessão.
- **O quê:** grava o estado atual do repositório, sem alterar conteúdo. Exclui só os artefatos de build padrão do Flutter, que são regenerados em qualquer build (`build/`, `.dart_tool/`, `ios/Pods/`, `ios/.symlinks/`, `ios/Flutter/ephemeral/`, `.flutter-plugins*`).
- **Não é intervenção** (equivale ao merge do `concluir-rf`, regra 25). Você não edita `.gitignore` nem nenhum arquivo.
- **Conferência antes de commitar:** `git status --short | head -40`. Se aparecer `.env`, **pare**: o `.gitignore` foi alterado pelo agente. Anote, não commite o `.env` (`git restore --staged .env`) e reporte o sintoma na próxima sessão, se fizer sentido.

### 12.3 Branches

O Spec Kit sem a extensão `git` não cria branches: tudo fica em `main`. Se o agente criar um branch por conta própria, o `concluir-rf` faz o merge `--no-ff` em `main` antes da tag (já testado no `C-017`).

### 12.4 Backup

- **Repositório do ciclo:** `git -C "$CERNE_CICLO_A_DIR" push origin main --tags` depois de cada tag.
- **Dados em `cerne-avaliacao`:** ao fim de cada dia, sem abrir nenhum arquivo:
  ```bash
  cd "$AVAL" && git add dados docs/rdr.md docs/plano-ciclos.md docs/desvios.md && git commit -m "Ciclo A: dados e notas de $(date +%d/%m)" && git push origin main
  ```
  Não use `git diff` nem `git show` nesses arquivos (mostrariam números).
- **Transcripts:** `~/cerne/cfg-ciclo-a/projects/` nunca é apagado (fonte primária; os brutos copiados são a segunda cópia).

---

## 13. Exceções e recuperação

| Situação | O que fazer | Registro |
|---|---|---|
| Limite de uso da assinatura no meio da sessão | Coleta `manual` com `limite_uso` (4.6). Esperar a liberação. Sessão nova com o **mesmo** comando | Notas: data e hora do corte (P13) |
| Extensão ou VS Code travou ou fechou | Coleta `manual` com `falha` **antes** de abrir outra sessão. Sessão nova com o mesmo comando | Notas |
| Fechou a sessão sem `/coletar-sessao` | Coleta `manual` com `falha` imediatamente | Notas ("esquecimento") |
| Coletou com o ID errado | **Não** edite CSV. Registre em `desvios.md` (sessão, ID usado, ID correto). A correção é feita na Parte IV a partir dos brutos | `desvios.md` |
| Coleta deu erro (`FileNotFoundError`, etc.) | Copie a mensagem de erro. Não retome a sessão. Rode a coleta `manual` no terminal; se também falhar, guarde o session-id e me procure | Notas |
| Compactação automática ocorreu | Nada a fazer (permitida e registrada) | — |
| Agente em laço (repete o mesmo erro por mais de ~15 min) | Esc → `INTERVENÇÃO [interrupção]: <o que estava acontecendo>`. Depois, se for o caso, `INTERVENÇÃO [redirecionamento|<causa>]: <sintoma>`. Nunca diga a solução | M5 |
| Agente começou tela de extensão | `INTERVENÇÃO [redirecionamento|prd]` citando a §2 (P10) | M5 |
| Agente pergunta algo fora das pausas previstas | Seção 2.4 | M5 ou neutra |
| Timebox `atingido` | Commit de fechamento + `rf-incompleto a <ID>`; seguir para a próxima unidade; unidades dependentes são tentadas | `tags.csv`, notas |
| App não instala no iPhone (assinatura ou bundle id) | Sintoma na próxima sessão: `INTERVENÇÃO [correção|S3|amb]` com a mensagem exata | M5 |
| `push` recusado (arquivo > 100 MB) | **Não** reescreva o histórico. Mantenha só local e faça um backup do repositório do ciclo (`tar`) em disco externo. Anote | Notas, `desvios.md` |
| Erro que parece do **backend** (500, 404 inesperado, job preso) | Política **D16**: (1) confirmar com `curl` fora do app que o backend responde igual; (2) classificar: **não bloqueante** (há contorno; nenhum critério fica impossível) → não corrigir, registrar em `cerne-backend/docs/bugs_conhecidos.md` + `desvios.md` e decidir com a orientadora se o `known-bugs.md` do pacote é atualizado para os dois ciclos (arquivo congelado); **bloqueante** (critério impossível) → corrigir nos 3 ambientes, reconferir o schema, registrar como ameaça; o Ciclo A fica sem a correção a partir do ponto em que já passou. Nunca corrigir no meio de uma sessão | `desvios.md` |
| Precisou editar um arquivo do ciclo | Evite. Se inevitável: editar, e na **próxima** sessão `INTERVENÇÃO [edição manual|N1/N2|causa]: <arquivo e o que mudou>` | M5 |
| `/clear` digitado por engano | Não continue nessa sessão: colete (`/coletar-sessao <ID>`) e abra outra com o mesmo comando | `desvios.md` |
| `uv`/rede fora do ar, `fvm` falhando | Ambiente: resolver fora de sessão; se aconteceu durante a sessão e o agente percebeu, `INTERVENÇÃO [esclarecimento não solicitado|amb]` explicando que foi falha de ambiente já resolvida | Notas |
| Mudou algo no ambiente por engano (atualização) | **Parar** o ciclo; registrar; decidir com a orientadora (`X-002`) | `desvios.md` |

---

## 14. Encerramento do Ciclo A

**Data proposta:** 21/10/2026.

### 14.1 `A-003` 🧑 Completude dos dados (sem olhar números)

Os comandos abaixo só **contam** linhas e arquivos:
```bash
cd "$AVAL/dados/cicloA"
ls ~/cerne/cfg-ciclo-a/projects/-Users-wagnerduarte-Documents-Faculdade-2026-2-TCC-cerne-ciclo-a/*.jsonl | wc -l   # sessões do ciclo no Claude Code (só a pasta do repositório; os ensaios de /tmp ficam de fora)
tail -n +2 sessoes.csv | grep -vc ",instalacao,"            # sessões coletadas (deve ser igual ao total acima)
ls brutos/*.jsonl | grep -vc '^brutos/agent-'               # transcripts principais copiados
cut -d, -f2,3 tags.csv                                      # tags registradas: baseline, instalado, setup-done, 11 unidades
git -C "$CERNE_CICLO_A_DIR" tag | sort                      # mesmas tags no repositório
```
**Critério:** toda sessão tem linha (`GATE-A02` e `GATE-A02b` só rodam `/context` e não geram transcript); as 11 unidades têm `-done` ou `-incompleto`; os brutos estão copiados.

### 14.2 📏 Tag `cicloA/final`

```bash
cd "$CERNE_CICLO_A_DIR"
git status --short | head -40
git add -A -- . ':(exclude)build/' ':(exclude).dart_tool/' ':(exclude)ios/Pods/' ':(exclude)ios/.symlinks/' ':(exclude)ios/Flutter/ephemeral/' ':(exclude).flutter-plugins' ':(exclude).flutter-plugins-dependencies'
git commit -m "Cycle A final snapshot" || true
git tag cicloA/final
python3 "$AVAL/scripts/registrar_tag.py" --ciclo a --tag cicloA/final --tipo final \
  --commit "$(git rev-parse HEAD)" --data "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
git push origin main --tags
```

### 14.3 🔴 `GATE-A03` Nota de encerramento

Em `plano-ciclos.md`: o que aconteceu de inesperado, desvios registrados e decisões novas no RDR. Sem números.

---

## 15. Transição A → B

**Data:** 22/10/2026. Detalhada em `docs/plano-ciclo-B-bmad.md`, seção 3. Resumo:
- `X-001`: `git diff --stat protocolo-v1.0 -- …` (3.1) só com as diferenças documentadas em `desvios.md`.
- `X-002`: repetir 3.6 (versões) e confirmar que `claude-sonnet-5` continua disponível. Se não estiver, **parar** e decidir com a orientadora.
- `GATE-X01`: backend `ciclo-b` (Confirm email OFF, `replay-mode b replay`, chamada autenticada 200).
- `GATE-X02`: `dados/cicloB/aprendizado-previo.md`. A partir daí, **não abrir `cerne-ciclo-a`** até o fim do Ciclo B.
- Preparações específicas do B (helper de timebox do `PLAN`; seção 2 de `docs/plano-ciclo-B-bmad.md`).

---

## 16. Calendário

**Revisado em 07/10/2026 (decisão do Wagner):** o Ciclo A começou com 6 dias de atraso e **mantém as datas finais** (fim em 21/10, transição em 22/10). As datas por unidade abaixo são só um guia de ritmo: a regra de parada continua sendo a timebox em tempo ativo (P7), e uma unidade que atrasar empurra as seguintes sem alterar nenhuma regra.

| Data | Etapa | Saída |
|---|---|---|
| 07/10 | Seção 3 (preparação) + A0 + A1 | `cicloA/baseline`, `cicloA/instalado`, `GATE-A02`, `cicloA/setup-done` |
| 08–09/10 | A2 F000 (12 h) | `cicloA/f000-done` |
| 10/10 | A3 RF03 | `cicloA/rf03-done` |
| 11–12/10 | A4 RF01 | `cicloA/rf01-done` |
| 12–13/10 | A5 RF02 | `cicloA/rf02-done` |
| 14/10 | A6 RF07 | `cicloA/rf07-done` |
| 15/10 | A7 RF06 | `cicloA/rf06-done` |
| 16/10 | A8 RF04 | `cicloA/rf04-done` |
| 17/10 | A9 RF10 | `cicloA/rf10-done` |
| 18/10 | A10 RF08 | `cicloA/rf08-done` |
| 19/10 | A11 RF05 | `cicloA/rf05-done` |
| 20/10 | A12 RF09 | `cicloA/rf09-done` |
| 21/10 | Encerramento | `cicloA/final`, `GATE-A03` |
| 22/10 | Transição | `GATE-X02` |

Se o ritmo não couber até 21/10, a decisão de estender (ou não) é tomada de novo, registrada nas notas e em `desvios.md` — nunca encurtando timebox.

Em paralelo (fora das sessões, em `cerne-avaliacao`): a trilha do harness (`H-001`–`H-006`), com corte da hold-out e da M8b em **06/11** (`GATE-H01`). Ela nunca toca `cerne-ciclo-a`.

---

## Apêndice A — Comandos prontos

```bash
# Abrir sessão
abrir-ciclo a

# Gerar o argumento da primeira mensagem de cada passo (digite o comando à mão, depois Cmd+V; D-014)
{ cat "$AVAL/prompts/P-SETUP.md"; } | pbcopy   # só o argumento: digite `/speckit-constitution ` à mão (com o espaço) e cole depois (D-014)
{ cat "$AVAL/prompts/P-F000.md"; printf '\n\n'; cat "$AVAL/prompts/P-GLOBAL.md"; } | pbcopy   # só o argumento: digite `/speckit-specify ` à mão (com o espaço) e cole depois (D-014)
{ cat "$AVAL/prompts/P-RF03.md"; } | pbcopy   # só o argumento: digite `/speckit-specify ` à mão (com o espaço) e cole depois (D-014); troque RF03
{ cat "$AVAL/prompts/P-TECH.md"; } | pbcopy   # só o argumento: digite `/speckit-plan ` à mão (com o espaço) e cole depois (D-014)
# Sem argumento: /speckit-clarify, /speckit-checklist, /speckit-tasks, /speckit-analyze, /speckit-implement, /speckit-converge

# Última mensagem de toda sessão
/coletar-sessao <ID>

# Verificação P6
cd "$CERNE_CICLO_A_DIR" && fvm flutter analyze && fvm flutter test && fvm flutter run -d "$IPHONE"

# Fechamento de unidade
cd "$CERNE_CICLO_A_DIR" && git add -A -- . ':(exclude)build/' ':(exclude).dart_tool/' ':(exclude)ios/Pods/' ':(exclude)ios/.symlinks/' ':(exclude)ios/Flutter/ephemeral/' ':(exclude).flutter-plugins' ':(exclude).flutter-plugins-dependencies' && git commit -m "<ID>: closing snapshot at unit completion"
cd "$AVAL" && scripts/concluir-rf a <ID>          # ou: scripts/rf-incompleto a <ID>
git -C "$CERNE_CICLO_A_DIR" push origin main --tags

# Coleta manual (P13)
cd "$CERNE_CICLO_A_DIR" && CLAUDE_CONFIG_DIR=~/cerne/cfg-ciclo-a python3 "$AVAL/scripts/coletar_sessao.py" manual <ID> --ciclo a --session-id <id> --motivo-fim <limite_uso|falha> --versao-claude-code "$(claude --version)" --config-raciocinio high --otel-output ~/cerne/otelcol/output.jsonl

# Backup diário dos dados
cd "$AVAL" && git add dados docs/rdr.md docs/plano-ciclos.md docs/desvios.md && git commit -m "Ciclo A: dados e notas de $(date +%d/%m)" && git push origin main
```

---

## Apêndice B — Correções em relação ao `plano-ciclos.md` (Parte II)

| # | Parte II dizia | Correto | Fonte |
|---|---|---|---|
| 1 | `/speckit.constitution`, `/speckit.specify`… (ponto) | `/speckit-constitution`, `/speckit-specify`… (hífen) | `protocolo.md` §4.2; CLI instalado |
| 2 | "o app roda no `sim-dev`" (P6) | Roda no **iPhone 16 Pro físico** (`fvm flutter run -d 00008140-000125D13C2A801C`) | P11 revisado, `GATE-C16` |
| 3 | RF03: "Face ID pelo menu Features do simulador" | Face ID real do aparelho; falha provocada cobrindo a câmera TrueDepth | P11 revisado |
| 4 | RF01: "sem câmera no simulador; foto pela galeria; microfone do Mac" | Câmera e microfone reais do iPhone | P11 revisado |
| 5 | A1: "Tag `cicloA/setup-done` (via `concluir-rf a SETUP`)" | `concluir-rf` rejeita `SETUP`: commit de fechamento + `git tag` + `registrar_tag.py --tipo setup-done` | `_ciclo_common.sh`; decisão de 01/10/2026 |
| 6 | (implícito) a metodologia faz os commits | O Spec Kit v1.0.10 sem a extensão `git` não commita: commit de fechamento antes de toda tag | Texto do `speckit-specify`; D-002 |
| 7 | Encerramento: "Tag `cicloA/final`" sem procedimento | Manual (14.2) | `registrar_tag.py` aceita `final` |
| 8 | Dependências: A8 RF04 "F000"; A12 RF09 "F000" | Pelos prompts congelados: RF04 depende de F000 e RF03; RF09 de F000 e RF01 | `prompts/P-RF04.md`, `P-RF09.md` |
| 9 | Sessão de correção sem detalhar a fase | O protocolo diz `IMPL`, mas o script grava `SETUP`: re-segmentar na Parte IV | §4.4; `coletar_sessao.py` |
| 10 | `GATE-A02` "nenhuma skill além das do Spec Kit" | Idem, mais a skill pessoal da conta já registrada como ameaça (`C-011`) | `protocolo.md` §6.4 |
| 11 | Ordem `clarify` → `checklist` → `plan` | **Alterada (D-016, 11/10):** `clarify` → `plan` → `checklist` → `tasks`; o script do `checklist` exige `plan.md` | `GATE-C09`, `desvios.md` |

---

## Apêndice C — Pendências abertas que afetam o ciclo ou a Parte IV

| Pendência | Efeito | Quando resolver |
|---|---|---|
| D-001 `P-SETUP` × contrato de autenticação | Bloqueia A1 | **Hoje, antes da A1** |
| D-002 commit de fechamento; D-003 perguntas espontâneas | Bloqueiam a primeira tag e a primeira pergunta espontânea | **Hoje** |
| Segmentação das sessões de correção (`SETUP` em vez de `IMPL`) | Só dados por fase; brutos preservados | Parte IV (re-segmentar) |
| Nome do comando no transcript não confirmado | Segmentação por fase | Checagem 8.5, depois da A1 |
| Evento de compactação (`compact_boundary`) e `rate_limit_s` não vistos em sessão real | `n_compactacoes`/`rate_limit_s` podem sair 0 | Quando ocorrerem; brutos preservados |
| `OTEL_TOLERANCE` = 2% (escolha do script, sem fonte) | Só o aviso de divergência | Revisar antes da Parte IV |
| **Cache de IA de desenvolvimento não é apagado pelo reset hospedado** (`TRUNCATE` não toca `experiment.ai_replay_cache`, §7 item 7). Em `REPLAY_MODE=replay`, todo uso do app no desenvolvimento grava no cache, e a passada `record` do `V-002` exportaria esse cache misturado | Risco à validade do `replay_strict` na Parte IV (o B pode ser servido por gravações do seu próprio desenvolvimento) | Antes do `V-002`: decidir truncar `experiment.ai_replay_cache` antes da passada `record` (com desvio) |
| `C-024` (interceptação do mitmproxy não confirmada) | Só Parte IV | Antes da Parte IV |
| `TEST_FAULT_KEY` (valor) | Só hold-out | Antes da Parte IV |
| `GATE-H01` (hold-out × checklist; M8b) | Parte IV | 06/11 |

---

## Apêndice D — Textos propostos para `docs/desvios.md` e `docs/rdr.md`

**`desvios.md`** (uma linha cada, preencher a data real; nenhuma é aplicada sem a sua decisão):

| # | Data | Ciclo / unidade | O que mudou ou aconteceu | Motivo | Arquivos afetados (hash antes → depois) | Efeito nas métricas | Declarado na monografia em |
|---|---|---|---|---|---|---|---|
| D-001 | 01/10/2026 | Ambos, antes da A1 | Parágrafo "Backend" do `P-SETUP` corrigido: `Authorization` leva a anon key só em signup/login/refresh e o token do usuário nos 20 endpoints `bearerAuth`; `apikey` sempre | O texto congelado contradizia o contrato (`openapi.yaml`) e o gateway do backend; seguido à risca, toda chamada autenticada falharia com `AUTH_INVALID` | `prompts/P-SETUP.md` e hash combinado de `prompts/` em `hashes-congelamento.md` (antes `a97753fd…5c36`) | Nenhum ciclo rodou com o texto antigo; evita intervenções `ctx` causadas pelo instrumento | Ameaças à validade (instrumento) |
| D-002 | 01/10/2026 | Ambos | Procedimento acrescentado: "commit de fechamento" do estado do repositório antes de toda tag (`setup-done`, `plan-done`, unidade, `final`), excluindo artefatos de build do Flutter | Spec Kit v1.0.10 sem a extensão `git` (proibida pelo `GATE-C08`) não faz commits; o BMAD commita só no fim do `bmad-build`; `concluir-rf` só faz merge e tag. Sem isso, as tags não conteriam o trabalho da unidade | Nenhum arquivo congelado | Nenhum efeito em M1–M5 (fora de sessão, sem alteração de conteúdo); garante M4, M6–M15 | Método |
| D-003 | 01/10/2026 | Ambos | Interpretação de lacuna da P5b: pergunta espontânea do agente que admite confirmação → neutra (`Yes, proceed.`); que pede escolha ou informação → `INTERVENÇÃO [esclarecimento não solicitado]` com a frase padrão ou a informação do pacote/RDR | P5b só prevê confirmações e colar erros; a taxonomia não tem tipo para "esclarecimento solicitado" | Nenhum | M5 conta essas respostas como `esclarecimento não solicitado`; reportar à parte na análise | Método / ameaças |

**`rdr.md`** — sugestões a gravar **na primeira ocorrência** (o texto exato passa a valer para todas as equivalentes):

| Comando/skill | Pergunta (resumo) | Fonte | Resposta (texto exato) |
|---|---|---|---|
| `speckit-implement` | "Some checklists have unchecked items. Do you want to proceed…? (yes/no)" | decisão | `PROCESSO: yes` |
| `speckit-analyze` | "Would you like me to suggest concrete remediation edits…?" | decisão | `PROCESSO: Yes.` |
| `speckit-constitution` | Data de ratificação desconhecida | decisão | `PROCESSO: Use today's date.` |
| qualquer | Preferência "A ou B?" | `GATE-C11` | `PROCESSO: Use your technical judgment, following the input package.` |
