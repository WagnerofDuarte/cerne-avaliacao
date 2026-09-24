# Prompt de retomada — colar no Claude Code, aberto em `cerne-avaliacao`

Sou o Wagner. Este repositório é o `cerne-avaliacao`, o instrumento de avaliação do meu TCC. As Fases 0, 1, 2, 3 e 7 estão **fechadas** (feitas numa conversa anterior, registradas neste repositório). Vamos retomar o plano a partir da **Fase 4**.

## Leia antes de qualquer ação
1. `docs/plano-ciclos.md` inteiro. Dê atenção especial às seções "Encerramento da Fase N" das Fases 0 a 3 e 7 (todas fechadas — leia mesmo assim, é onde estão os achados que afetam a Fase 4 em diante), à Fase 4 em diante, ao "Checklist de congelamento do protocolo", aos "Itens em aberto" e ao "Apêndice — Erros comuns a evitar".
2. `docs/protocolo.md` inteiro — em especial as seções 4 (regras por metodologia, com a **4.6 "Pendências verificadas na Fase 4"**), 5 (pacote de entrada, com os hashes), 8 (avaliação) e **9 (cache de IA e reset — leia com atenção; é um achado de correção feito em 24/09, depois de uma versão do plano que tinha um bug real)**.
3. `docs/Metricas_e_Skills_Ciclos.md` (v1.0): o que é medido, as skills e o esquema de dados (§8).

## Situação: nada pendente antes da Fase 4
Todos os itens manuais das Fases 0–3 e 7 foram concluídos e registrados em 24/09/2026: `GATE-C00`/`C-000` (repositório), `GATE-C13` (revisão do pacote + hashes), `C-021` (rubricas do avaliador), `GATE-C22` (revisão de `holdout/`/`harness/`), `C-014` (`.env` dos dois ciclos). Não pergunte por eles de novo — confirme lendo os registros nos próprios itens do plano, e comece direto pelo `GATE-C14`.

## Como conduzir a partir da Fase 4
1. Siga o plano **na ordem, uma tarefa por vez**: Fase 4 (`GATE-C14` → `C-010` → `GATE-C15` → `C-011` → `C-012` → `C-013` → `GATE-C16`), depois a Fase 5 e depois a Fase 6.
2. Em cada 🔴 GATE, apresente as opções em múltipla escolha, com a recomendação do plano (⭐) e a justificativa com seção e ID. Se discordar, diga por quê. No máximo 3 perguntas por vez; espere a minha resposta.
3. Tarefas `[MANUAL]` são minhas. Você prepara os comandos e confere o resultado, mas não marca `[x]` sem a minha confirmação.
4. Ao fim de cada tarefa, marque `[x]` no plano só se o critério foi verificado, e escreva uma linha de registro com a data.
5. Ao fim de cada fase, preencha "Encerramento da Fase N — notas para quem retomar" e atualize o `protocolo.md`.
6. Em divergência entre o plano e os documentos-fonte, as fontes prevalecem: aponte a divergência e não a resolva sozinho.
7. Seja crítico: aponte problemas no plano, não o execute cegamente — foi assim que achamos e corrigimos o bug do cache (seção 9 do protocolo) antes de chegar aqui.
8. **Se aparecer uma decisão que não depende de nada instalado na máquina** (uma escolha pura, sem precisar rodar comando ou ler documentação externa): resolva aqui mesmo, do mesmo jeito — não precisa voltar para a outra conversa. Só volte para lá se precisar pesquisar algo que você não consiga fazer bem sozinho, achar uma contradição de desenho como a do cache, ou eu preferir decidir por lá.

## Conferências que só podem ser feitas aqui (protocolo, seção 4.6)
- **Spec Kit v1.0.10** (`C-010`): já lidas as notas de versão 1.0.0–1.0.10 (`GATE-C08` fechado) — não precisa reler. Confira o texto real dos comandos instalados contra a lista de gatilhos `PROCESSO` do protocolo (seção 4.5), porque essa lista foi montada em parte por inferência, sem a ferramenta instalada.
- **BMAD v6.11.0**: instalação só por flags (`--modules bmm --tools claude-code --yes`, `--set` de idioma inglês; chaves via `--list-options bmm`). Confira os nomes exatos das skills, se o `bmad-project-context` grava no `AGENTS.md` e se o Claude Code lê esse arquivo, e o formato das stories: se não houver checkboxes de tarefa, vale a regra alternativa da `M6_tasks` (`harness/regras.md`, seção 5 — é o único ponto do `C-022` ainda condicional). Confira também o texto real das skills contra a seção 4.5, e que nenhuma definição de agente tem modelo próprio (neutralizado por `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, mas confirme).
- **Claude Code** (P1–P1c): `claude-sonnet-5`, `CLAUDE_CODE_EFFORT_LEVEL=high`, `CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5` com `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001`, OpenTelemetry local. No `GATE-C21`, confira o campo `model` do transcript de um subagente e o local onde ficam gravados os transcripts de subagentes — é a base da soma de tokens da M3.
- **Superfície (P2):** extensão do Claude Code no VS Code. O `abrir-ciclo` abre o VS Code com o `CLAUDE_CONFIG_DIR` do ciclo; trave as versões do VS Code e da extensão. No `C-016`, confira quais marcadores a extensão grava no transcript quando injeta arquivo aberto ou seleção (coluna `n_msgs_contexto_ide`).
- **Simulador (P11):** frame de 390 × 844. Candidatos: iPhone 16e ou iPhone 14, conforme a disponibilidade no Xcode travado (`GATE-C15`).
- **`TEST_FAULT_KEY` real dos ambientes hospedados** (`GATE-C18`): o `.env.local` do backend só tem o valor de desenvolvimento local; confirme o valor configurado em `ciclo-a` e `ciclo-b` de verdade antes de escrever o proxy do `harness`.
- **Senha do banco de `ciclo-b`** (`GATE-C18`/`C-015`): recebi duas grafias da mesma senha (bruta e com `%40`); `segredos/db.ciclo-b.env` está com a versão codificada — teste a conexão e corrija se necessário.
- **Cache de IA — já resolvido, só executar.** O achado e a correção completa estão no `protocolo.md`, seção 9, e propagados no `V-002` e em `holdout/cenarios.md`/`rnf09.md`. Resumo: `record` e `replay` gravam igual no backend; um reset apaga o schema `experiment` inteiro (cache, config do worker); por isso `reset-ambiente` (`C-015`) é sempre um procedimento de 4 passos (reset → reconfigurar worker → reimportar `harness/cache-ciclo-a.json` se existir → rodar `backfill-seed-embeddings.ts`), nunca um reset isolado. `--force` do `replay-cache-import.ts` nunca é usado no fluxo normal — se o script recusar, o reset não rodou de verdade; não contorne com `--force`.

## Carga da Fase 6 (prazo apertado: 29/09)
A `/coletar-sessao` (`C-016`) tem **três modos** (skill, hook `SessionEnd` + `scripts/marcar-sessao`, `manual` para cortes por limite de uso) e precisa de:
- soma dos transcripts principal e de subagentes;
- tempo ativo com teto de 30 min nas esperas pelo pesquisador;
- segmentação por fase (tabela do protocolo, 4.4);
- extração de `INTERVENÇÃO [tipo|Sn|N1-N2|causa]` e `PROCESSO:`;
- conferência com o OTel (`div_otel`);
- `n_msgs_contexto_ide`;
- avisos de prefixo mal formado;
- exibição restrita (nunca tokens, tempo ou custo).

O critério são 4 transcripts sintéticos, rodados nos três modos. O `scripts/reset-ambiente` (`C-015`) também é maior do que um wrapper simples — ver a seção do cache acima. Se o prazo apertar, me avise **antes** de cortar escopo.

## Não fazer
- Não abrir nem ler os repositórios `cerne-ciclo-a`/`cerne-ciclo-b` fora do que o plano manda (as verificações de ambiente das Fases 4–5 são exceção).
- Não rodar nenhum script de medição sobre código de ciclo antes da Parte IV. O harness só é testado no repositório de calibração.
- Não reabrir D1–D18 nem propor mudanças no backend congelado.
- Não alterar arquivos de `entrada/`, `prompts/`, `holdout/` ou `harness/` depois dos seus gates sem registrar como desvio. Antes do congelamento, qualquer mudança passa pelo gate correspondente.
- Não rodar `reset-ambiente` (nem `db reset` isolado) sem os 4 passos completos — ver seção do cache acima.
- Nunca colocar `ANTHROPIC_API_KEY`, `VOYAGE_API_KEY`, `SUPABASE_DB_URL`, `service_role` ou qualquer coisa de `segredos/db.*.env` no `.env` do app. O `.env` do app tem só `FUNCTIONS_BASE_URL` e `SUPABASE_ANON_KEY` (`P-SETUP.md`).
- Não iniciar o Ciclo A: pare no **Checklist de congelamento do protocolo** (`GATE-C23`) e espere a minha confirmação item a item.
- **Antes da transição A → B (22/10):** a Parte III do plano (B0–B3 e o bloco do Ciclo B) ainda descreve o fluxo antigo do BMAD e precisa ser reescrita conforme o `GATE-C10` e o protocolo, seção 4.3. Isso não é tarefa da Fase 4, mas não deixe passar.
