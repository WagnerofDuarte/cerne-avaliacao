# Plano de execução — Ciclo B (BMAD-METHOD v6.11.0)

**Projeto:** TCC Wagner Duarte — Spec Kit × BMAD-METHOD (veículo: app Cerne)
**Versão deste documento:** 1.1 — 01/10/2026 (para execução a partir de 22/10/2026; decisões D-001 a D-008 tomadas e aplicadas, commit `6c9686d`)
**Base:** protocolo congelado (tag `protocolo-v1.0`) — `docs/protocolo.md` §4.3 (`GATE-C10`), §4.4, §4.5, §5 (tabela de entrega), `docs/Metricas_e_Skills_Ciclos.md` v1.0, `prompts/`, `entrada/`, `scripts/`.
**Conferido contra:** BMAD-METHOD v6.11.0 reinstalado em pasta descartável com as flags exatas do `instalar-metodologia b` (49 skills, texto real de cada skill usada); `cerne-backend` (commit `5a0f809`); `cerne-ciclo-b` no GitHub (vazio em 01/10/2026).
**Precedência:** protocolo congelado > comportamento real das ferramentas > este documento > `plano-ciclos.md` Parte III. **A Parte III do `plano-ciclos.md` descreve o fluxo antigo do BMAD e não deve ser seguida** (lista de diferenças no Apêndice B).

> **Onde este documento mora:** fora do VS Code do ciclo. Ele descreve métricas e protocolo e nunca pode ser aberto, colado ou citado dentro de uma sessão medida.

---

## Sumário

0. Como usar este documento
1. Mapa dos repositórios e ambientes
2. Antes de começar — decisões e correções necessárias
3. Transição A → B e preparação do Ciclo B (22/10)
4. Anatomia de uma sessão medida
5. Como escrever ao agente
6. Tempo, timebox e pausas (incluindo as 32 h do planejamento)
7. B0 — Instalação e baseline
8. B1 — Setup (`bmad-project-context`)
9. B2 — Análise (`PLAN`)
10. B3 — Planejamento (`PLAN`)
11. B4 — Solução (`PLAN`) e tag `plan-done`
12. Mapa story → unidade e ordem de implementação
13. B5 — Bloco-padrão de implementação por unidade
14. Fichas das unidades (B5.1–B5.11)
15. Matriz de métricas — o que é coletado, quando e por quem
16. Git, tags e backup
17. Exceções e recuperação
18. Encerramento do Ciclo B
19. Calendário
- Apêndice A — Comandos prontos
- Apêndice B — Correções em relação ao `plano-ciclos.md` (Parte III)
- Apêndice C — Pendências abertas
- Apêndice D — Textos propostos para `desvios.md`, `rdr.md` e o script `faixa-plan`

---

## 0. Como usar este documento

### 0.1 Legenda

| Marca | Quem faz | Onde |
|---|---|---|
| 🧑 **[MANUAL]** | Você (Wagner) | Terminal do Mac, painel do Supabase, iPhone |
| 🤖 **[AGENTE]** | O agente medido (Claude Code, `claude-sonnet-5`) executando a skill do BMAD | VS Code aberto por `abrir-ciclo b` |
| ⚙️ **[SCRIPT]** | Script de `cerne-avaliacao/scripts/` rodado por você | Terminal |
| 📏 **[COLETA]** | Ato que grava dado (`/coletar-sessao`, tag, `tags.csv`, `mapa-stories.csv`) | Sessão ou terminal |
| 🧪 **[SESSÃO]** | Sessão medida | VS Code do ciclo |
| 🔴 **[PORTÃO]** | Parar e conferir | — |
| ⚠️ | Armadilha conhecida | — |

Ninguém além do agente medido trabalha dentro das sessões. No BMAD, os "agentes" (analista, PM, arquiteto, dev, UX) são **skills** instaladas no próprio repositório. O protocolo usa as skills de workflow diretamente (`bmad-prd`, `bmad-build`…), nunca as skills de persona (`bmad-agent-*`).

### 0.2 IDs de coleta do Ciclo B

| ID | Quando |
|---|---|
| `SETUP` | Sessão do `bmad-project-context` (B1) |
| `PLAN` | As 11 sessões de B2–B4 (análise, planejamento, solução) **e** cada `bmad-retrospective` |
| `F000`, `RF01`…`RF10` | Sessões de `bmad-build`, `bmad-code-review` e `bmad-qa-generate-e2e-tests` das stories da unidade (pelo `mapa-stories.csv`), e as sessões de correção |

---

## 1. Mapa dos repositórios e ambientes

```
cerne-backend ──► cerne-backend-handoff ──► cerne-avaliacao (laboratório)
 (congelado)        (só documentação)          │  entrada/ ──cópia──► cerne-ciclo-b/docs/input/
     │                                         │  prompts/ ──colados no chat (tabela de entrega)
     │ deploy                                  │  scripts/ ──operam cerne-ciclo-b e o Supabase
     ▼                                         │  dados/cicloB/ ◄── /coletar-sessao, scripts, mapa-stories.csv
 Supabase "ciclo-b" (bpoutqdbpwccimridgdi) ◄── app do cerne-ciclo-b
```

| Peça | Papel no Ciclo B | Regra |
|---|---|---|
| `cerne-backend` (`$CERNE_BACKEND_DIR`) | Scripts usados pelos wrappers | Nunca alterar (D1–D18). Defeito → D16 (seção 17) |
| `cerne-avaliacao` (`$AVAL`) | Laboratório: scripts, skill, prompts, dados, RDR, desvios | Nunca aberto no VS Code do ciclo |
| `cerne-ciclo-a` | Ciclo anterior | **Proibido abrir** do `GATE-X02` até o fim do Ciclo B |
| `cerne-ciclo-b` (`$CERNE_CICLO_B_DIR`) | O app do B, mais o BMAD instalado em `_bmad/` e `.claude/skills/`; artefatos em `_bmad-output/planning-artifacts/` e `_bmad-output/implementation-artifacts/` | Você não edita nenhum arquivo (inclui `AGENTS.md`, `_bmad*/`, `sprint-status.yaml`) |
| Supabase `ciclo-b` | Backend do ciclo, `REPLAY_MODE=replay` | Schema idêntico ao do `ciclo-a` (`f33a12b4…9868e2`) |
| `~/cerne/cfg-ciclo-b/` | `CLAUDE_CONFIG_DIR` do B (`settings.json` idêntico ao do A + skill de coleta) | Não editar |
| `~/cerne/otelcol/` | Coletor OTel | Rodando durante as sessões |
| iPhone 16 Pro | Ambiente de desenvolvimento e verificação | Sem certificado ou proxy do mitmproxy (`C-024`) |

**Onde o BMAD grava** (config gerada pela instalação, `_bmad/bmm/config.yaml`):

| Chave | Valor |
|---|---|
| `planning_artifacts` | `_bmad-output/planning-artifacts` (brief, PRD, UX, arquitetura, `epics.md`…) |
| `implementation_artifacts` | `_bmad-output/implementation-artifacts` (`sprint-status.yaml`, specs das stories, contexto de épico, revisões, retrospectivas) |
| `project_knowledge` | `docs` (onde está `docs/input/`) |
| `communication_language` / `document_output_language` | `English` / `English` |

---

## 2. Antes de começar — decisões e correções necessárias

### 2.1 Herdadas do Ciclo A (já decididas antes da A1)

| # | Ponto | Efeito no B |
|---|---|---|
| D-001 | `P-SETUP` × contrato de autenticação — corrigido | O B usa **o mesmo** `P-SETUP` corrigido usado no A |
| D-002 | Commit de fechamento antes de toda tag | No B: antes de `setup-done`, **`plan-done`**, cada unidade e `final`. O `bmad-build` commita sozinho no fim de cada story, mas o planejamento, o `code-review` e o QA deixam arquivos sem commit |
| D-003 | Perguntas espontâneas | Mesma regra do A (seção 5.6) |
| `concluir-rf` × `SETUP` | Contorno documentado | No B também para `plan-done` (seções 8.4 e 11.4) |
| Modo de permissão | Padrão, aprovar uma vez | Idem. O BMAD roda muitos `uv run` (83 menções nas skills): espere muitos pedidos de permissão |

### 2.2 🔴 BLOQUEANTE para o B — a coleta mostra a faixa errada para o `PLAN` — ✅ decidido (opção ⭐), registrado em `desvios.md`

**Achado.** `coletar_sessao.py` (congelado) só tem teto para F000 (12 h). Todo o resto, `PLAN` inclusive, usa 8 h. A timebox do planejamento global é **32 h** de tempo ativo para B2–B4 juntos, com as retrospectivas **fora** (R23). Com o script atual, a faixa exibida depois das sessões `PLAN` chega a "atingido" às 8 h e não diz nada entre 8 e 32 h. Como você está cego aos números, não teria como saber quando parar.

- ⭐ **Script auxiliar novo, `scripts/faixa-plan`** (não altera nenhum arquivo congelado). Soma só as sessões `PLAN` do Ciclo B anteriores à tag `cicloB/plan-done` e imprime **apenas** a faixa em relação a 32 h. Texto pronto no Apêndice D. Registrar como D-004 em `desvios.md` e commitar na transição (22/10). Depois de cada coleta `PLAN` de B2–B4, você roda `scripts/faixa-plan` e **ignora** a linha "Timebox da unidade" da coleta.
- Alternativa: alterar `TIMEBOX_SECONDS` no `coletar_sessao.py`. Mexe em script congelado (novo hash) e ainda contaria as retrospectivas.

### 2.3 Sessões de correção no B — sem skill, como no A — ✅ decidido (opção ⭐), registrado em `desvios.md`

O `plano-ciclos.md` (Parte III) dizia que a correção no B seria "numa sessão nova com o workflow de implementação". O protocolo congelado (P4, §3.3 regra 13) diz: **sessão nova aberta pela mensagem `INTERVENÇÃO [correção|…]`**.
- ⭐ Seguir o protocolo: a primeira mensagem é a intervenção, **sem** `/bmad-build`. Dois motivos:
  1. **Simetria com o A.**
  2. **Parse da coleta.** Uma mensagem que começa com `/bmad-build INTERVENÇÃO …` não começa com `INTERVENÇÃO` e **não seria contada** como intervenção.

  Registrar como D-005 (esclarecimento de procedimento).

### 2.4 Escolha da story a implementar — você escolhe pela unidade — ✅ decidido (opção ⭐), registrado em `desvios.md`

O BMAD v6.11 recomenda a próxima story pela ordem do `sprint-status.yaml`. As unidades, porém, precisam fechar na ordem P9 (F000 → RF03 → …), com uma tag por unidade.
- ⭐ Você chama `/bmad-build <story_key>` com as stories **da unidade atual** (pelo `mapa-stories.csv`), na ordem em que aparecem no `sprint-status.yaml`. É o equivalente exato do Ciclo A, em que você escolhe qual `P-RFxx` especificar. O `GATE-B04` vira uma checagem: só há intervenção se o agente se recusar a implementar uma story por dependência de outra unidade ainda não feita (seção 12.3). Registrar como D-006.
- Alternativa (texto antigo da Parte III): mandar uma `INTERVENÇÃO [redirecionamento|prd]` pedindo que o sprint siga a ordem do pacote.

### 2.5 Gatilhos `PROCESSO` encontrados no texto da v6.11.0 e ausentes da lista esperada (§4.5) — ✅ decidido (opção ⭐), registrado em `desvios.md`

A **definição** de gatilho é congelada: toda pausa em que a skill, pelo próprio texto, pede resposta, escolha, confirmação ou aprovação. Logo, estas pausas levam `PROCESSO:` mesmo fora da lista esperada:
- **`bmad-build`:**
  - pedido único de autorização para usar subagentes;
  - parada se a árvore git estiver suja (*"If the tree is dirty… HALT and ask"*);
  - escolha `[S] Split` / `[K] Keep`;
  - **CHECKPOINT 1** `[A] Approve` / `[E] Edit` da spec da story;
  - oferta final de push/PR.
- **`bmad-code-review`:** confirmação da story em `review` (`[Y]/[N]`); menus numerados de `decision-needed`, `patch` e "next steps".
- **`bmad-qa-generate-e2e-tests`:** "o que testar"; confirmação do framework.
- **`bmad-sprint-planning`:** pergunta de intenção, se a skill não inferir.
- **`bmad-product-brief`, `bmad-prd`, `bmad-ux`, `bmad-architecture`:** escolha **Coaching path** × **Fast path**.

⭐ Registrar a lista como D-007 (achado, sem mudar a definição). As respostas estão na seção 5.3.

### 2.6 Não bloqueantes (detalhe no Apêndice C)

- A coleta grava a fase das sessões de correção como `SETUP` (deveria ser `IMPL`), e o `bmad-prd` (validar) como `ESPEC` (deveria ser `VALID`: a tabela do script não distingue as duas intenções da mesma skill). Os brutos estão preservados, então dá para re-segmentar na Parte IV.
- O formato `M6_tasks` do B: as stories em `epics.md` **não** têm checkboxes; as specs que o `bmad-build` cria em `implementation-artifacts` **têm** (`- [ ] \`FILE\` -- ACTION`). Você não faz nada, só preserva os arquivos.

---

## 3. Transição A → B e preparação do Ciclo B (22/10/2026)

Tudo 🧑 [MANUAL], no terminal. Nenhuma sessão.

### 3.1 `X-001` Instrumento intacto

```bash
cd "$AVAL" && git checkout main && git pull origin main
git diff --stat protocolo-v1.0 -- docs/protocolo.md docs/Metricas_e_Skills_Ciclos.md entrada prompts holdout harness scripts skills
```
**Critério:** só aparecem diferenças com entrada correspondente em `docs/desvios.md` (ex.: `prompts/P-SETUP.md` se o D-001 foi aplicado; `scripts/faixa-plan` depois do D-004).

### 3.2 `X-002` Ambiente igual

```bash
sw_vers -productVersion; xcodebuild -version; fvm flutter --version; claude --version; code --version | head -1; uv --version; node -v
shasum -a 256 ~/cerne/cfg-ciclo-b/settings.json      # 0112786e12fbe0917221c8d09f17f9f4b9c022d5ef811b9123b9fb9b0a62f393 (D-013; antes: 3904700b…5922, D-012; db5d321b…91e2, D-009)
diff "$AVAL/skills/coletar-sessao/SKILL.md" ~/cerne/cfg-ciclo-b/skills/coletar-sessao/SKILL.md && echo OK-b
ls ~/cerne/cfg-ciclo-b/skills ~/cerne/cfg-ciclo-b/plugins      # só coletar-sessao; sem pasta synced (D-009, D-012)
```
**Critério:** macOS 27.0.1, build 26A434 (D-010); Xcode 27.0 (27A266a); Flutter 3.47.5 / Dart 3.13.4; Claude Code 2.1.282; VS Code 1.139.1; uv 0.12.19; Node v26.10.0; hash idêntico; `OK-b`. Confirmar também que o modelo `claude-sonnet-5` continua disponível (página de modelos da Anthropic). **Se algo mudou ou o modelo saiu do ar: parar e decidir com a orientadora.**

### 3.3 🔴 `GATE-X01` Backend `ciclo-b`

1. Painel do Supabase → `ciclo-b` → Authentication → Providers → Email → **Confirm email: OFF**.
2. Schema idêntico ao do congelamento:
   ```bash
   set -a; source "$AVAL/segredos/db.ciclo-b.env"; set +a
   deno run -A "$CERNE_BACKEND_DIR/scripts/schema-hash.ts"      # f33a12b44912ae129a4702bcf7c8fffdcd93d7defad15df2323171cf779868e2
   ```
3. `REPLAY_MODE=replay` para o desenvolvimento:
   ```bash
   cd "$AVAL" && scripts/replay-mode b replay        # digite: sim
   ```
4. Chamada autenticada responde 200 (só leitura). Usa a conta `cenario-cheio@cerne.test`, cuja senha está em `segredos/`, e não faz nenhuma escrita:
   ```bash
   set -a; source "$AVAL/segredos/.env.ciclo-b"; set +a
   TOKEN=$(curl -s -X POST "$FUNCTIONS_BASE_URL/auth-login" -H "Authorization: Bearer $SUPABASE_ANON_KEY" -H "apikey: $SUPABASE_ANON_KEY" -H "Content-Type: application/json" -d '{"email":"cenario-cheio@cerne.test","password":"<senha do seed>"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["data"]["session"]["accessToken"])')
   curl -s -o /dev/null -w "%{http_code}\n" "$FUNCTIONS_BASE_URL/entries-list" -H "Authorization: Bearer $TOKEN" -H "apikey: $SUPABASE_ANON_KEY"     # 200
   ```
5. **Não** rodar `reset-ambiente b` (o `ciclo-b` está no estado do seed desde 29/09 e nunca foi usado).

### 3.4 🔴 `GATE-X02` Efeito de aprendizado

Escrever `$AVAL/dados/cicloB/aprendizado-previo.md` com o que você aprendeu no Ciclo A e que pode influenciar o B: comportamento do backend, armadilhas do **dispositivo físico** (assinatura, permissões, Face ID), pacotes problemáticos e o tempo de build do `whisper_ggml`. Commit e push.

**A partir daqui, não abrir `cerne-ciclo-a`** (nem `git log`, nem VS Code) até o `cicloB/final`.

### 3.5 Preparações específicas do B

- [ ] Variáveis e `abrir-ciclo` da preparação única do A (`docs/plano-ciclo-A-speckit.md`, seções 3.2 e 3.3) continuam valendo: `echo "$CERNE_CICLO_B_DIR"` mostra o caminho do clone; `git -C "$CERNE_CICLO_B_DIR" status` funciona; `grep -c cfg-ciclo-b ~/cerne/bin/abrir-ciclo` ≥ 1.
- [x] D-004 a D-007 já registrados e `scripts/faixa-plan` já no repositório (commit `6c9686d`). Conferir: `"$AVAL/scripts/faixa-plan"` → `Timebox do planejamento (B2–B4): abaixo de 50%.`
- [ ] `fvm flutter devices | grep "$IPHONE"` lista o iPhone; proxy do Wi-Fi desligado; nenhum perfil do mitmproxy (`C-024`).
- [ ] Coletor OTel rodando (`~/cerne/otelcol/otelcol-contrib --config ~/cerne/otelcol/config.yaml`).
- [ ] Assinatura do Claude: anotar o plano e os limites vigentes (P13).
- [ ] `git -C "$CERNE_CICLO_B_DIR" log --oneline` → sem commits.

---

## 4. Anatomia de uma sessão medida

Idêntica à do Ciclo A. Vale para **toda** sessão.

1. 🧑 Coletor OTel rodando. VS Code **fechado** (Cmd+Q). Terminal: `abrir-ciclo b`.
2. 🧑 Painel do Claude Code → **conversa nova**. Fechar todos os editores (Cmd+K W) e **desligar o anexo de contexto** (olho), antes de **cada** mensagem.
3. 🧑 **Primeira mensagem:** a skill da etapa, como comando de barra (`/bmad-<skill>`), com o argumento indicado (seções 8–13). **Uma skill por sessão** (P4). ⚠️ **Forma (D-014):** **digite** `/bmad-<skill> ` à mão (com o espaço) e **depois cole** só o argumento (`cat prompts/P-….md | pbcopy`, Cmd+V). Nunca cole a mensagem inteira com o comando dentro: a extensão a envolve em `<pasted_content>`, o comando não é expandido e o agente chama a skill por conta própria (visto no `SETUP` do Ciclo A). **Painel de perguntas (D-015):** as perguntas das skills do BMAD que vierem no painel de opções também são respondidas por *Other*, digitando `PROCESSO: …` à mão; nunca por clique numa opção.
4. 🤖 O agente executa a skill. Pedidos de permissão: 🧑 **Yes** só desta vez. Negar → `INTERVENÇÃO [permissão negada]: …`.
5. 🧑 Pausas: seção 5.
6. 🚫 Proibido: `/clear`, `/compact`, `/model`, `/effort`, `ultrathink`, Option+T, editar arquivos, chamar outra skill do BMAD na mesma sessão (inclusive `bmad-help`), colar este documento, citar `cerne-avaliacao` ou o outro ciclo.
7. 📏 Última mensagem: `/coletar-sessao <ID>` → aprovar a permissão → conferir a saída (`Registrado…`, contagens, faixa) → fechar. Nunca retomar.
8. 🧑 Sessões `PLAN` de B2–B4: rodar `scripts/faixa-plan` e usar **essa** faixa (2.2).
9. 🧑 Notas da etapa ou unidade (sem números); backup diário dos dados (16.4).

**Modo `manual`** (limite de uso, travamento, esquecimento), sempre **antes** de abrir outra sessão no B:
```bash
cd "$CERNE_CICLO_B_DIR"
ls -t ~/cerne/cfg-ciclo-b/projects/*/*.jsonl | head -1          # nome do arquivo = session-id
CLAUDE_CONFIG_DIR=~/cerne/cfg-ciclo-b python3 "$AVAL/scripts/coletar_sessao.py" manual <ID> \
  --ciclo b --session-id <session-id> --motivo-fim <limite_uso|falha> \
  --versao-claude-code "$(claude --version)" --config-raciocinio high \
  --otel-output ~/cerne/otelcol/output.jsonl
```
A sessão seguinte repete a **mesma** skill (P4/P13).

---

## 5. Como escrever ao agente

### 5.1 As cinco categorias de mensagem

| Categoria | Quando | Forma | Conta como |
|---|---|---|---|
| **Comando** | 1ª mensagem | `/bmad-<skill> [argumento]` | Marca a fase |
| **Neutra** (P5b) | Confirmar pausa **espontânea**; colar erro pedido | Sem prefixo: `Yes, proceed.` | Nada |
| **PROCESSO** | Pausa **prevista** pela skill (5.3) | `PROCESSO: <inglês>` | M5b |
| **INTERVENÇÃO** | Qualquer outra | `INTERVENÇÃO [tipo\|campos]: <inglês>` | M5 |
| **Coleta** | Última | `/coletar-sessao <ID>` | Corte |

### 5.2 Formato da intervenção

O mesmo do Ciclo A: tipos exatos `correção` · `edição manual` · `redirecionamento` · `permissão negada` · `interrupção` · `esclarecimento não solicitado`. Severidade `S1`/`S2`/`S3` (só em `correção`), nível `N1`/`N2` (só em `edição manual`), causa `ctx`/`chk`/`inc`/`prd`/`amb`/`out` (obrigatória em `redirecionamento`, `correção` e `edição manual`). Correção: **sintoma, nunca solução**:
```
INTERVENÇÃO [correção|S<n>|<causa>]: Expected: … Actual: … Where: <tela "texto do protótipo"> → <ação>. Error: <mensagem exata>.
```

### 5.3 Pausas previstas das skills do BMAD v6.11.0 (respostas `PROCESSO`)

"Sugestão de RDR" = vira regra quando você grava no `rdr.md` na primeira ocorrência. Se o Ciclo A já criou uma linha equivalente no RDR, use **o mesmo texto** (regra 18).

| Skill | Pausa (texto real) | Resposta |
|---|---|---|
| `bmad-project-context` | "Ask what they bring" (regras, documentos externos); confirmações quando o repositório contradiz o usuário; proposta de trocar regra por hook/lint/CI | Regras já vão no `P-SETUP` da 1ª mensagem. Documentos externos: `PROCESSO: The product input is in docs/input/ (requirements.md, prototype/, backend/). There are no other documents.` (sugestão de RDR). Hook/lint/CI: frase padrão |
| `bmad-brainstorming` | "the one allowed menu" (quatro formas de conduzir); perguntas e pedidos de ideias | Menu: `PROCESSO: Use your technical judgment, following the input package.` Ideias: **só** conteúdo do pacote, citando a seção. Quando pedir mais do que o pacote tem: `PROCESSO: The input package does not cover further ideas.` (regra 23), registrando no RDR |
| `bmad-forge-idea` | Confirmação de premissas; perguntas de interrogatório das personas | Só o pacote; fora dele: `PROCESSO: The input package does not cover that.` (sugestão de RDR) |
| `bmad-deep-recon` | Escolha do modo (rascunhar um prompt para ferramenta externa / processar relatório / pesquisar aqui) e do tipo de pesquisa | `PROCESSO: Use your technical judgment, following the input package.` ⚠️ Se a skill gerar um prompt para você rodar em outra ferramenta (ChatGPT etc.): **não** rode; encerre a sessão normalmente e anote nas notas. Não traga informação de fora |
| `bmad-prfaq` | Perguntas de descoberta por estágio; menus de continuar; elicitação avançada / party mode | Pacote; menus: ver 5.4 |
| `bmad-product-brief`, `bmad-prd`, `bmad-ux`, `bmad-architecture` | **Coaching path** × **Fast path** | Frase padrão (`GATE-C11` regra 20) |
| idem | Perguntas de descoberta; aprovação de seções; menus `[C] Continue`; ofertas `[A]` elicitação avançada / `[P]` party mode | Pacote; menus: ver 5.4 |
| `bmad-prd` (1ª sessão) | Pergunta de intenção, se a skill não inferir | `PROCESSO: Create.` |
| `bmad-prd` (2ª sessão) | Pergunta de intenção | `PROCESSO: Validate the existing PRD.` |
| `bmad-ux` | De onde partir (fonte de UX) | `PROCESSO: The UX source is the frozen prototype in docs/input/prototype/ (cerne-prototype.html and prototype-extract.md). Do not change the prototype.` (sugestão de RDR; fonte: `GATE-C10`) |
| `bmad-create-epics-and-stories` | Menus a cada etapa (*"ALWAYS halt at menus"*): aprovar lista de épicos, stories, validação final | `PROCESSO: C` para continuar; ofertas `[A]`/`[P]`: ver 5.4 |
| `bmad-sprint-planning` | Intenção (se não inferir); gate **PASS / CONCERNS / FAIL** | Intenção: `PROCESSO: Run sprint planning.` CONCERNS: `PROCESSO: Proceed.` (regra 21). FAIL: **não** responda para seguir; colete e rode **em sessão nova** a skill que o achado indica (`PLAN`), depois rode o `bmad-sprint-planning` de novo |
| `bmad-build` | (1) Autorização para usar subagentes; (2) árvore git suja; (3) perguntas de intenção numeradas; (4) `[S] Split` / `[K] Keep`; (5) **CHECKPOINT 1** `[A] Approve` / `[E] Edit`; (6) ambiguidade na matriz de casos; (7) escalada se o laço de revisão passar de 5; (8) oferta final de push/PR | (1) `PROCESSO: Yes, you may use subagents for this whole run.` (2) `PROCESSO: Proceed. The uncommitted changes come from earlier workflow steps of this project.` (3) Pacote; fora dele, frase padrão. (4) Frase padrão. (5) `PROCESSO: A` (6–7) Pacote ou frase padrão. (8) **Não responder**: o trabalho já terminou e a próxima mensagem é a coleta. Todas são sugestões de RDR |
| `bmad-code-review` | `[Y] Yes / [N]` para a story em `review`; menus numerados de `decision-needed`; `patch` (1 Apply / 2 Leave / 3 Walk); "next steps" (1 next story / 2 re-run / 3 Done) | `[Y]`: `PROCESSO: Y`. `decision-needed`: frase padrão (se insistir em número, o número da opção que o próprio agente recomendou). `patch`: `PROCESSO: 1`. Next steps: `PROCESSO: 3`. Sugestões de RDR |
| `bmad-qa-generate-e2e-tests` | "Ask user what to test"; confirmação do framework | `PROCESSO: The features implemented in story <story_key>.` Framework: frase padrão |
| `bmad-retrospective` | Confirmar o épico detectado; aceitar retro de épico não terminado; veredito; discussão opcional | `PROCESSO: Yes.` para o épico detectado. Épico não terminado: não deveria acontecer (você só roda com o épico concluído); se ocorrer, `PROCESSO: No.` e anote |
| `bmad-correct-course` | Aprovação da proposta de mudança | Só em mudança grande (13.6). Aprovação: `PROCESSO: Approve.` |

### 5.4 Elicitação avançada e party mode (`GATE-C10`, regra 22)

- **Regra congelada:** aceitar quando oferecidos; o método e as melhorias aceitas ficam à sua escolha, e cada escolha vai para o RDR.
- ⭐ **Interpretação operacional** (para não virar laço infinito; registrar com o D-007):
  1. Em cada menu que oferece `[A]`/`[P]`, escolha **um** dos dois, uma vez (`PROCESSO: A` ou `PROCESSO: P`).
  2. Dentro da elicitação, aceite ou descarte as melhorias propostas com `PROCESSO:`, sempre com base no pacote.
  3. Quando o mesmo menu voltar, `PROCESSO: C`.
  4. RDR: uma linha por menu (skill, seção, método escolhido, melhorias aceitas e descartadas).
- Lembre que isso consome a timebox de 32 h: acompanhe pelo `faixa-plan`.

### 5.5 RDR (regras 16–23)

1. `PROCESSO:` e inglês.
2. Só o pacote, citando a seção.
3. Fora do pacote: procurar no `rdr.md` (aberto **fora** do VS Code do ciclo) uma pergunta equivalente e usar **o mesmo texto**. Várias perguntas do B já foram respondidas no A.
4. Se não houver: decidir, responder com uma frase curta e registrar logo depois da sessão.
5. Preferência: `PROCESSO: Use your technical judgment, following the input package.`

### 5.6 Perguntas espontâneas (D-003)

- Admite confirmação → neutra `Yes, proceed.`
- Pede escolha → `INTERVENÇÃO [esclarecimento não solicitado]: Use your technical judgment, following the input package.`
- Pede informação → resposta pelo pacote/RDR com o mesmo prefixo, e acrescentar ao RDR.

### 5.7 Escopo e nunca fazer

Igual ao A:
- tela de extensão → `INTERVENÇÃO [redirecionamento|prd]` citando a §2;
- nunca editar arquivo, rodar métrica (`--coverage`), abrir CSVs de dados ou olhar painel de uso;
- não ler artefatos do BMAD no VS Code do ciclo. Para descobrir as chaves das stories, use o terminal (`grep`, seção 12).

---

## 6. Tempo, timebox e pausas

| Escopo | Teto (tempo ativo) | Como você acompanha | Ao atingir |
|---|---|---|---|
| B2–B4 (11 sessões `PLAN`) | **32 h** somadas | `scripts/faixa-plan` depois de cada coleta `PLAN` | Planejamento encerrado no estado em que está (`GATE-C10`): commit de fechamento + `plan-done` + registro nas notas. Se faltar `epics.md` ou `sprint-status.yaml`, **parar e decidir com a orientadora** (o B5 depende deles) |
| Retrospectivas (`PLAN`) | Fora das 32 h e sem teto próprio | — | — |
| F000 | 12 h | Faixa da coleta | `rf-incompleto b F000` |
| Cada RF | 8 h | Faixa da coleta | `rf-incompleto b RFxx` |

- **Tempo ativo:** esperas por você contam até 30 min cada (P5c).
- **Faixas:** `abaixo de 50%` · `50-80%` · `acima de 80%` · `atingido`.
- **Limite de uso da assinatura:** coleta `manual` (`limite_uso`), com a data e a hora nas notas.
- **Ritmo do calendário:** o B tem cerca de 15 dias de implementação contra 19 do A, compensados pelo planejamento antecipado. A timebox é por tempo ativo, não por calendário.

---

## 7. B0 — Instalação e baseline

**Data proposta:** 23/10/2026.

### 7.1 `B-001` ⚙️📏 Baseline

```bash
cd "$AVAL" && scripts/iniciar-ciclo b
```
**Critério:** `Hashes conferidos: 15 arquivos, todos idênticos.` e tag `cicloB/baseline`. Depois:
```bash
git -C "$CERNE_CICLO_B_DIR" ls-files | grep -c "^docs/input/"          # 15
grep -c "service_role" "$CERNE_CICLO_B_DIR/.env"                        # 0
```

### 7.2 🔴 `GATE-B01` ⚙️📏 Instalar o BMAD (por flags, **não** interativo)

```bash
cd "$AVAL" && scripts/instalar-metodologia b
```
Executa `npx bmad-method@6.11.0 install --directory . --modules bmm --tools claude-code --communication-language English --document-output-language English --yes`, cronometra (M1), faz o commit `Install BMAD-METHOD v6.11.0 (bmm module, claude-code)`, cria a tag `cicloB/instalado` e grava em `sessoes.csv` (`tipo_sessao=instalacao`). Este ramo do script nunca foi rodado de ponta a ponta. As flags e a instalação em si foram validadas separadamente (Fase 4 e 01/10/2026).

**Critério:**
```bash
cd "$CERNE_CICLO_B_DIR"
ls .claude/skills | wc -l                         # 49
ls -d _bmad _bmad-output                          # existem
grep -E "communication_language|document_output_language|planning_artifacts|implementation_artifacts" _bmad/bmm/config.yaml
test -e CLAUDE.md && echo "ATENÇÃO: CLAUDE.md existe" || echo "sem CLAUDE.md (correto)"
git tag                                            # cicloB/baseline cicloB/instalado
```
Se não houver `CLAUDE.md`, o Claude Code lê o `AGENTS.md` (≥ v2.1.277), condição necessária ao B1 (§4.6).

### 7.3 🔴 `GATE-B02` Conferência de largada (sessão não medida)

`abrir-ciclo b` → conversa nova → só `/context`. Conferir:
- modelo `claude-sonnet-5`;
- skills: as 49 `bmad-*` (mais a skill pessoal da conta registrada no `C-011`, se aparecer);
- `coletar-sessao` ausente.

Screenshot → `$AVAL/dados/evidencias/gate-b02-ciclo-b.png`. **Deixar a sessão aberta por 2 minutos**, fechar **sem** coletar e conferir que `~/cerne/cfg-ciclo-b/skills` e `plugins` continuam **sem `synced`** (D-012: o `/context` sozinho não prova ausência, porque a sincronização da conta roda em segundo plano; o `settings.json` do B já tem `syncClaudeAiSkills` e `syncClaudeAiPlugins` = `false` e `disableClaudeAiConnectors` = `true`; a linha `MCP tools` do `/context` deve vir zerada, D-013).

---

## 8. B1 — Setup (`bmad-project-context`)

**Data proposta:** 23 a 24/10 · **ID:** `SETUP` · **Fase:** `ESPEC` · **M1** (parte "sessão")

### 8.1 🧪 `B-002` Sessão `/bmad-project-context` com o `P-SETUP` como regras do projeto

Gere a mensagem a partir do arquivo. É o **mesmo** `P-SETUP` usado na A1 (com ou sem a correção D-001).
```bash
{ cat "$AVAL/prompts/P-SETUP.md"; } | pbcopy   # só o argumento: digite `/bmad-project-context ` à mão (com o espaço) e cole depois (D-014); Cmd+V no Claude Code
```
O texto (com o D-001) é o mesmo transcrito na seção 8.1 de `docs/plano-ciclo-A-speckit.md`.

🤖 A skill ("a conversation that produces a repository's agent instructions: a small verified block inside `AGENTS.md`") varre o repositório, verifica as regras contra os fatos e grava o bloco em `AGENTS.md`. Pausas: 5.3. Para documentos externos, a resposta sugerida aponta só para `docs/input/`.

### 8.2 📏 Coleta

`/coletar-sessao SETUP`.

### 8.3 Conferência (fora da sessão, sem editar)

```bash
cd "$CERNE_CICLO_B_DIR" && git status --short && test -f AGENTS.md && echo "AGENTS.md criado"
```

### 8.4 📏 Commit de fechamento + `cicloB/setup-done`

```bash
cd "$CERNE_CICLO_B_DIR"
git add -A
git commit -m "SETUP: closing snapshot (project context)"
git tag cicloB/setup-done
python3 "$AVAL/scripts/registrar_tag.py" --ciclo b --tag cicloB/setup-done --tipo setup-done \
  --commit "$(git rev-parse HEAD)" --data "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
git push origin main --tags
```

### 8.5 🔴 Checagem única de parse (cega a números)

```bash
cut -d, -f4,5 "$AVAL/dados/cicloB/segmentos.csv" | sort -u
```
**Esperado:** `ESPEC,bmad-project-context`. Se só aparecer `SETUP,(nenhum)`, o nome da skill no transcript não bate com a tabela de fases. Não corrija: anote (re-segmentação na Parte IV).

---

## 9. B2 — Análise (`PLAN`)

**Datas propostas:** 24 a 25/10 · **ID:** `PLAN` · **Fase:** `ESPEC` · Uma sessão por skill, nesta ordem. Depois de cada coleta: `scripts/faixa-plan`.

| # | Primeira mensagem 🧪 | Argumento | Saída esperada 🤖 (em `_bmad-output/…`) |
|---|---|---|---|
| 9.1 | `/bmad-brainstorming <P-GLOBAL>` | `P-GLOBAL` (tabela de entrega) | Sessão de brainstorming documentada |
| 9.2 | `/bmad-forge-idea` | nenhum | Ideia "forjada" (`{output_folder}/forge`) |
| 9.3 | `/bmad-deep-recon` | nenhum | Pesquisa ou rascunho de prompt de pesquisa, conforme o modo |
| 9.4 | `/bmad-prfaq` | nenhum | `planning-artifacts/prfaq-<projeto>.md` + destilado |
| 9.5 | `/bmad-product-brief` | nenhum | Product brief |

### 9.1 🧪 Brainstorming com o `P-GLOBAL`

```bash
{ cat "$AVAL/prompts/P-GLOBAL.md"; } | pbcopy   # só o argumento: digite `/bmad-brainstorming ` à mão (com o espaço) e cole depois (D-014)
```
```text
/bmad-brainstorming # P-GLOBAL — Product vision

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

⚠️ **Ameaça registrada (métricas §12):** o brainstorming pede ideias. Você contribui **só** com o conteúdo do pacote. Ideias novas que o agente propuser e que você aceitar podem mudar o escopo do B. Na dúvida: `PROCESSO: The input package does not cover further ideas.`

### 9.2–9.5 Skills sem argumento

Primeira mensagem: só o comando (`/bmad-forge-idea`, `/bmad-deep-recon`, `/bmad-prfaq`, `/bmad-product-brief`). Quando a skill perguntar de onde partir, a resposta vem do pacote, com `PROCESSO:` e texto fixado no RDR (tabela de entrega, §5). Sugestão de RDR, igual para as quatro:
```
PROCESSO: Start from the product input in docs/input/ (requirements.md, prototype/, backend/) and the earlier outputs in _bmad-output/.
```

---

## 10. B3 — Planejamento (`PLAN`)

**Datas propostas:** 26 a 27/10 · **ID:** `PLAN`

| # | Primeira mensagem 🧪 | Argumento | Fase | Saída |
|---|---|---|---|---|
| 10.1 | `/bmad-prd <11 prompts>` | `P-F000` e `P-RF01`…`P-RF10`, **todos de uma vez, na ordem da P9** | `ESPEC` | PRD em `planning-artifacts/` |
| 10.2 | `/bmad-prd` | nenhum (intenção: validar) | `VALID`* | Relatório de validação do PRD |
| 10.3 | `/bmad-ux` | nenhum (fonte: protótipo) | `ESPEC` | `DESIGN.md` / `EXPERIENCE.md` |

\* A coleta grava `ESPEC` para as duas sessões do `bmad-prd` (Apêndice C). Não faça nada; anote nas notas qual sessão foi a de validação (data e hora).

### 10.1 🧪 PRD (criar) — mensagem exata

Os 11 prompts na ordem **F000 → RF03 → RF01 → RF02 → RF07 → RF06 → RF04 → RF10 → RF08 → RF05 → RF09**, separados por uma linha `---`. O `P-GLOBAL` **não** vai aqui (ele foi para o brainstorming). Gere com:
```bash
{ for p in F000 RF03 RF01 RF02 RF07 RF06 RF04 RF10 RF08 RF05 RF09; do cat "$AVAL/prompts/P-$p.md"; printf '\n---\n\n'; done; } | pbcopy   # só o argumento: digite `/bmad-prd ` à mão (com o espaço) e cole depois (D-014)
```
A mensagem fica assim (início e fim):
```text
/bmad-prd # P-F000 — Foundation

Build the foundation that every later unit uses, as described in `docs/input/requirements.md`, section 12:
…
---

# P-RF03 — Biometric authentication vault
…
---

# P-RF09 — Temporal summaries / dashboard
…
- Change the backend.

---
```
O texto integral de cada prompt está nas fichas da seção 14.

Pausas: intenção → `PROCESSO: Create.`; Coaching/Fast → frase padrão; descoberta → pacote; menus → 5.4.

**Diferença de método declarada (§5):** o BMAD recebe todos os `P-RFxx` aqui; o Spec Kit recebeu um por vez. O `requirements.md` completo está nos dois repositórios desde o baseline.

### 10.2 🧪 PRD (validar)

Primeira mensagem: `/bmad-prd`. Intenção → `PROCESSO: Validate the existing PRD.` Se a validação propuser mudanças e perguntar se aplica, é aprovação de seção → `PROCESSO:` com a decisão pelo pacote.

### 10.3 🧪 UX

Primeira mensagem: `/bmad-ux`. Fonte → `PROCESSO: The UX source is the frozen prototype in docs/input/prototype/ (cerne-prototype.html and prototype-extract.md). Do not change the prototype.` Se a skill propuser direções visuais diferentes do protótipo: o protótipo prevalece (`P-SETUP`: "The UI is faithful to the prototype").

---

## 11. B4 — Solução (`PLAN`) e tag `plan-done`

**Datas propostas:** 27 a 28/10 · **ID:** `PLAN`

| # | Primeira mensagem 🧪 | Argumento | Fase | Saída |
|---|---|---|---|---|
| 11.1 | `/bmad-architecture <P-TECH>` | `P-TECH` (primeira mensagem do `bmad-architecture`, uma vez) | `ESPEC` | Documento de arquitetura (fonte da M14 do B) |
| 11.2 | `/bmad-create-epics-and-stories` | nenhum | `ESPEC` | `planning-artifacts/epics.md` (épicos e stories `### Story N.M`, critérios Given/When/Then) |
| 11.3 | `/bmad-sprint-planning` | nenhum | `VALID` | Gate de prontidão PASS/CONCERNS/FAIL e `implementation-artifacts/sprint-status.yaml` |

### 11.1 🧪 Arquitetura com o `P-TECH`

```bash
{ cat "$AVAL/prompts/P-TECH.md"; } | pbcopy   # só o argumento: digite `/bmad-architecture ` à mão (com o espaço) e cole depois (D-014)
```
```text
/bmad-architecture # P-TECH — Technical instruction

Follow the technical constraints in `docs/input/requirements.md` and the architecture already in place in the project.
```
A skill oferece Coaching path (padrão) ou Fast path como passo de ativação: responda com a frase padrão. As decisões estruturais são "shown, not silently made", então espere aprovações de seção (`PROCESSO:`, pelo pacote).

### 11.2 🧪 Épicos e stories

`/bmad-create-epics-and-stories`. A skill para em menus a cada etapa (validação de pré-requisitos → desenho dos épicos → stories → validação final): `PROCESSO: C` para avançar, com as ofertas `[A]`/`[P]` pela regra 5.4. **Não corrija a decomposição**: ela é dado.

### 11.3 🧪 Sprint planning (portão de prontidão)

`/bmad-sprint-planning`. Intenção → `PROCESSO: Run sprint planning.`
- **PASS:** gera o `sprint-status.yaml` com as chaves das stories (formato `N-M-<slug>`, ex.: `1-1-project-scaffold`).
- **CONCERNS:** `PROCESSO: Proceed.`
- **FAIL:** colete (`/coletar-sessao PLAN`); abra uma sessão nova com a skill que o achado indica (ex.: `/bmad-create-epics-and-stories` ou `/bmad-prd`), `PLAN`; depois, uma sessão nova de `/bmad-sprint-planning`.

### 11.4 📏 Commit de fechamento + `cicloB/plan-done` (contorno manual)

```bash
cd "$CERNE_CICLO_B_DIR"
git status --short | head -40
git add -A
git commit -m "PLAN: closing snapshot (analysis, planning and solution artifacts)"
git tag cicloB/plan-done
python3 "$AVAL/scripts/registrar_tag.py" --ciclo b --tag cicloB/plan-done --tipo plan-done \
  --commit "$(git rev-parse HEAD)" --data "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
git push origin main --tags
```
A M4 do B é lida nesta tag e na `final`. Sem este commit, os artefatos do planejamento não estariam na tag.

---

## 12. Mapa story → unidade e ordem de implementação

### 12.1 🔴 `GATE-B03` Mapa story → unidade (📏 `dados/cicloB/mapa-stories.csv`)

Fora de sessão, no terminal. Liste as stories **sem abrir os arquivos no VS Code do ciclo**:
```bash
cd "$CERNE_CICLO_B_DIR"
grep -E "^### Story" _bmad-output/planning-artifacts/epics.md
grep -E "^\s+[0-9]+-[0-9]+-" _bmad-output/implementation-artifacts/sprint-status.yaml
```
Para atribuir uma story a uma unidade, leia só o título e o texto da story **no terminal** (ex.: `sed -n '/### Story 1.1/,/### Story 1.2/p' _bmad-output/planning-artifacts/epics.md`). Crie o CSV:
```bash
cat > "$AVAL/dados/cicloB/mapa-stories.csv" <<'EOF'
story_id,arquivo,unidade,nota
1-1-<slug>,_bmad-output/planning-artifacts/epics.md,F000,
1-2-<slug>,_bmad-output/planning-artifacts/epics.md,F000,
EOF
```
Regras:
- `story_id` = a chave exata do `sprint-status.yaml`.
- `arquivo` = `epics.md` (as specs com checkboxes só nascem no `bmad-build`).
- `unidade` ∈ `F000`, `RF01`…`RF10`.
- Story que cobre dois RFs → o primeiro na ordem P9, com nota.
- **Não corrija** a decomposição: ela é dado.

**Critério:** toda story mapeada.

**Unidade sem story:**
- Se o escopo dela estiver dentro de uma story de outra unidade (nota): a unidade não terá sessões próprias. Faça a P6 dela quando essa story estiver `done` e feche com commit de fechamento + `concluir-rf` (tag sem sessões, anotar).
- Se o escopo não estiver coberto em lugar nenhum: é achado (perda de escopo no planejamento). Mande **uma** mensagem `INTERVENÇÃO [redirecionamento|prd]: Requirement <RFxx> of docs/input/requirements.md (section 1) is not covered by any story.`, numa sessão `PLAN` nova com a skill que o BMAD indicar para isso (`/bmad-correct-course`). A intervenção vai como segunda mensagem, depois do comando.

### 12.2 Unidades na ordem P9

**F000 → RF03 → RF01 → RF02 → RF07 → RF06 → RF04 → RF10 → RF08 → RF05 → RF09** — igual ao A. Para cada unidade, as stories mapeadas são implementadas na ordem em que aparecem no `sprint-status.yaml` (D-006).

### 12.3 🔴 `GATE-B04` Ordem do sprint × ordem de entrega

Compare a ordem dos épicos e das stories no `sprint-status.yaml` com a P9 e anote nas notas.
- Com o D-006: divergência **não** gera intervenção, porque você escolhe as stories por unidade.
- Se o `bmad-build` se recusar a implementar uma story por depender de outra (de unidade posterior): **uma** `INTERVENÇÃO [redirecionamento|prd]: Follow the delivery order in docs/input/requirements.md, section 12; implement this story now.` Se a dependência for real e impossível de contornar, anote; a story vai para a unidade seguinte, com registro em `desvios.md`.

---

## 13. B5 — Bloco-padrão de implementação por unidade

**ID de coleta:** a unidade da story (pelo mapa). Uma sessão por skill, por story.

### 13.1 Por story da unidade (na ordem do `sprint-status.yaml`)

| # | Primeira mensagem 🧪 | Fase | Pausas previstas → resposta (5.3) | Resultado esperado 🤖 |
|---|---|---|---|---|
| a | `/bmad-build <story_key>` (ex.: `/bmad-build 1-1-project-scaffold`) | `IMPL` | Subagentes → `Yes…`; árvore suja → `Proceed…`; perguntas → pacote; `[S]/[K]` → frase padrão; CHECKPOINT 1 → `A`; push/PR → **sem resposta** | Spec da story em `implementation-artifacts/` (`baseline_commit`, tarefas `- [ ]`), código, testes, **commit local**, story em `review` no `sprint-status.yaml` |
| b | `/bmad-code-review` | `VALID` | `[Y]` → `Y`; `decision-needed` → frase padrão; `patch` → `1`; next steps → `3` | Achados na spec; patches aplicados; story `done` (ou `in-progress` se sobrar algo) |
| c | `/bmad-qa-generate-e2e-tests` | `VALID` | "o que testar" → `The features implemented in story <story_key>.`; framework → frase padrão | Testes automatizados (ameaça: testes que só o B tem; M8/M13 reportadas com e sem eles) |

- Se o code review deixar a story em `in-progress`: nova sessão `/bmad-build <story_key>` (retoma pelo status) → nova `/bmad-code-review`. Repetir até `done` ou até a timebox.
- `bmad-build` só com a chave da story: **nunca** reenvie o `P-RFxx` (tabela de entrega).
- O `bmad-build` commita sozinho no fim. O `code-review` e o QA deixam arquivos sem commit; por isso o próximo `bmad-build` vai parar com "árvore suja" (resposta 5.3, item 2). É esperado.

### 13.2 Retrospectiva por épico (`PLAN`, fora da timebox de B2–B4)

Quando **todas** as stories de um épico estiverem `done`:
```bash
grep -E "^\s+[0-9]+-[0-9]+-|epic-[0-9]+" "$CERNE_CICLO_B_DIR/_bmad-output/implementation-artifacts/sprint-status.yaml"
```
🧪 Sessão nova: `/bmad-retrospective` → confirmar o épico detectado (`PROCESSO: Yes.`) → veredito → `/coletar-sessao PLAN`. Não pedir "team discussion" nem party mode (não oferecidos por padrão). O fim de um épico não precisa coincidir com o fim de uma unidade: a retrospectiva roda quando o épico termina.

### 13.3 🔴 Verificação de "concluído" da unidade (P6) — 🧑 fora de sessão

Quando **todas** as stories da unidade estiverem `done`:

| | Critério | Como |
|---|---|---|
| (a) | O agente declarou pronto | O `code-review` da **última** story da unidade terminou com status `done` (`grep <story_key> …/sprint-status.yaml`) |
| (b) | `flutter analyze` sem erros | `cd "$CERNE_CICLO_B_DIR" && fvm flutter analyze` → nenhuma linha `error •` |
| (c) | Testes do agente passam | `fvm flutter test` (pasta padrão `test/`). Os e2e do QA em `integration_test/` não entram, por simetria com o A. **Nunca** `--coverage` |
| (d) | Critérios de aceite no iPhone | `fvm flutter run -d "$IPHONE"` + roteiro da ficha (seção 14) |

### 13.4 🧪 Correção (se a P6 falhar) — D-005

Sessão nova. A **primeira mensagem** é a intervenção, sem skill:
```
INTERVENÇÃO [correção|S<n>|<causa>]: Expected: … Actual: … Where: … Error: …
```
`/coletar-sessao <ID>` ao fim. Repetir a P6. A timebox soma todas as sessões da unidade.

**Diferenças de tela em relação ao protótipo (D-019, igual ao Ciclo A):** uma intervenção **por tela**, listando as diferenças da tela, com a severidade da mais grave (`S2` se falta ou difere texto, estado ou elemento do protótipo; `S1` se só o estilo difere). Descreva em termos qualitativos citando o estado do protótipo; sem valores numéricos de estilo nem código. Diferença vista em tela de unidade já fechada entra na correção da unidade atual.

### 13.5 📏 Fechamento da unidade

```bash
cd "$CERNE_CICLO_B_DIR"
git status --short | head -40
git add -A -- . ':(exclude)build/' ':(exclude).dart_tool/' ':(exclude)ios/Pods/' ':(exclude)ios/.symlinks/' ':(exclude)ios/Flutter/ephemeral/' ':(exclude).flutter-plugins' ':(exclude).flutter-plugins-dependencies'
git commit -m "<ID>: closing snapshot at unit completion" || true
cd "$AVAL" && scripts/concluir-rf b <ID>          # timebox atingido: scripts/rf-incompleto b <ID>
git -C "$CERNE_CICLO_B_DIR" push origin main --tags
```
Se o `git status` mostrar `.env`: **pare**, não commite (`git restore --staged .env`).

### 13.6 `bmad-correct-course` — só em mudança grande

Use só quando algo grande mudar durante a execução e o próprio BMAD indicar (ex.: o `bmad-build` ou o `code-review` concluírem que uma story ou um épico precisa ser refeito). Sessão nova, `/bmad-correct-course`, ID = unidade em andamento (interpretação: o custo é da unidade que provocou a mudança; anotar). Aprovação da proposta → `PROCESSO: Approve.`, pelo pacote.

### 13.7 Notas da unidade (sem números)

Em `plano-ciclos.md`, na unidade:
- stories e chaves; sessões por skill; laços build ↔ review;
- retrospectivas feitas no período;
- intervenções marcantes; linhas novas do RDR;
- cortes por limite de uso; avisos de coleta; critérios da P6 verificados em parte.

---

## 14. Fichas das unidades (B5.1–B5.11)

No B, os `P-RFxx` **já foram** entregues no PRD (10.1). Aqui eles servem só para você saber o escopo, nunca para colar numa sessão de build. Os roteiros da P6 são **idênticos** aos do Ciclo A, com uma diferença: a conta de desenvolvimento é outra, `dev-ciclob@cerne.test`, criada no `ciclo-b` durante a F000 (nunca as contas do seed, nunca a conta do A).

| Bloco | Unidade | Datas propostas | Timebox | Depende de (prompt) |
|---|---|---|---|---|
| B5.1 | F000 Fundação | 29 a 30/10 | 12 h | — |
| B5.2 | RF03 Cofre | 30 a 31/10 | 8 h | F000 |
| B5.3 | RF01 Captura | 31/10 a 02/11 | 8 h | F000, RF03 |
| B5.4 | RF02 STT/OCR | 02 a 03/11 | 8 h | RF01 |
| B5.5 | RF07 Timeline | 03 a 04/11 | 8 h | F000, RF01 |
| B5.6 | RF06 Busca | 04 a 05/11 | 8 h | RF07 |
| B5.7 | RF04 Chat | 05 a 07/11 | 8 h | F000, RF03 |
| B5.8 | RF10 Salvar do chat | 07 a 08/11 | 8 h | RF01, RF04 |
| B5.9 | RF08 Insights | 08 a 09/11 | 8 h | RF04 |
| B5.10 | RF05 Exportação | 09 a 11/11 | 8 h | RF07 |
| B5.11 | RF09 Dashboard | 11 a 12/11 | 8 h | F000, RF01 |

### 14.1 B5.1 — F000 Fundação

**Escopo (`P-F000`):** scaffold com a convenção de pastas; `lib/core/design_tokens.dart`; cliente HTTP com `Either<Failure, T>` e o contrato de erro; Entrar / Criar conta (Tela 0.1a) com `auth-signup`/`auth-login`/`auth-refresh`/`auth-session`; splash (Tela 0) e navegação base com placeholders; overlay "Sessão expirada".

**P6(d):**
1. Splash → Entrar / Criar conta (textos do protótipo).
2. **Criar a conta de desenvolvimento** `dev-ciclob@cerne.test` (senha guardada em `$AVAL/segredos/`, nunca no chat). Deve entrar direto.
3. Sair e entrar → Home/Chat.
4. Menu lateral → Meus Registros e Configurações como placeholders.
5. Login com senha errada → erro tratado, sem crash.

**Armadilhas:**
- Bundle id `com.example.*` impede instalar no iPhone → sintoma `INTERVENÇÃO [correção|S3|amb]` com a mensagem exata.
- "Confiar no desenvolvedor" no iPhone é ambiente, sem intervenção.

### 14.2 B5.2 — RF03 Cofre de autenticação biométrica

**Escopo (`P-RF03`):** barreira Face ID / Touch ID / PIN validada no aparelho; estados Tela 0.1, 0.1b (PIN inicial), 0.1c (PIN após falha); preferência por `PATCH /account/settings`; sessão renovada por `refresh`/`login`; `logout`.

**P6(d):**
- Falha do Face ID (cobrir a câmera TrueDepth) → oferece PIN, sem trancar fora.
- Segundo plano por **5 min e 15 s** (cronômetro) → pede autenticação ao voltar.
- Os três estados com os textos do protótipo.

**Armadilha:** app fecha ao chamar o Face ID → sintoma `S3` com o log, nunca a chave do `Info.plist`.

### 14.3 B5.3 — RF01 Captura multimodal

**Escopo (`P-RF01`):** modal de inserção ("Texto", "Áudio — Gravando", "Foto — Captura") pelo "+" do Home/Chat; `POST /entries` com `source` `manual`/`audio`/`photo`.

**P6(d):**
- Criar uma entrada de cada tipo (câmera e microfone **reais**). Conferir no SQL Editor do `ciclo-b`:
  `select source, left(content,50), created_at from entries where user_id = (select id from auth.users where email='dev-ciclob@cerne.test') order by created_at desc limit 5;` → mesma estrutura nas três.
- Cancelar uma gravação e uma foto no meio → nenhuma linha nova.

### 14.4 B5.4 — RF02 STT/OCR

**Escopo (`P-RF02`):** STT no aparelho com `whisper_ggml` (áudio nunca vai ao backend); OCR por `POST /media/ocr`; estados "Áudio — Processando / Transcrito / Erro" e "Foto — Processando OCR / Reconhecido / Erro"; material em `docs/input/backend/fixtures/`.

**P6(d):**
- Áudio falado (ou `audio_fixture_01.wav` tocado no Mac): Gravando → Processando → Transcrito.
- **Silêncio** → estado de erro de transcrição.
- OCR com `ocr_fixture_01.png` (Reconhecido) e `ocr_fixture_ilegivel.png` (Erro), passados por AirDrop.

**Armadilhas:**
- `whisper_ggml` não compila para simulador. Você **não** avisa o agente que existe um iPhone físico, exceto se ele perguntar (5.6).
- Asset de modelo > 100 MB impede o `push` (seção 17).

### 14.5 B5.5 — RF07 Timeline

**Escopo (`P-RF07`):** "Tela 4 — Meus Registros" e "Vazio"; selo de sincronização por entrada (`sync-badge.md`); overlay "Sessão expirada"; `GET /entries`, `GET /entries/:id`, `GET /auth/session`, `POST /auth/refresh`.

**P6(d):**
- Selo muda de estado numa entrada nova sem relogar.
- **Sessão expirada:**
  1. Logar no iPhone, rolar a timeline até o meio.
  2. No Mac, fazer o logout global da mesma conta:
     ```bash
     set -a; source "$AVAL/segredos/.env.ciclo-b"; set +a
     TOKEN=$(curl -s -X POST "$FUNCTIONS_BASE_URL/auth-login" -H "Authorization: Bearer $SUPABASE_ANON_KEY" -H "apikey: $SUPABASE_ANON_KEY" -H "Content-Type: application/json" -d '{"email":"dev-ciclob@cerne.test","password":"<sua senha>"}' | python3 -c 'import sys,json;print(json.load(sys.stdin)["data"]["session"]["accessToken"])')
     curl -s -X POST "$FUNCTIONS_BASE_URL/auth-logout" -H "Authorization: Bearer $TOKEN" -H "apikey: $SUPABASE_ANON_KEY"
     ```
  3. Depois de **60 min** do login no iPhone, reabrir Meus Registros, rolar até carregar mais ou voltar do modal de inserção → overlay "Sessão expirada", rolagem preservada, sem crash (o protótipo não tem "puxar para atualizar", D-023).
  4. Se não reproduzir: "verificado em parte", exatamente como no A. **No A o pesquisador decidiu não esperar os 60 min (D-023); aqui também não esperar**: registrar "verificado em parte — limitação do ambiente de desenvolvimento".
- "Nenhum BLoC importa outro BLoC" é estrutural: não verificar à mão.
- **Design da Tela 4 (decisão do A, 17/10):** o card mostrar o **texto completo** da entrada não é diferença contra o protótipo ("text excerpt" do resumo) e não vai para a sessão de correção; igual no B. Gesto de "puxar para atualizar" não existe no protótipo e não é cobrado (D-023).

### 14.6 B5.6 — RF06 Busca e filtros

**Escopo (`P-RF06`):** barra de busca, "Sheet de filtro", "Filtros ativos"; `GET /entries/search`, `GET /entries`; fixture `seeded-search-entries.md`.

**P6(d)** (antes, crie na conta `dev-ciclob` as entradas com os textos do fixture):
- Busca semântica sem a palavra exata.
- Digitação rápida sem "piscar" (debounce: verificação parcial; a medida exata é da hold-out).
- Modo Avião → lista do cache → reconectar sem itens duplicados.
- `source` + datas combinam com E.
- Limpar filtros volta à lista completa sem reiniciar a tela.

**Armadilha:** filtro por tag ou categoria é extensão → redirecionamento `prd`.

**Decisões do A (19/10), valem igual no B:** (1) a busca devolve todas as entradas por similaridade, sem corte, e a ordem vem do backend (conferir com a consulta direta a `entries-search` antes de culpar o app); (2) indicador de carregamento enquanto se digita, estado "Nenhum resultado para esta busca/filtro" no lugar do estado vazio do protótipo, rótulo de data repetido na lista por relevância e chips de categoria sem efeito: **só anotar**; (3) o que o HTML do protótipo tem e falta no app, o texto/estilo que difere do HTML e **o que só o resumo do protótipo tem (grupo "CATEGORIA", botão "Limpar" na sheet etc.) e o app oferece** são diferença de design (uma intervenção `correção|S2|prd` para a Tela 4); esta última parte foi decidida em 19/10, depois da P6 rodada 2 do A, e substitui o "mantido e anotado" da rodada 1 e alcança também o "Salvar só a foto" do estado *Foto — Erro* da Tela 2 (RF02), que no A entrou, pela D-019 (c), na correção da RF06; (4) offline: a lista do cache deve aparecer ao abrir a tela e o texto técnico da exceção não deve ser exibido.

### 14.7 B5.7 — RF04 Chat (RAG)

**Escopo (`P-RF04`):** "Tela 1 — Home/Chat", "Streaming", "Falha ao gerar resposta", "Offline"; "Tela 3 — Menu lateral" com sessões e nova conversa; `chat-sessions-*`, `chat-messages-*` (SSE), `retry`.

**P6(d):**
- Streaming → resposta completa.
- Modo Avião no meio do streaming → parcial visível com falha e retry.
- Conversar não cria entradas (SQL Editor).
- Menu lateral com sessões e "Novo Chat".

### 14.8 B5.8 — RF10 Salvar mensagem do chat

**Escopo (`P-RF10`):** "Tela 1 — Bookmark" e subestados; `POST /entries` com `source=chat` e `chatMessageId`.

**P6(d):**
- Botão só nas mensagens do usuário.
- Salvar duas vezes → uma entrada (SQL Editor).
- Sem rede → erro tratado e o botão permite tentar de novo.
- O chat não importa o repositório de entradas: estrutural, não verificar à mão.

### 14.9 B5.9 — RF08 Insights proativos

**Escopo (`P-RF08`):** "Tela 1 — Insight"; `POST /chat/sessions/:id/insight`.

**P6(d):**
- 5 mensagens → um insight.
- 1 mensagem + **2 min e 10 s** parado → um insight, sem repetir.
- Falha do insight (Modo Avião) não afeta o chat.
- Dispensar não muda a rolagem nem o estado.

### 14.10 B5.10 — RF05 Exportação

**Escopo (`P-RF05`):** sheet de exportação ("Pendente", "Processando", "Concluído", "Erro", "Período vazio"), aberta pelo ícone de download de Meus Registros; `export-screen-states.md`; `export-summary-create`, `export-status-get`, `export-download-get`.

**P6(d):**
- Período vazio → estado tratado.
- Período com entradas → Pendente → Processando → Concluído → baixar o PDF.
- Opção de dados brutos funcional.
- Falha da narrativa: verificação parcial (coberta pela hold-out).

**Armadilha:** job preso em "Pendente" → conferir `export_jobs` no SQL Editor antes de culpar o app (ambiente/backend → seção 17).

### 14.11 B5.11 — RF09 Dashboard

**Escopo (`P-RF09`):** "Tela 6 — Configurações" nas quatro variações do dashboard e "Confirmar exclusão de conta"; edição de nome, "Sair", "Apagar conta"; `dashboard-aggregate-get`, `dashboard-narrative-get`, `account-settings-update`, `account-delete`, `auth-logout`.

**P6(d):**
- 0 entradas (conta nova `dev-ciclob-vazia@cerne.test`), 1 entrada, > 30 entradas (conta principal; complete pelo modal).
- Recalcula ao criar uma entrada.
- Narrativa não quebra a UI.
- Sair.
- **Apagar conta só na conta descartável.**

**Armadilhas:**
- Seletor de persona é extensão.
- 404 "perfil do usuário autenticado não encontrado" na sua conta seria defeito de backend (D16).

---

## 15. Matriz de métricas — o que é coletado, quando e por quem

| Métrica | Onde nasce no Ciclo B | Quem/quando | Arquivo | O que você precisa garantir |
|---|---|---|---|---|
| **M1** Setup | `instalar-metodologia b` + sessão `SETUP` (B1) + calendário até `setup-done` | ⚙️; 📏 | `sessoes.csv`, `tags.csv` | `P-SETUP` entra no B1. Se entrasse na arquitetura, o custo cairia em `PLAN` (assimetria declarada na M1) |
| **M2** Tempo | Toda sessão; linha `PLAN` própria (zero no A); calendário por tags | 📏 | `sessoes.csv`, `segmentos.csv`, `tags.csv` | ID certo; `plan-done` e tags de unidade no dia em que terminam |
| **M3** Tokens/custo | Toda sessão; o BMAD usa subagentes (`bmad-build`, `code-review`) | 📏 + OTel | `sessoes.csv` (`sub_*`), `brutos/` (inclui `agent-*.jsonl`) | Nunca apagar `~/cerne/cfg-ciclo-b/projects/`; OTel rodando |
| **M4** Artefatos | `_bmad-output/planning-artifacts/` e `implementation-artifacts/`, lidos em `plan-done` e `final` | Parte IV | — | Commit de fechamento antes de `plan-done` e `final` |
| **M5 / M5b / D16** | Mensagens prefixadas | 🧑 → 📏 | `intervencoes.csv`, `revisoes_processo.csv` | Prefixos exatos; a correção começa com `INTERVENÇÃO` (D-005) |
| **M6** Aderência | `M6_tasks`: checkboxes das specs das stories da unidade (ou % `done` no `sprint-status.yaml`, regra alternativa); arquitetura + stories × diff; J | Parte IV | `rf.csv`, `julgamentos.jsonl` | `mapa-stories.csv` completo; tags por unidade |
| **M7, M8, M9 (hardcodes), M10 (assinaturas), M12, M13** | Código em cada tag de unidade | Parte IV | `rf.csv` | Tags corretas; nunca `--coverage`. M8/M13 também sem os testes do QA (ameaça) |
| **M8b, M9 (cor/tipografia/espaçamento), M10 (cenários), M11** | App da tag `final` | Parte IV | `rf.csv`, `estados_m9.csv`, `ciclo.csv` | Nenhum proxy durante o ciclo; hold-out nunca roda antes |
| **M14** Handoff | Documento de arquitetura do `bmad-architecture`, verificado na `final` | Parte IV | `ciclo.csv` | Nunca editar a arquitetura |
| **M15** Padrões | Feature do RF01 (tag `cicloB/rf01-done`) × demais | Parte IV | `ciclo.csv` | Tag `rf01-done` com o código do RF01 |
| `n_msgs_contexto_ide` | Toda sessão | 📏 | `sessoes.csv` | Editores fechados e olho desligado |
| `mapa-stories.csv` | `GATE-B03` | 🧑 | `dados/cicloB/mapa-stories.csv` | Toda story mapeada |

**Nunca abrir:** `sessoes.csv`, `segmentos.csv`, `intervencoes.csv`, `revisoes_processo.csv`, `output.jsonl` do OTel, painel de uso. Exceções: a checagem cega da 8.5 (só `fase`/`marcador`) e o `faixa-plan` (só a faixa).

---

## 16. Git, tags e backup

### 16.1 Tags do Ciclo B, em ordem

| Tag | Quando | Como |
|---|---|---|
| `cicloB/baseline` | B0 | `iniciar-ciclo b` |
| `cicloB/instalado` | B0 | `instalar-metodologia b` |
| `cicloB/setup-done` | Fim do B1 | Manual (8.4) |
| `cicloB/plan-done` | Fim do B4 (depois do sprint planning) | Manual (11.4) |
| `cicloB/f000-done` … `cicloB/rf09-done` / `-incompleto` | Fim de cada unidade | Commit de fechamento + `concluir-rf b` / `rf-incompleto b` |
| `cicloB/final` | Encerramento | Manual (18.2) |

Nenhuma tag é movida ou apagada.

### 16.2 Commits

- O `bmad-build` faz **um commit local por story** (*"If version control is available and the tree is dirty, create a local commit"*). Isso é da metodologia.
- O commit de fechamento (D-002) cobre o que ficou de fora: planejamento, review, QA.
- O BMAD não cria branches neste fluxo. Se o agente criar, o `concluir-rf` faz o merge.

### 16.3 Push

O `bmad-build` oferece push/PR no fim: **não** responda (5.3). O push é seu, depois de cada tag: `git -C "$CERNE_CICLO_B_DIR" push origin main --tags`.

### 16.4 Backup diário dos dados (sem abrir arquivos)

```bash
cd "$AVAL" && git add dados docs/rdr.md docs/plano-ciclos.md docs/desvios.md && git commit -m "Ciclo B: dados e notas de $(date +%d/%m)" && git push origin main
```

---

## 17. Exceções e recuperação

| Situação | O que fazer | Registro |
|---|---|---|
| Limite de uso no meio da sessão | Coleta `manual` (`limite_uso`) **antes** de outra sessão; depois, a mesma skill de novo | Notas (data e hora) |
| Travamento ou esquecimento da coleta | Coleta `manual` (`falha`) | Notas |
| ID errado na coleta | Não editar CSV; registrar em `desvios.md` | `desvios.md` |
| `uv run` falhou (*"On failure (including uv being unavailable), report… and HALT"*) | Ambiente: resolver fora (`uv --version`, `PATH`). Na sessão seguinte, a mesma skill. Se o agente reportou a falha na sessão, a próxima mensagem pode ser a confirmação neutra depois de você resolver | Notas |
| `bmad-build` com várias specs ativas pergunta qual retomar | `PROCESSO:` com a chave da story da unidade atual | M5b |
| `bmad-sprint-planning` FAIL | Seção 11.3 | — |
| Timebox de B2–B4 atingida (`faixa-plan`) | Encerrar o planejamento no estado atual; commit de fechamento + `plan-done`; anotar. Se faltar `epics.md` ou `sprint-status.yaml`, parar e decidir com a orientadora | Notas, `desvios.md` |
| Timebox da unidade atingida | Commit de fechamento + `rf-incompleto b <ID>`; seguir | `tags.csv` |
| Agente em laço | Esc → `INTERVENÇÃO [interrupção]` → se preciso, `INTERVENÇÃO [redirecionamento|<causa>]` com o sintoma | M5 |
| Tela de extensão ou feature fora do pacote vinda do brainstorming | `INTERVENÇÃO [redirecionamento|prd]` citando a §2 ou o `requirements.md` | M5 |
| App não instala no iPhone | Sintoma `INTERVENÇÃO [correção|S3|amb]` | M5 |
| Erro que parece do backend | Política D16 (igual ao A, seção 13 de `docs/plano-ciclo-A-speckit.md`). Se for **bloqueante descoberto no Ciclo B**: corrigir, terminar o ciclo e **declarar a métrica não comparável** | `desvios.md` |
| `push` recusado (> 100 MB) | Não reescrever histórico; backup local; anotar | Notas |
| `/clear` por engano | Coletar e abrir outra sessão com a mesma skill | `desvios.md` |
| Quis abrir `cerne-ciclo-a` para "lembrar como foi" | **Não.** Use só `aprendizado-previo.md` e as notas | — |

---

## 18. Encerramento do Ciclo B

**Data proposta:** 13/11/2026.

### 18.1 `B-009` Completude (sem números)

```bash
cd "$AVAL/dados/cicloB"
ls ~/cerne/cfg-ciclo-b/projects/-Users-wagnerduarte-Documents-Faculdade-2026-2-TCC-cerne-ciclo-b/*.jsonl | wc -l     # só a pasta do repositório do ciclo (D-012)
tail -n +2 sessoes.csv | grep -vc ",instalacao,"
ls brutos/*.jsonl | grep -vc '^brutos/agent-'
cut -d, -f2,3 tags.csv
tail -n +2 mapa-stories.csv | wc -l                       # = número de stories no sprint-status.yaml
grep -cE "^\s+[0-9]+-[0-9]+-" "$CERNE_CICLO_B_DIR/_bmad-output/implementation-artifacts/sprint-status.yaml"
```
**Critério:**
- toda sessão tem linha (o `GATE-B02` só roda `/context` e não gera transcript);
- as 11 unidades têm tag;
- `setup-done` e `plan-done` existem;
- o mapa cobre todas as stories;
- toda épica concluída tem retrospectiva.

### 18.2 📏 `cicloB/final`

```bash
cd "$CERNE_CICLO_B_DIR"
git add -A -- . ':(exclude)build/' ':(exclude).dart_tool/' ':(exclude)ios/Pods/' ':(exclude)ios/.symlinks/' ':(exclude)ios/Flutter/ephemeral/' ':(exclude).flutter-plugins' ':(exclude).flutter-plugins-dependencies'
git commit -m "Cycle B final snapshot" || true
git tag cicloB/final
python3 "$AVAL/scripts/registrar_tag.py" --ciclo b --tag cicloB/final --tipo final \
  --commit "$(git rev-parse HEAD)" --data "$(date -u +%Y-%m-%dT%H:%M:%S.000Z)"
git push origin main --tags
```

### 18.3 🔴 `GATE-B05` Nota de encerramento

Em `plano-ciclos.md`, sem números. A partir daqui, a Parte IV (14 a 20/11) pode começar, depois do `GATE-H02` (harness congelado).

---

## 19. Calendário

| Data | Etapa | Saída |
|---|---|---|
| 22/10 | Transição (seção 3) | `GATE-X01`, `GATE-X02`, D-004 a D-007 |
| 23/10 | B0 | `cicloB/baseline`, `cicloB/instalado`, `GATE-B02` |
| 23–24/10 | B1 SETUP | `cicloB/setup-done` |
| 24–25/10 | B2 Análise (5 sessões `PLAN`) | — |
| 26–27/10 | B3 Planejamento (3 sessões `PLAN`) | — |
| 27–28/10 | B4 Solução (3 sessões `PLAN`) | `cicloB/plan-done`, `GATE-B03`, `GATE-B04` |
| 29/10–12/11 | B5.1–B5.11 (unidades + retrospectivas) | `cicloB/<id>-done` |
| 13/11 | Encerramento | `cicloB/final`, `GATE-B05` |

**Trilha paralela:** corte da hold-out e da M8b em **06/11** (`GATE-H01`), no meio do B5, sem tocar o `cerne-ciclo-b`.

---

## Apêndice A — Comandos prontos

```bash
abrir-ciclo b

# B1
{ cat "$AVAL/prompts/P-SETUP.md"; } | pbcopy   # só o argumento: digite `/bmad-project-context ` à mão (com o espaço) e cole depois (D-014)
# B2
{ cat "$AVAL/prompts/P-GLOBAL.md"; } | pbcopy   # só o argumento: digite `/bmad-brainstorming ` à mão (com o espaço) e cole depois (D-014)
#   sem argumento: /bmad-forge-idea  /bmad-deep-recon  /bmad-prfaq  /bmad-product-brief
# B3
{ for p in F000 RF03 RF01 RF02 RF07 RF06 RF04 RF10 RF08 RF05 RF09; do cat "$AVAL/prompts/P-$p.md"; printf '\n---\n\n'; done; } | pbcopy   # só o argumento: digite `/bmad-prd ` à mão (com o espaço) e cole depois (D-014)
#   sem argumento: /bmad-prd (validar)  /bmad-ux
# B4
{ cat "$AVAL/prompts/P-TECH.md"; } | pbcopy   # só o argumento: digite `/bmad-architecture ` à mão (com o espaço) e cole depois (D-014)
#   sem argumento: /bmad-create-epics-and-stories  /bmad-sprint-planning
# B5 (por story)
/bmad-build <story_key>
/bmad-code-review
/bmad-qa-generate-e2e-tests
# por épico concluído
/bmad-retrospective

# Última mensagem de toda sessão
/coletar-sessao <SETUP|PLAN|F000|RF01..RF10>

# Faixa do planejamento (depois de cada coleta PLAN de B2–B4)
"$AVAL/scripts/faixa-plan"

# Chaves das stories (terminal, nunca no VS Code do ciclo)
grep -E "^\s+[0-9]+-[0-9]+-" "$CERNE_CICLO_B_DIR/_bmad-output/implementation-artifacts/sprint-status.yaml"

# P6
cd "$CERNE_CICLO_B_DIR" && fvm flutter analyze && fvm flutter test && fvm flutter run -d "$IPHONE"

# Fechamento de unidade
cd "$CERNE_CICLO_B_DIR" && git add -A -- . ':(exclude)build/' ':(exclude).dart_tool/' ':(exclude)ios/Pods/' ':(exclude)ios/.symlinks/' ':(exclude)ios/Flutter/ephemeral/' ':(exclude).flutter-plugins' ':(exclude).flutter-plugins-dependencies' && git commit -m "<ID>: closing snapshot at unit completion"
cd "$AVAL" && scripts/concluir-rf b <ID>
git -C "$CERNE_CICLO_B_DIR" push origin main --tags

# Coleta manual
cd "$CERNE_CICLO_B_DIR" && CLAUDE_CONFIG_DIR=~/cerne/cfg-ciclo-b python3 "$AVAL/scripts/coletar_sessao.py" manual <ID> --ciclo b --session-id <id> --motivo-fim <limite_uso|falha> --versao-claude-code "$(claude --version)" --config-raciocinio high --otel-output ~/cerne/otelcol/output.jsonl
```

---

## Apêndice B — Correções em relação ao `plano-ciclos.md` (Parte III)

| # | Parte III dizia | Correto (fonte) |
|---|---|---|
| 1 | `GATE-B01`: "respostas ao instalador interativo registradas no `GATE-C10`" | Instalação **por flags**, não interativa (`GATE-C08`; `instalar-metodologia b`) |
| 2 | B1: "**se** o `GATE-C10` decidiu pelo contexto de projeto" | Decidido: `bmad-project-context` com o `P-SETUP` (§4.3 item 1) |
| 3 | B2: só "Product brief (Analyst)" com `P-GLOBAL` | B2 Análise = 5 skills: `brainstorming` (com `P-GLOBAL`) → `forge-idea` → `deep-recon` → `prfaq` → `product-brief` (§4.3; tabela de entrega) |
| 4 | B-004 "PRD" como sessão única | `bmad-prd` **criar** (com os 11 prompts) → `bmad-prd` **validar** → `bmad-ux` (§4.3 item 3) |
| 5 | B-005: `P-SETUP` como primeira mensagem da arquitetura "se não entrou no B1" | `P-TECH` é a primeira mensagem do `bmad-architecture`; o `P-SETUP` já entrou no B1 (§5) |
| 6 | B-007 "Verificação de prontidão" como sessão separada | Não existe na v6.11: a prontidão é o gate do próprio `bmad-sprint-planning` (§4.3 item 4) |
| 7 | B3 "Sprint planning" **depois** da tag `plan-done` | `bmad-sprint-planning` é o último passo do B4, **antes** de `plan-done` (§4.3 item 4) |
| 8 | Nenhuma timebox no planejamento | **32 h** de tempo ativo para B2–B4 (R23), medidas por `faixa-plan` (D-004) |
| 9 | Bloco por story: `build` → `code-review` | `build` → `code-review` → **`qa-generate-e2e-tests`** (§4.3 item 6) |
| 10 | Sem retrospectiva | `bmad-retrospective` ao fim de **cada épico**, ID `PLAN`, fora da timebox (§4.3 item 6) |
| 11 | Correção "numa sessão nova com o workflow de implementação" | Sessão nova **aberta pela mensagem** `INTERVENÇÃO [correção|…]`, sem skill (P4, regra 13; D-005) |
| 12 | Unidades rotuladas "B4–B14" | B4 é a Solução no protocolo; as unidades viram B5.1–B5.11 |
| 13 | `GATE-X02`: "armadilhas do simulador" | Armadilhas do **dispositivo físico** (P11 revisado) |
| 14 | `GATE-B04`: intervenção se a ordem do sprint divergir | Você escolhe as stories por unidade; intervenção só se o agente recusar (D-006) |
| 15 | Tag `plan-done` sem procedimento | Manual (11.4), com commit de fechamento |
| 16 | `mapa-stories.csv` sem formato de `story_id` | Chave exata do `sprint-status.yaml` (`N-M-<slug>`) |

---

## Apêndice C — Pendências abertas

| Pendência | Efeito | Quando |
|---|---|---|
| D-004 (`faixa-plan`) | Sem ele, não há como saber o teto das 32 h | Transição (22/10) |
| D-005 a D-007 | Procedimentos do B | Transição |
| Fase do `bmad-prd` (validar) gravada como `ESPEC`; sessões de correção como `SETUP` | Só dados por fase; brutos preservados | Parte IV (re-segmentar) |
| `M6_tasks` do B: arquivo-fonte (specs das stories × status `done`) | Parte IV, `harness/regras.md` §5 | Antes da Parte IV, com a calibração |
| Cache de IA de desenvolvimento não é apagado pelo reset hospedado (detalhe em `docs/plano-ciclo-A-speckit.md`, Apêndice C) | Validade do `replay_strict` | Antes do `V-002` |
| `C-024`, `TEST_FAULT_KEY`, `OTEL_TOLERANCE`, `compact_boundary` | Parte IV / conferência | Antes da Parte IV |
| Corte da v7 do BMAD durante o B | Versão travada continua (v6.11.0) | — |

---

## Apêndice D — Textos propostos

### D.1 `docs/desvios.md` (linhas do B; as linhas D-001 a D-003 estão em `docs/plano-ciclo-A-speckit.md`)

| # | Data | Ciclo / unidade | O que mudou ou aconteceu | Motivo | Arquivos afetados | Efeito nas métricas | Declarado em |
|---|---|---|---|---|---|---|---|
| D-004 | 22/10/2026 | B, planejamento | Script auxiliar novo `scripts/faixa-plan`: faixa da timebox de 32 h das sessões `PLAN` anteriores a `cicloB/plan-done`, sem exibir valores | `coletar_sessao.py` (congelado) aplica 8 h a `PLAN` e soma as retrospectivas; o pesquisador, cego aos números, não teria como respeitar as 32 h (R23) | Novo arquivo; nenhum congelado alterado | Nenhum (só exibição); garante a regra de parada | Método |
| D-005 | 22/10/2026 | B | Sessões de correção abertas pela mensagem `INTERVENÇÃO [correção\|…]`, sem skill, como no A | P4/regra 13 do protocolo; uma mensagem que começa com `/bmad-build` esconderia o prefixo da coleta | Nenhum | Paridade de M5 entre ciclos | Método |
| D-006 | 22/10/2026 | B, implementação | O pesquisador escolhe as stories por unidade (mapa), na ordem do `sprint-status.yaml`; `GATE-B04` vira checagem | Simetria com o A, em que o pesquisador escolhe o `P-RFxx`; garante tags por unidade na ordem P9 | Nenhum | M2/M5 por unidade comparáveis | Método |
| D-007 | 22/10/2026 | B | Registro dos gatilhos `PROCESSO` da v6.11.0 ausentes da lista esperada da §4.5 (lista da seção 2.5) e da interpretação da regra 22 (uma escolha `[A]`/`[P]` por menu) | Definição congelada de gatilho aplicada ao texto real | Nenhum | M5b | Método |

### D.2 `docs/rdr.md` — sugestões a gravar na primeira ocorrência

| Skill | Pergunta (resumo) | Fonte | Resposta (texto exato) |
|---|---|---|---|
| `bmad-forge-idea`, `bmad-deep-recon`, `bmad-prfaq`, `bmad-product-brief` | De onde partir | Tabela de entrega (§5) | `PROCESSO: Start from the product input in docs/input/ (requirements.md, prototype/, backend/) and the earlier outputs in _bmad-output/.` |
| `bmad-project-context` | Documentos externos | Pacote | `PROCESSO: The product input is in docs/input/ (requirements.md, prototype/, backend/). There are no other documents.` |
| `bmad-brainstorming` | Pedido de mais ideias | Regra 23 | `PROCESSO: The input package does not cover further ideas.` |
| `bmad-prd` | Intenção (1ª e 2ª sessão) | `GATE-C10` | `PROCESSO: Create.` / `PROCESSO: Validate the existing PRD.` |
| `bmad-ux` | Fonte de UX | `GATE-C10` | `PROCESSO: The UX source is the frozen prototype in docs/input/prototype/ (cerne-prototype.html and prototype-extract.md). Do not change the prototype.` |
| `bmad-sprint-planning` | Intenção; CONCERNS | Regra 21 | `PROCESSO: Run sprint planning.` / `PROCESSO: Proceed.` |
| `bmad-build` | Subagentes; árvore suja; CHECKPOINT 1 | decisão | `PROCESSO: Yes, you may use subagents for this whole run.` / `PROCESSO: Proceed. The uncommitted changes come from earlier workflow steps of this project.` / `PROCESSO: A` |
| `bmad-code-review` | Story em review; patch; next steps | decisão | `PROCESSO: Y` / `PROCESSO: 1` / `PROCESSO: 3` |
| `bmad-qa-generate-e2e-tests` | O que testar | decisão | `PROCESSO: The features implemented in story <story_key>.` |
| `bmad-retrospective` | Confirmar épico | decisão | `PROCESSO: Yes.` |
| qualquer | Coaching × Fast path; preferência "A ou B?" | Regra 20 | `PROCESSO: Use your technical judgment, following the input package.` |

### D.3 `scripts/faixa-plan` (novo, não congelado — criar na transição, com o D-004)

```python
#!/usr/bin/env python3
"""scripts/faixa-plan — faixa da timebox do planejamento global do BMAD.

32 h de tempo ativo para B2–B4 (GATE-C10, R23). Soma `duracao_s` das sessões
`PLAN` do Ciclo B iniciadas antes da tag `cicloB/plan-done` (todas, se a tag
ainda não existe) — as retrospectivas, que vêm depois, ficam fora. Imprime só
a faixa, nunca o valor (P7 do documento de métricas). Desvio D-004.
"""
import csv
from pathlib import Path

DADOS = Path(__file__).resolve().parent.parent / "dados" / "cicloB"
LIMITE_S = 32 * 3600

plan_done = None
tags = DADOS / "tags.csv"
if tags.exists():
    with tags.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("tag") == "cicloB/plan-done":
                plan_done = row.get("data")

total = 0
sessoes = DADOS / "sessoes.csv"
if sessoes.exists():
    with sessoes.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("ciclo") != "b" or row.get("id_rf") != "PLAN":
                continue
            if plan_done and (row.get("inicio") or "") >= plan_done:
                continue
            total += int(row.get("duracao_s") or 0)

pct = total / LIMITE_S
if pct >= 1:
    faixa = "atingido"
elif pct > 0.8:
    faixa = "acima de 80%"
elif pct >= 0.5:
    faixa = "50-80%"
else:
    faixa = "abaixo de 50%"
print(f"Timebox do planejamento (B2–B4): {faixa}.")
```
Teste antes de usar: com `dados/cicloB/sessoes.csv` inexistente ou sem linhas `PLAN`, deve imprimir `abaixo de 50%`.
