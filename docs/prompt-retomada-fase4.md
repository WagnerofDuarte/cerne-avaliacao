# Prompt de retomada — colar no Claude Code, aberto em `cerne-avaliacao`

Sou o Wagner. Este repositório é o `cerne-avaliacao`, o instrumento de avaliação do meu TCC. Nele vamos retomar o plano dos ciclos comparativos a partir da **Fase 4**. As Fases 0, 1, 2, 3 e 7 foram feitas numa conversa anterior e estão registradas nos arquivos deste repositório.

## Leia antes de qualquer ação
1. `docs/plano-ciclos.md` inteiro. Dê atenção especial às seções "Encerramento da Fase N" das Fases 0 a 3 e 7, à Fase 4 em diante, ao "Checklist de congelamento do protocolo", aos "Itens em aberto" e ao "Apêndice — Erros comuns a evitar".
2. `docs/protocolo.md`: decisões P1–P14, regras operacionais (seção 3), regras por metodologia (seção 4, com a **4.6 "Pendências verificadas na Fase 4"**), composição do pacote (5.1), divergências (seção 7) e especificação da avaliação (seção 8).
3. `docs/Metricas_e_Skills_Ciclos.md` (v1.0): o que é medido, as skills e o esquema de dados (§8).

## Primeira ação: situação das pendências manuais
Antes da Fase 4, me pergunte em que pé estão estes itens. Não os marque como feitos sem a minha confirmação:
- `GATE-C00` e `C-000`: este repositório e sua estrutura. Confira com `tree -L 3` e `git check-ignore segredos/teste`.
- `GATE-C13`: minha revisão lado a lado do pacote (`docs/revisoes/gate-c13-lista-de-revisao.md`). Os hashes são calculados aqui, no terminal, sobre os arquivos já versionados: `sha256sum` de cada arquivo de `entrada/`, o hash do pacote inteiro (`find entrada -type f | sort | xargs sha256sum | sha256sum`), o hash de `prompts/` e o do HTML derivado `entrada/prototype/cerne-prototype.html`. Grave os resultados no `protocolo.md`, seção 5.1.
- `C-021`: minha aplicação à mão dos 4 exemplos sintéticos de `harness/juiz/`.
- `GATE-C22`: minha revisão de `holdout/` e `harness/`.

## Como conduzir a partir da Fase 4
1. Siga o plano **na ordem, uma tarefa por vez**: Fase 4 (`GATE-C14` → `C-010` → `GATE-C15` → `C-011` → `C-012` → `C-013` → `GATE-C16`), depois a Fase 5 e depois a Fase 6.
2. Em cada 🔴 GATE, apresente as opções em múltipla escolha, com a recomendação do plano (⭐) e a justificativa com seção e ID. Se discordar, diga. No máximo 3 perguntas por vez; espere a minha resposta.
3. Tarefas `[MANUAL]` são minhas. Você prepara os comandos e confere o resultado, mas não marca como concluído sem a minha confirmação.
4. Ao fim de cada tarefa, marque `[x]` no plano só se o critério foi verificado, e escreva uma linha de registro.
5. Ao fim de cada fase, preencha "Encerramento da Fase N — notas para quem retomar" e atualize o `protocolo.md`.
6. Em divergência entre o plano e os documentos-fonte, as fontes prevalecem: aponte a divergência e não a resolva sozinho.
7. Seja crítico: aponte problemas no plano, não o execute cegamente.

## Conferências que só podem ser feitas aqui (protocolo, seção 4.6)
- **Spec Kit v1.0.10** (`C-010`): leia as notas de versão 1.0.4–1.0.5 e 1.0.7–1.0.10 antes de instalar; isso fecha o `GATE-C08`. Registre o modo de integração padrão para o Claude Code. Confira o texto dos comandos contra a lista de gatilhos `PROCESSO` do protocolo (seção 4.5).
- **BMAD v6.11.0**: instalação só por flags (`--modules bmm --tools claude-code --yes`, `--set` de idioma inglês; chaves via `--list-options bmm`). Confira os nomes exatos das skills e se o `bmad-project-context` grava no `AGENTS.md`, e se o Claude Code lê esse arquivo. Confira também o formato das stories: se não houver checkboxes de tarefa, vale a regra alternativa da `M6_tasks` (`harness/regras.md`, seção 5). Confira que nenhuma definição de agente tem modelo próprio e o texto das skills contra a lista de gatilhos.
- **Claude Code** (P1–P1c): `claude-sonnet-5`, `CLAUDE_CODE_EFFORT_LEVEL=high`, `CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5` com `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001`, OpenTelemetry local. No `GATE-C21`, confira o campo `model` do transcript de um subagente e o local dos transcripts de subagentes (é a base da soma de tokens da M3).
- **Superfície (P2):** extensão do Claude Code no VS Code. O `abrir-ciclo` abre o VS Code com o `CLAUDE_CONFIG_DIR` do ciclo; as versões do VS Code e da extensão ficam travadas. No `C-016`, confira quais marcadores a extensão grava no transcript quando injeta arquivo aberto ou seleção (coluna `n_msgs_contexto_ide`).
- **Simulador (P11):** frame de 390 × 844. Candidatos: iPhone 16e ou iPhone 14, conforme a disponibilidade no Xcode travado (`GATE-C15`).
- **Cache (`GATE-C19`):** confira se `replay-cache-import.ts --force` mescla ou sobrescreve o cache. Eu envio o arquivo quando você pedir.

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

O critério são 4 transcripts sintéticos, rodados nos três modos. Se o prazo apertar, me avise **antes** de cortar escopo.

## Não fazer
- Não abrir nem ler os repositórios `cerne-ciclo-a`/`cerne-ciclo-b` fora do que o plano manda (as verificações de ambiente das Fases 4–5 são exceção).
- Não rodar nenhum script de medição sobre código de ciclo antes da Parte IV. O harness só é testado no repositório de calibração.
- Não reabrir D1–D18 nem propor mudanças no backend congelado.
- Não alterar arquivos de `entrada/`, `prompts/`, `holdout/` ou `harness/` depois dos seus gates sem registrar como desvio. Antes do congelamento, qualquer mudança passa pelo gate correspondente.
- Não iniciar o Ciclo A: pare no **Checklist de congelamento do protocolo** (`GATE-C23`) e espere a minha confirmação item a item.
- **Antes da transição A → B (22/10):** a Parte III do plano (B0–B3 e o bloco do Ciclo B) ainda descreve o fluxo antigo do BMAD e precisa ser reescrita conforme o `GATE-C10` e o protocolo, seção 4.3. Isso não é tarefa da Fase 4, mas não deixe passar.
