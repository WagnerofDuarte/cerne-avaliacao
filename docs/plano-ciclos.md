# Big Plan — Checklist Mestre dos Ciclos Comparativos (App Cerne)

**Gerado a partir de:** `Requisitos_e_Fluxo_de_Telas_TCC.md` (RF01–RF10, RNF01–RNF09, §5–§11), `doc-prototipo.md`, `Metricas_e_Skills_Ciclos.md` (instrumento de medição, revisão v2 de 22/09/2026, publicada como v1.0 no `C-001`), `plano-backend.md` (backend congelado e pacote de handoff) e decisões D1–D18.

Este arquivo leva o app Cerne do zero absoluto — **nenhum repositório, nenhuma linha de código** — até os dois ciclos comparativos concluídos e avaliados: Ciclo A (GitHub Spec Kit) e Ciclo B (BMAD-METHOD). A Parte I é compartilhada pelos dois ciclos e termina num congelamento; a partir do **Marco de Bifurcação** cada ciclo segue sua trilha; a Parte IV avalia os dois com o mesmo instrumento.

**Princípio estrutural:** os ciclos se separam **na execução, não no planejamento**. Toda regra específica de cada metodologia — inclusive as do BMAD — é decidida e congelada na Parte I, antes do primeiro comando do Ciclo A. Decidir as regras do Ciclo B depois de ver o Ciclo A contaminaria o planejamento do B com o resultado do A.

**Precedência:** em divergência entre este arquivo e os documentos-fonte, os documentos-fonte prevalecem — reportar a divergência, não resolver silenciosamente. Depois do congelamento (seção "Checklist de congelamento do protocolo"), o protocolo congelado prevalece sobre qualquer documento, e toda mudança passa pelo "Registro de desvios de protocolo".

---

## Como usar este arquivo

**Onde este arquivo mora:** em `cerne-avaliacao/docs/`. **Nunca** num repositório de ciclo e nunca aberto dentro de uma sessão medida — ele descreve as métricas e o protocolo, e o agente medido não pode conhecê-los.

**Legenda:**
- `- [ ] C-0NN` / `H-0NN` / `V-0NN` — tarefa executável pelo Claude Code **no projeto `cerne-avaliacao`** (nunca num repositório de ciclo), com critério de conclusão verificável por comando.
- `- [ ] 🔴 [MANUAL] GATE-xNN` — **portão de ação ou decisão humana.** Só o Wagner executa ou decide. Quando a decisão tem opções, a recomendação vem marcada com ⭐.
- `- [ ] 🧪 [SESSÃO] A-0NN` / `B-0NN` — ação **dentro de uma sessão medida**, no repositório do ciclo: comando ou prompt digitado pelo Wagner, executado pelo agente medido.
- `- [ ] 📏 [COLETA]` — ato de coleta de dados (`/coletar-sessao`, tag git, cópia de transcript).

**Prefixos de ID:** `C` = compartilhado (Parte I) · `A` = Ciclo A · `X` = transição · `B` = Ciclo B · `H` = trilha paralela do harness · `V` = avaliação (Parte IV).

**Regras invioláveis (valem para todo este checklist):**
1. Executar as tarefas na ordem em que aparecem. Pré-requisitos estão implícitos na ordem.
2. Nenhuma tarefa conta como concluída sem o critério verificado. "Parece certo" não conta.
3. Este arquivo, o `Metricas_e_Skills_Ciclos.md` e tudo que está em `cerne-avaliacao` **nunca** entram num repositório de ciclo nem são abertos numa sessão medida.
4. Nada do protocolo congelado muda sem entrada no **Registro de desvios de protocolo**.
5. Não reabrir D1–D18 nem o backend congelado (`backend-v1.0-frozen`). Defeito de backend encontrado durante um ciclo segue a política D16 (`bugs_conhecidos.md`) — nunca uma correção no meio do ciclo.
6. `/coletar-sessao` é **sempre a última ação** de uma sessão medida. Uma sessão onde ela rodou **nunca** é retomada (`--continue`/`--resume` proibidos).
7. Toda intervenção começa com o prefixo `INTERVENÇÃO [tipo|campos]:`, no formato da §9, regra 2, do documento de métricas: severidade `Sn` para `correção`; nível `N1`/`N2` para `edição manual`; causa (`ctx`/`chk`/`inc`/`prd`/`amb`/`out`) obrigatória para `redirecionamento`, `correção` e `edição manual`. Toda resposta a uma pausa prevista pela metodologia (lista de gatilhos congelada) começa com `PROCESSO:`. Só as mensagens da lista de "mensagens neutras permitidas" (Fase 1) dispensam prefixo.
8. **Cegamento do pesquisador:** nenhuma métrica de produto ou diferencial (M6–M15) do Ciclo A é calculada ou consultada antes do fim do Ciclo B. Coletar dados brutos pode; olhar números não. As métricas de processo por sessão (M1–M5) são gravadas pela `/coletar-sessao` sem exibição de tokens, tempo ou custo; só a contagem de intervenções e respostas `PROCESSO:` reconhecidas é mostrada, para conferência do parse (ver `GATE-C03`, item 7).
9. A suíte hold-out **nunca** roda durante um ciclo nem antes da tag de conclusão do RF. Ela é instrumento de medição, não guia de desenvolvimento.
10. Nenhum output de medição (cobertura, relatórios, screenshots) é gravado num repositório de ciclo.
11. Modelo, versões, configuração do Claude Code e pacote de entrada são idênticos nos dois ciclos.
12. Nunca ajustar um script do harness, um teste ou uma rubrica para fazer uma métrica "dar certo". Divergência entre esperado e obtido é reportada, não corrigida.

**Ao encontrar um item 🔴 [MANUAL]:** parar, explicar o que fazer e por quê, aguardar confirmação explícita do Wagner, e só então verificar e seguir.

---

# PARTE I — COMPARTILHADO (antes da bifurcação)

## Fase 0 — Refinamento e fechamento do instrumento de medição
**Prazo proposto: 23 a 24/09/2026**

Objetivo: bater o martelo sobre **o que** é medido e **como** — incluindo as skills — e levar o `Metricas_e_Skills_Ciclos.md` da revisão v2 para a v1.0. Nenhuma fase seguinte começa antes disto, porque as decisões de protocolo (Fase 1) e o pacote de entrada (Fase 3) dependem de saber o que será medido.

- [x] 🔴 **[MANUAL] `GATE-C00`** — Criar o repositório `cerne-avaliacao` (GitHub, privado)
  - **Por que agora:** é a casa deste plano, do documento de métricas, das decisões e, mais tarde, dos scripts e dos dados. Todas as tarefas `C-` rodam nele. Os repositórios de ciclo só nascem na Fase 5.
  - **Como confirmo:** `git remote -v` aponta para ele.
  - **Registro (24/09/2026):** repositório privado `WagnerofDuarte/cerne-avaliacao` criado; `git remote -v` confere.

- [x] `C-000` Criar a estrutura de `cerne-avaliacao`: `docs/` (este plano, `Metricas_e_Skills_Ciclos.md`, `protocolo.md`, `desvios.md`), `entrada/` (pacote neutro, Fase 3), `skills/`, `scripts/`, `harness/`, `holdout/`, `calibracao/`, `dados/cicloA/brutos/`, `dados/cicloB/brutos/`, `dados/evidencias/`, `segredos/`; e um `.gitignore` com a linha `segredos/` (credenciais do `C-014`) — **Critério:** `tree -L 3` bate com a lista; `git check-ignore segredos/teste` responde; plano e documento de métricas versionados.
  - **Registro (24/09/2026):** estrutura criada e versionada (commit inicial com o instrumento das Fases 0–3 e 7); `git check-ignore -v segredos/teste` → `.gitignore:1:segredos/`; `git status` limpo; `docs/desvios.md` criado vazio.

- [x] 🔴 **[MANUAL] `GATE-C01`** — Revisão integral do `Metricas_e_Skills_Ciclos.md` (revisão v2)
  - **O quê:** reler o documento inteiro e marcar tudo que discorda, falta ou sobra, antes de decidir as pendências abaixo.
  - **Base da v1.0 (decidido em 22/09/2026):** a revisão v2 do arquivo do projeto. As menções a "v0" neste plano foram corrigidas para "v2".
  - **Como confirmo:** lista de observações registrada (ou "nenhuma") no próprio GATE. Roteiro de revisão em `docs/revisoes/gate-c01-roteiro-revisao.md`.
  - **Registro (22/09/2026):** revisão concluída pelo Wagner. Observações próprias: **nenhuma**. Divergências plano × v2 e lacunas resolvidas em 21 decisões (rodadas R1–R7), registradas no roteiro e aplicadas neste plano; os itens 🔁/✅ do roteiro são a lista de aplicação do `C-001`. Adiados com dono: `setup-done` do BMAD e menus interativos do BMAD (`GATE-C10`/`C11`); origem das decisões da M14 (`C-022`).

- [x] 🔴 **[MANUAL] `GATE-C02`** — Fechar as 12 pendências: as 11 da seção 13 do documento de métricas (v2) e as tags da suíte hold-out (numeração da v2; decidido em 22/09/2026)
  1. **Ferramenta de lint de arquitetura (M7).** Opções: (a) pacote Dart de lint de arquitetura, a verificar se existe e é mantido; (b) ⭐ script próprio do harness que lê os `import` de cada arquivo e aplica o mapa de camadas congelado — determinístico, sem dependência de ecossistema, e aplica também a regra "nenhum BLoC importa outro BLoC" do RF07 e a regra de fronteira do RF10. Registrar que `import-linter` é ferramenta Python, não Dart. **Decidido (22/09/2026, `GATE-C01` R6) — sem dupla contagem:** o mesmo script tem duas saídas. A regra do RNF06 (domínio não importa `package:flutter` nem `data/`) alimenta a **M7**; as regras do RF07 e do RF10 são critérios de aceite estruturais e contam **só na M11**. **Ferramenta — decidido (22/09/2026, `GATE-C02` R8):** opção (b), script próprio do harness em Python (`GATE-C03` item 3), que resolve imports relativos e `package:<app>/...` e aplica o mapa de camadas da convenção de pastas (P8), com configuração do harness e nunca o `analysis_options.yaml` do app.
  2. **Complexidade ciclomática (M12).** Opções: (a) DCM (pago); (b) fork open-source do `dart_code_metrics`; (c) ⭐ script próprio sobre a AST do `package:analyzer` — calcula a complexidade por método com regra documentada. Se (a) ou (b), fixar versão. **Decidido (22/09/2026, `GATE-C02` R8):** opção (c). A regra de contagem (McCabe, 1976: 1 + cada `if`, `for`, `while`, `do`, `case`, `catch`, `&&`, `||`, `?:`, `??` e `if` de coleção) é escrita na M12 da v1.0 (`C-001`) e validada contra valores calculados à mão no repositório de calibração (`H-001`). **Desvio da fonte a declarar:** a §8.2 dos requisitos prevê DCM ou fork do `dart_code_metrics`; a v1.0 e a monografia registram a troca e o motivo (determinismo, sem dependência de ferramenta paga ou descontinuada).
  3. **Suíte hold-out × checklist manual (M10, M11).** ⭐ suíte hold-out, com **data de corte**: se a implementação não estiver pronta e validada até o fim da trilha paralela, cai para o checklist manual roteirizado com gravação de tela, declarado na monografia. **Decidido (22/09/2026, `GATE-C02` R8):** ⭐ confirmado; data de corte 06/11 (`GATE-H01`).
  4. **Respostas a perguntas da metodologia (M5).** **Decidido (22/09/2026, `GATE-C01` R2):** não contam como intervenção; levam o prefixo `PROCESSO:` (v2, §9 regra 7) e formam a série **M5b** = `n_processo` em `sessoes.csv`, com detalhe em `revisoes_processo.csv`. É `PROCESSO` toda resposta a uma pausa prevista pela metodologia, segundo a lista de gatilhos congelada por framework; confirmação a uma pausa que o agente fez por conta própria é neutra. Falta só congelar a lista de gatilhos (dono: `C-004`). Isso é crítico para o BMAD, cujos workflows de planejamento são interativos: sem separar, o BMAD pareceria ter muito mais "intervenções" por pura mecânica do método.
  5. **Testes apagados na regressão (M13).** ⭐ contam, em coluna separada (`M13_apagados`). **Decidido (22/09/2026, `GATE-C02` R9):** ⭐ confirmado — coluna `M13_apagados`; a M13 é reportada com e sem os apagados.
  6. **Avaliador LLM.** Decidir: modelo e família (⭐ ID exato de um modelo Claude diferente do usado nos ciclos, com cegamento; registrar a autopreferência como ameaça); tamanho da amostra de validação (⭐ ≥20 itens por métrica julgada); limiar de concordância (⭐ kappa ≥0,61); e **o que acontece se o limiar não for atingido** (⭐ a métrica passa a ser reportada como exploratória e a amostra humana vira o dado principal).
     **Decidido em parte (22/09/2026, `GATE-C01` R5):** (i) **família:** modelo de **outra família**, com entrada de imagem (M9), via API de outro fornecedor (v2 §6; Taghavi & Bhavani §3.3; Baltes et al. §3.1.2) — o ⭐ original do plano (modelo Claude) foi substituído pela recomendação da fonte; (ii) **κ abaixo do limiar:** regra da v2 (§5.4, §6) com o rótulo do plano — a métrica é rotulada "exploratória", o resultado J é reportado com ressalva e a amostra humana ao lado; na D16, a classificação humana registrada no momento continua como dado primário; nenhuma troca de avaliador ou de rubrica depois de ver os dados. O ⭐ original ("a amostra humana vira o dado principal") foi descartado porque uma amostra de ~20 itens não cobre todas as unidades dos dois ciclos. **Decidido (22/09/2026, `GATE-C02` R9):** fornecedor **OpenAI** (família GPT), com entrada de imagem; amostra de **≥20 itens por métrica julgada** (M6, espaçamento da M9, M14, D16), **somados** aos itens sem maioria, que entram obrigatoriamente; limiar **κ ≥ 0,61**. O intervalo de confiança largo do κ com n≈20 é declarado como limitação. **Parâmetros (R9):** `reasoning.effort = medium`, fixado explicitamente em toda chamada; os demais parâmetros ficam no padrão, mas todos são registrados (Baltes et al., §4.2). **ID exato — decidido em 24/09/2026 (R29): `gpt-5.5-2026-04-23`** (era: adiado por decisão do Wagner na R9, para antes do `C-021` (Fase 7), sempre como snapshot datado, nunca alias, com entrada de imagem. Candidato levantado em 22/09/2026: `gpt-5.5-2026-04-23`. A disponibilidade é conferida na página de *deprecations* da OpenAI no `GATE-C23` e no `GATE-V01`.
  7. **RNF08 (M9).** Lista dos estados avaliados dentre os 32 e dispositivo do simulador — fechados junto com a decisão de telas de extensão (`GATE-C06`, item P10). Pode ficar com a marcação "fecha na Fase 1".
  8. **M8b — mutation score do domínio** (pendência #8 da v2). **Decidido (22/09/2026, `GATE-C01` R4):** adotada **só na tag `final`**, com condição: a ferramenta precisa funcionar no repositório de calibração (`H-001`, `H-002`) até a data de corte de 06/11 (`GATE-H01`). Se não funcionar, a M8b sai, e a validação circular da M8 é declarada como ameaça na §12. Versão da ferramenta travada e registrada no `protocolo.md`.
  9. **Tabela comando/persona → fase** (`ESPEC`/`IMPL`/`VALID`), para `segmentos.csv` (pendência #9 da v2). **Decidido (22/09/2026, `GATE-C01` R3):** a segmentação é mantida. A tabela é congelada no `C-004` a partir das versões travadas, e o `C-016` grava `segmentos.csv`. Esboço a confirmar: Spec Kit — `specify`, `clarify`, `plan`, `tasks` → `ESPEC`; `checklist`, `analyze`, `converge` → `VALID`; `implement` → `IMPL`. BMAD — brief, PRD, arquitetura, épicos, `sprint-planning` → `ESPEC`; `readiness` → `VALID`; `bmad-build` → `IMPL`; `bmad-code-review` → `VALID`. Mensagens sem marcador herdam a fase do marcador anterior (v2, M2).
  10. **Regex da M6 e formato das rotas do backend** (pendência #10 da v2). **Decidido (22/09/2026, `GATE-C01` R6):** as regex e o hash da Especificação Técnica usada como referência são escritos no `C-022` (Fase 7), a partir do formato real das rotas na `doc-backend-tec.md`.
  11. **Opcionais da v2:** estimativa prévia por RF (M2) e estabilidade de decisões (M14) (pendência #11 da v2). **Decidido (22/09/2026, `GATE-C01` R7):** nenhuma é adotada; as duas vão para "trabalhos futuros" na monografia. Sai da v1.0: `estimativas.csv` (§8), a regra 8 da §9 e a linha correspondente da §10.
  12. **Em quais tags a suíte hold-out roda.** A v2 prevê rodá-la em toda tag de RF. Cada execução exige build a partir da tag, reset do banco e modo de cache controlado, e são 11 tags × 2 ciclos. ⭐ Rodar só na tag `final` de cada ciclo, avaliando os critérios de **todos** os RFs no app final; a M13 (regressão) passa a usar só a suíte do próprio agente, tag a tag. Custo: perde-se a regressão medida pela suíte hold-out entre RFs. Registrar a mudança na v1.0.
     **Decidido (22/09/2026, `GATE-C01` R4):** só na tag `final`. Razões adicionais: o cache de IA é gravado uma única vez, na `final` do Ciclo A (`GATE-C19`, `V-002`), e execuções em tags intermediárias exigiriam novas gravações (contra a D5); e a §8.2 dos requisitos já define a regressão com a suíte do agente. Consequências na v1.0 (`C-001`): (i) o último ajuste da M8 é reescrito — a evidência funcional vem da M10 e da M11 (hold-out, tag `final`) e da M8b, se adotada; a M13 é medida pela suíte do agente; (ii) a M11 por RF passa a significar "critério do RF atendido no app final", não "no momento da entrega"; (iii) nova ameaça na §12: perda da regressão medida por suíte independente entre RFs.
  - **Como confirmo:** as 12 decisões registradas com data.
  - **Registro (22/09/2026):** itens 1–6 e 8–12 decididos (rodadas R1–R9 do `GATE-C01`/`C02`). Adiados com dono, por decisão do Wagner: item 7 → `GATE-C06` (P10, P11); ID exato do avaliador (item 6) → antes do `C-021`.

- [x] 🔴 **[MANUAL] `GATE-C03`** — Fechar o desenho da coleta automatizada (skills e scripts)
  1. **Fonte primária de tokens e tempo.** Opções: (a) OpenTelemetry; (b) ⭐ transcript JSONL do Claude Code como fonte primária — presente sempre, offline, com `usage` e timestamp por mensagem, o que torna o corte na mensagem de invocação trivial — e OpenTelemetry como conferência opcional. (Ajusta a M3 da v2, que colocava o OTel como primário.) **Decidido (22/09/2026, `GATE-C01` R4) — subagentes:** a fonte primária é o transcript principal **mais** os transcripts de subagentes e tarefas auxiliares da mesma sessão, onde quer que a versão travada do Claude Code os grave; tokens e tempo são somados, e a M3 registra também a parcela dos subagentes. O local e o formato desses arquivos são conferidos na versão travada, no `C-016` e no `GATE-C21`. **Decidido (22/09/2026, `GATE-C03` R10):** JSONL primário; OpenTelemetry **ligado nos dois ciclos** só como conferência. Se a soma de tokens do JSONL (principal + subagentes) divergir do total do OTel acima da tolerância fixada no `C-016`, a divergência é reportada, nunca corrigida à mão (regra 12). O OTel é a verificação independente da subcontagem de subagentes.
  2. **IDs aceitos pela `/coletar-sessao`.** A v2 prevê `SETUP`, `F000`, `RF01`–`RF10`. **Falta `PLAN`**, para as sessões de planejamento global do BMAD (PRD, arquitetura, épicos), que não são atribuíveis a um RF. ⭐ Adicionar `PLAN`, e reportar M2 por RF **mais** uma linha de planejamento global — no Spec Kit essa linha fica zerada por construção, e isso é resultado, não defeito. **Decidido (22/09/2026, `GATE-C03` R10):** ⭐ confirmado — `PLAN` aceito; M2 e M3 por RF mais uma linha de planejamento global (zerada no Spec Kit por construção), coerente com o pareamento decidido no `GATE-C01` R3.
  3. **Linguagem dos scripts.** ⭐ Python (um só runtime para parse de JSONL, CSV e chamadas ao avaliador). **Decidido (22/09/2026, `GATE-C03` R10):** Python para coleta, harness e chamadas ao avaliador; um CLI Dart pequeno (`harness/m12/`) só para a complexidade ciclomática sobre a AST do `package:analyzer` (`GATE-C02` item 2), chamado pelo Python. O teste de introspecção tipográfica (`H-003`) é Dart por natureza, porque roda dentro do app.
  4. **Onde ficam os transcripts brutos.** ⭐ a `/coletar-sessao` copia o JSONL da sessão **e os de seus subagentes** (item 1) para `cerne-avaliacao/dados/<ciclo>/brutos/` no mesmo ato. **Decidido (22/09/2026, `GATE-C01` R4-Q12):** inclui os transcripts de subagentes.
  5. **Fallback se `disable-model-invocation` falhar** na versão travada do Claude Code. ⭐ hook `SessionEnd` executando o mesmo script, sem skill. **Decidido (22/09/2026, `GATE-C03` R11):** hook `SessionEnd` executando o mesmo script. Como o hook não recebe argumento, o pesquisador roda `scripts/marcar-sessao <ID>` no terminal antes de fechar a sessão; o comando grava o ID num arquivo em `cerne-avaliacao/dados/<ciclo>/`, que o hook lê. Nesse modo, o corte é a última mensagem da sessão. O script do `C-016` já nasce com os dois modos (skill e hook), para o fallback não exigir código novo.
  6. **Repositório de calibração do harness.** ⭐ criar um app Flutter mínimo, sintético, com violações plantadas (um import proibido, um hardcode de cor, um método com complexidade 12, um teste que regride), usado para testar cada script do harness antes de aplicá-lo aos ciclos. É assim que o harness é validado sem olhar o código dos ciclos (regra 8). **Decidido (22/09/2026, `GATE-C03` R11):** ⭐ confirmado (`H-001`), com as violações plantadas e o gabarito já definidos no `GATE-C01` R4 (mutante da M8b) e no `GATE-C02` R8 (complexidade calculada à mão).
  7. **O que a `/coletar-sessao` exibe.** ⭐ Só a confirmação do registro ("sessão RF04 registrada: 1 linha em `sessoes.csv`, 3 em `intervencoes.csv`"), sem valores de tokens ou tempo. Ver os números a cada sessão faria o pesquisador reagir a eles — economizar prompts no fim do Ciclo A, ou no Ciclo B para "competir" com o A. Os valores ficam no CSV e só aparecem em `/avaliar-ciclo`. Se o Wagner preferir ver os números, registrar isso como ameaça. **Decidido (22/09/2026, `GATE-C03` R11), com correção:** o exemplo acima mostrava a contagem de intervenções, que a regra 8 proíbe exibir. A saída passa a ser: confirmação do registro; número de intervenções e de respostas `PROCESSO:` **reconhecidas** (o pesquisador as digitou, então a contagem não revela nada novo e serve para conferir o parse); um aviso por linha que começa com `INTERVEN` ou `PROCESSO` e não pôde ser lida; e a faixa da timebox. Tokens, tempo, custo e `div_otel` **nunca** são exibidos.
  - **Como confirmo:** as 7 decisões registradas.
  - **Registro (22/09/2026):** os 7 itens decididos (R10, R11; item 4 em R4-Q12). Nenhum adiado.

- [x] `C-001` Aplicar as decisões dos `GATE-C01`–`C03` ao `Metricas_e_Skills_Ciclos.md` e publicá-lo como **v1.0** (seções 4, 5, 8 e 13 atualizadas; seção 13 esvaziada ou só com o que foi explicitamente adiado, com dono — item 7 para o `GATE-C06` e ID do avaliador para o `C-021`; M1 com a instalação incluída e κ com a regra decididas no `GATE-C01` R5; §9 só com as regras que afetam os dados (prefixos, coleta, tags), com remissão à seção "Regras operacionais" do `protocolo.md` para as de conduta (`GATE-C01` R7); §14 com diferenças nulas do Wilcoxon tratadas pelo **método de Pratt** (`GATE-C01` R7); §14 com as regras de pareamento e de censura decididas no `GATE-C01` R3: **par principal por RF só nas fases `IMPL` + `VALID`**, com `ESPEC` comparada no nível do ciclo — soma de `ESPEC` dos RFs no A × `PLAN` + `ESPEC` dentro das stories no B —; **RF incompleto entra no par com o valor do teto marcado como censurado**, mais análise de sensibilidade sem os pares censurados) — **Critério:** diff revisado pelo Wagner; nenhuma pendência sem dono.
  - **Registro (22/09/2026):** v1.0 publicada em `docs/Metricas_e_Skills_Ciclos.md`; diff v2 → v1.0 (`Metricas_v2_para_v1.0.diff`) aprovado pelo Wagner. Decidido na mesma revisão: a leitura dimensional final (§5.6) é adotada como análise descritiva. §13 da v1.0 com dois adiamentos com dono (item 6 → `C-021`; item 7 → `GATE-C06`). **Ajuste posterior (22/09/2026, antes do congelamento):** M14, §5.6, §8 (`n_msgs_contexto_ide`) e §12 atualizados pelas decisões P2 e P4 do `GATE-C05`.

- [x] `C-002` Atualizar o esquema dos CSVs (seção 8 do documento de métricas) com as mudanças: ID `PLAN`, série M5b (`n_processo`, `revisoes_processo.csv`), coluna `tipo_sessao` em `sessoes.csv`, coluna `timebox_censurado` (booleano) em `rf.csv`, colunas de tokens de subagentes em `sessoes.csv` e `segmentos.csv`, coluna `div_otel` em `sessoes.csv`, e a indicação de que `M10_cenarios`, `M11` e `M8b_mutation` vêm só da execução na tag `final` (`M13_apagados` e `segmentos.csv` já existem na v2) — **Critério:** esquema de cada CSV listado coluna a coluna, com tipo.
  - **Registro (22/09/2026):** esquema escrito na §8 da v1.0 (`Metricas_e_Skills_Ciclos.md`), coluna a coluna com tipo: 11 arquivos CSV gravados na coleta e na avaliação (`sessoes`, `segmentos`, `intervencoes`, `revisoes_processo`, `avisos_coleta`, `tags`, `mapa-stories`, `rf`, `estados_m9`, `ciclo`, `validacao`) e o formato do `julgamentos.jsonl`. Arquivos novos em relação à v2: `avisos_coleta.csv` (`GATE-C03` item 7), `tags.csv` (`C-017`), `mapa-stories.csv` (`GATE-B03`), `estados_m9.csv` (score 0–3 por estado da M9, que a v2 previa sem arquivo).

### Encerramento da Fase 0 — notas para quem retomar
**Situação em 24/09/2026: fechada por completo.**
- **Concluído:** `GATE-C01` (revisão, 21 decisões nas rodadas R1–R7; roteiro em `docs/revisoes/gate-c01-roteiro-revisao.md`), `GATE-C02` (12 itens; R8–R9), `GATE-C03` (7 itens; R10–R11), `C-001` (v1.0 aprovada), `C-002` (esquema na §8 da v1.0), `GATE-C00` e `C-000` (repositório `WagnerofDuarte/cerne-avaliacao` criado e versionado em 24/09/2026).
- **Decisões que mudaram o plano:** base passou a ser a revisão v2 (não v0); `PROCESSO:` como série M5b; prefixo completo com causa; segmentação por fase e par principal em `IMPL`+`VALID`; censura pela timebox; hold-out só na `final`; M8b condicional; subagentes somados e OTel como conferência; M7/M12 por scripts próprios (Python + CLI Dart); avaliador OpenAI (`medium`, ≥20 + sem maioria, κ ≥ 0,61); hook `SessionEnd` com `marcar-sessao` como fallback; exibição da coleta restrita.
- **Adiados com dono:** ID exato do avaliador → antes do `C-021`; estados da M9 e dispositivo → `GATE-C06`; `setup-done` e menus interativos do BMAD → `GATE-C10`/`C11`; artefato de origem das decisões da M14 → `C-022`.
- **Carga nova para a Fase 6** (atenção ao prazo de 29/09): `/coletar-sessao` com dois modos, soma de subagentes, conferência OTel e avisos de prefixo; `marcar-sessao`.

---

## Fase 1 — Decisões de protocolo experimental
**Prazo proposto: 24 a 25/09/2026**

Cada decisão abaixo vale **igualmente para os dois ciclos**. As específicas de cada metodologia ficam na Fase 2.

- [x] 🔴 **[MANUAL] `GATE-C04`** — Modelo e configuração do agente
  - **P1 — Modelo.** ⭐ Claude Sonnet 5 com o **ID exato** (nunca um alias que possa mudar de versão no meio de um ciclo). Alternativa: Opus 5.5 — mais capaz, mais caro e mais lento; com a janela de ~3 semanas por ciclo, o Sonnet 5 é a escolha mais segura.
  - **P1b — Raciocínio.** Nível de raciocínio/esforço **fixado na configuração** (`settings.json`), nunca ativado por palavra-chave num prompt específico.
  - **P1c — Subagentes e tarefas de fundo.** Verificar na versão travada qual modelo o Claude Code usa para subagentes e tarefas auxiliares, e travá-lo no mesmo modelo por variável de ambiente, se a versão permitir. Se não permitir, registrar como ameaça.
  - **Decidido (22/09/2026, `GATE-C04` R12), com base na documentação atual da Anthropic e do Claude Code:**
    - **P1:** `claude-sonnet-5` no campo `model` do `settings.json`. Desde a geração 4.6, o ID sem data é snapshot fixo, não alias; o alias `sonnet` do Claude Code é proibido. Exige Claude Code ≥ v2.1.197.
    - **P1b:** esforço `high` (padrão do modelo), fixado por `CLAUDE_CODE_EFFORT_LEVEL=high` no bloco `env` do `settings.json`. A variável prevalece sobre o `effort` declarado em frontmatter de skills e subagentes, o que neutraliza diferenças introduzidas pelos arquivos de cada metodologia (registrar no `C-004` se alguma declara `effort`). O Sonnet 5 não tem *extended thinking* manual: o raciocínio é sempre adaptativo, controlado pelo esforço. `alwaysThinkingEnabled: true` fixado; proibidos a palavra `ultrathink` em qualquer prompt, a alternância manual de raciocínio (`Option+T`) e `/effort`/`/model` durante as sessões.
    - **P1c:** `CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5` com `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` ativado (sem o *force*, o `model` de uma definição de agente, como as do BMAD, prevaleceria). Tarefas auxiliares de fundo: `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001` (ID exato), iguais nos dois ciclos — decisão que diverge do plano original ("mesmo modelo") porque essas tarefas não produzem o código do app; o requisito de paridade é que sejam fixas e iguais. **Verificação obrigatória** no `GATE-C21`: o campo `model` dos transcripts de subagentes mostra `claude-sonnet-5` (há relatos de versões em que o roteamento de subagentes não seguiu a documentação). Se falhar, registrar como ameaça.
  - **Como confirmo:** ID do modelo, nível de raciocínio e configuração de subagentes registrados.

- [x] 🔴 **[MANUAL] `GATE-C05`** — Superfície, permissões e sessões
  - **P2 — Superfície.** ⭐ CLI no terminal. VS Code só como visualizador de código, sem a extensão do Claude Code. Xcode só como simulador.
    **Decidido (22/09/2026, `GATE-C05` R13–R14), contra a recomendação:** **extensão do Claude Code no VS Code**, nos dois ciclos; Xcode só como simulador. A extensão anexa a cada mensagem o arquivo aberto e a seleção, e não há configuração para desligar isso de forma permanente. **Mitigação obrigatória**, antes de **cada** mensagem de uma sessão medida: fechar todos os editores e desligar o anexo de contexto (ícone de olho). **Medição da ameaça:** o `C-016` conta, por sessão, as mensagens do pesquisador que chegaram com contexto injetado pela IDE (coluna `n_msgs_contexto_ide`), a partir dos marcadores que a extensão insere no transcript (formato confirmado no `C-016`). Registrada como ameaça na §12 do documento de métricas. Versões do VS Code e da extensão travadas, com atualização automática de extensões desligada (`C-011`).
  - **P3 — Permissões.** ⭐ `allowlist` idêntica nos dois ciclos em `.claude/settings.json` (ex.: `flutter`, `dart`, `git`, `xcrun simctl`, `fvm`), para reduzir pedidos de permissão. Aprovar um pedido de permissão não é intervenção; **negar** é (`INTERVENÇÃO [permissão negada]`). **Decidido (22/09/2026, `GATE-C05` R13):** ⭐ confirmado, com duas regras a mais: (i) a allowlist inclui o comando que executa o script da `/coletar-sessao`, para a coleta não parar num pedido de permissão; (ii) todo pedido é aprovado **só daquela vez** — a opção "sim, não pergunte de novo" é proibida, porque grava a permissão de forma persistente e muda o ambiente no meio do ciclo, de modo diferente em cada um.
  - **P4 — Gestão de sessão e contexto.** *(Texto original, substituído pela decisão abaixo.)* Regra: cada metodologia segue **a orientação oficial dela mesma**, e o pesquisador não impõe resets que ela não pede. ⭐ Spec Kit: uma sessão por RF, com todas as fases do RF na mesma sessão, sem `/clear` intermediário; uma sessão nova só se o contexto estourar, registrada. BMAD: sessão nova por workflow, como o próprio BMAD orienta. Compactação automática, quando ocorrer, é registrada no log da sessão. **Esta regra é o coração da métrica M14** — impor `/clear` ao Spec Kit simularia o reset do BMAD e apagaria o contraste que se quer medir.
    **Decidido (22/09/2026, `GATE-C05` R13–R14), contra a recomendação e com divergência registrada em relação à §8.3 dos requisitos:** **uma sessão nova por comando do Spec Kit** (`/speckit.constitution`, `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`), cada uma terminada com `/coletar-sessao`; no BMAD, uma sessão nova por workflow, como antes. Os dois ciclos passam a transmitir contexto entre fases **só pelos artefatos**. Justificativa: o Spec Kit guarda o estado em arquivos, e cada comando lê os artefatos do anterior; a documentação oficial não prescreve sessão contínua nem sessão por fase. Consequências: (i) a §8.3 dos requisitos define o contraste "agente único × reset de contexto entre fases", que deixa de variar entre os ciclos — a hipótese é reformulada para **fidelidade do handoff mediado por artefatos**, e a M14 passa a medir o quanto os artefatos de cada método carregam as decisões até o código (documento de métricas, §5.3 e §5.6); (ii) o custo de tokens do Spec Kit inclui a recarga de contexto a cada fase; (iii) cada sessão do Spec Kit corresponde a uma fase, o que torna a segmentação da M2/M3 direta. Compactação automática permitida e registrada; `/clear` proibido; uma fase que não termina numa sessão (limite de uso, falha) continua numa sessão nova com o mesmo comando, registrada. Divergência anotada no `protocolo.md`, seção "Divergências em relação aos documentos-fonte", para a monografia.
  - **P5 — Edição manual.** Proibida como rotina. Quando inevitável, conta como `INTERVENÇÃO [edição manual|N1 ou N2|causa]` e é seguida de mensagem prefixada descrevendo o que foi editado. Correções vão preferencialmente por prompt. **Decidido (22/09/2026, `GATE-C05` R15):** ⭐ confirmado, no formato `INTERVENÇÃO [edição manual|N1 ou N2|causa]`. Com a extensão do VS Code (P2), editar no editor é intervenção igual.
  - **P5b — Mensagens neutras permitidas** (não são intervenção): confirmações de avanço ("sim", "pode seguir", "prossiga") dadas a pausas que o agente fez por conta própria, fora da lista de gatilhos, e colar a saída de um erro que o agente pediu. Respostas a pausas previstas pela metodologia **não** são neutras: levam `PROCESSO:` (série M5b). Qualquer outra mensagem livre é intervenção. **Registrado (22/09/2026):** conforme decidido no `GATE-C01` R2 — respostas a pausas previstas pela metodologia levam `PROCESSO:` e não são neutras.
  - **P5c — Tempo ocioso (M2, timebox). Decidido (22/09/2026, `GATE-C05` R15):** o tempo em sessão é o **tempo ativo**: intervalos que terminam numa ação do agente contam inteiros; esperas pelo pesquisador contam até 30 min cada, e o excedente vai para `pausa_s`. O tempo bruto também é gravado. A timebox (P7) usa o tempo ativo.
  - **Como confirmo:** P2–P5b registradas.
  - **Registro (22/09/2026):** P2, P3, P4, P5, P5b e P5c decididas (R13–R15); P2 e P4 contra a recomendação, com consequências registradas.

- [x] 🔴 **[MANUAL] `GATE-C06`** — Escopo, stack e unidade de trabalho
  - **P6 — Definição de "RF concluído".** ⭐ Os quatro juntos: (a) o agente declara o RF pronto; (b) `flutter analyze` sem erros; (c) os testes que o próprio agente escreveu passam; (d) o Wagner percorre no simulador os critérios de aceite do RF, conforme a §1 dos requisitos (o mesmo texto que o agente recebeu). A suíte hold-out **não** entra nesta decisão (regra 9). **Decidido (22/09/2026, `GATE-C06` R16):** ⭐ confirmado. Com a P4 e o `GATE-C09`, "o agente declara pronto" = no Spec Kit, o `converge` reporta *Converged*; no BMAD, o code review aprova a última story da unidade.
  - **P7 — Timebox e regra de parada.** ⭐ Teto de **8 horas de tempo ativo em sessão por RF** (P5c) (12 horas para a F000). O teto é limite, não meta: no cronograma da P14, a média disponível é de cerca de 5 horas por bloco. Estourado o teto, o RF é encerrado como "não concluído", recebe a tag `rfNN-incompleto` e o ciclo segue. O tempo desse RF é um limite inferior: entra na análise marcado como censurado (`timebox_censurado`), conforme a §14 da v1.0. Um RF incompleto do qual outro depende é registrado como bloqueio, e o dependente é tentado mesmo assim. **Decidido (22/09/2026, `GATE-C06` R16):** ⭐ confirmado, em **tempo ativo** (P5c), somando todas as sessões da unidade, inclusive as de correção; a verificação, fora de sessão, não consome a timebox.
  - **P8 — Stack fixa × livre.**
    - **Fixo, para os dois ciclos:** Flutter e Dart na versão travada (via fvm); `flutter_bloc`; Clean Architecture em três camadas; `fpdart` (`Either<Failure, T>`); `mocktail`; `whisper_ggml` para STT on-device; `design_tokens.dart` como fonte única de tokens visuais; Voyage `voyage-4` (fixo pelo backend — a §10 dos requisitos ainda diz "`voyage-3` ou `voyage-4`" e precisa ser corrigida no pacote); iOS como plataforma.
    - ⭐ **Também fixo — convenção de pastas:** `lib/core/` + `lib/features/<feature>/{data,domain,presentation}/`. Sem isso, o harness precisaria de um mapa de camadas diferente por ciclo (M7, M8), e a M15 ficaria ambígua. É uma restrição pequena, e igual para os dois.
    - **Decidido (22/09/2026, `GATE-C06` R16):** ⭐ confirmado — fixos e livres como acima, com a convenção de pastas.
    - **Livre (cada metodologia escolhe):** roteamento, cliente HTTP, cache local, injeção de dependência, armazenamento seguro, pacotes de biometria e de gráfico. É nesse espaço que as metodologias vão divergir, e isso é dado.
  - **P9 — Ordem e granularidade.** ⭐ Uma unidade de trabalho por RF, precedida da fundação (F000), na ordem: **F000 → RF03 → RF01 → RF02 → RF07 → RF06 → RF04 → RF10 → RF08 → RF05 → RF09**. Duas posições são forçadas por dependência: RF10 depois de RF01 e RF04; RF08 depois de RF04. A ordem vai no pacote de entrada, que os dois ciclos recebem. **Decidido (22/09/2026, `GATE-C06` R17):** ⭐ confirmado.
    - **F000** cobre: scaffold do projeto, `design_tokens.dart`, cliente HTTP com `Either`, login e cadastro (Tela 0.1a), navegação base e tratamento de sessão expirada, ou seja, tudo que não pertence a um RF mas que todos usam.
  - **P10 — Telas de extensão** (Planos de Ação, seletor de persona, tags manuais). ⭐ Não são construídas: a §2 já as tira da implementação funcional nos dois ciclos, e construí-las só visualmente custaria tempo de ciclo sem medir nada comparativo. Entradas de menu para elas podem existir como placeholder. **Seus estados saem da M9.** Com isso, fecha-se a pendência 7 do `GATE-C02`: a lista de estados avaliados da M9 = os 32 menos os de extensão. **Decidido (22/09/2026, `GATE-C06` R17–R18):** ⭐ não construir, alinhado ao cabeçalho da §2 dos requisitos ("não recebem implementação funcional em nenhum dos dois ciclos"). Entradas de menu como placeholder são aceitas. Se o agente começar a construir uma extensão, **uma** mensagem `INTERVENÇÃO [redirecionamento|prd]` apontando a §2. Estados das telas de extensão fora da M9 (lista no `C-020`).
  - **P11 — Plataforma e dispositivo.** ⭐ iOS, só no simulador, num **único modelo de dispositivo** cujas dimensões lógicas batem com as dos frames do protótipo (conferir no `doc-prototipo.md`), usado no desenvolvimento e na avaliação (M9). Registrar os limites do simulador: sem câmera (a foto do RF01 é testada pela galeria), Face ID simulado pelo menu Features (RF03), microfone do Mac (RF01/RF02). **Decidido (22/09/2026, `GATE-C06` R17):** ⭐ confirmado. As dimensões dos frames não estão no `doc-prototipo.md`: o modelo do simulador é escolhido a partir do HTML do protótipo (`C-006`) e travado no `GATE-C15`. O `doc-prototipo.md` descreve o app como "Flutter, iOS e Android"; a restrição ao iOS é do experimento e está registrada como divergência no `protocolo.md`. Limites do simulador declarados: sem câmera (foto do RF01 pela galeria), Face ID pelo menu Features, microfone do Mac.
  - **P12 — Idioma.** ⭐ Prompts e documentos em português; identificadores de código em inglês; textos de UI em português, conforme o protótipo.
    **Decidido (22/09/2026, `GATE-C06` R19), contra a recomendação:** **inglês** para prompts, documentos do pacote de entrada, artefatos das metodologias, respostas `PROCESSO:` e RDR, e código; **textos de UI em português**, reproduzidos literalmente do protótipo (entre aspas, sem tradução). Consequências: (i) o pacote de entrada da Fase 3 é uma **tradução fiel** dos documentos-fonte, sem acrescentar nem omitir conteúdo — a revisão do `GATE-C13` passa a conferir também a fidelidade da tradução; (ii) os marcadores `INTERVENÇÃO` e `PROCESSO:` continuam em português, como tokens fixos para o script de coleta, com o corpo da mensagem em inglês; (iii) o instalador do BMAD é configurado em inglês nos dois idiomas que pergunta; (iv) citações de artefatos na monografia são traduzidas para o português, com o original em nota.
  - **Como confirmo:** P6–P12 registradas.

- [x] 🔴 **[MANUAL] `GATE-C07`** — Custo, cobrança e cronograma
  - **P13 — Cobrança do Claude Code.** Opções: (a) assinatura — custo previsível, mas limites de uso por janela de tempo podem cortar sessões no meio; (b) chave de API com teto de gasto — sem corte por janela, com custo real proporcional ao uso. ⭐ A escolha é livre, desde que seja **a mesma nos dois ciclos**. Se for (a): uma sessão cortada pelo limite é fechada com `/coletar-sessao`, e a retomada é uma sessão nova, com o corte registrado. O valor em USD da M3 é sempre calculado pela tabela de preços congelada, independentemente de como a conta é paga.
    **Decidido (22/09/2026, `GATE-C07` R19), contra a recomendação:** **assinatura** nos dois ciclos, o mesmo plano. Consequências: (i) **corte por limite de uso** — com o limite atingido, o modelo não responde, então a `/coletar-sessao` (que depende do modelo para executar o script) não roda; a sessão é fechada e coletada **à mão**, pelo terminal, com o script em modo `manual` (`C-016`), com `motivo_fim = limite_uso`; a retomada é uma sessão nova com o mesmo comando (P4); (ii) cortes semanais podem parar o ciclo por dias, em semanas diferentes em cada ciclo — registrado como ameaça na §12 do documento de métricas, com a contagem de cortes por ciclo; (iii) o plano de assinatura e os limites vigentes são registrados no `protocolo.md` no início de cada ciclo.
  - **P14 — Cronograma**, respeitando a Tabela 2 da análise de resultados iniciais:

    | Etapa | Proposta |
    |---|---|
    | Parte I (Fases 0–7 + congelamento) | 23/09 a 30/09 |
    | Ciclo A | 01/10 a 21/10 |
    | Transição A → B | 22/10 |
    | Ciclo B | 23/10 a 13/11 |
    | Trilha paralela do harness | 01/10 a 06/11 (data de corte da suíte hold-out: 06/11) |
    | Parte IV — Avaliação | 14/11 a 20/11 |

  - **P14 — Decidido (22/09/2026, `GATE-C07` R19):** ⭐ cronograma acima mantido. Condição registrada: capítulos da monografia que não dependem de dados (fundamentação, método, protocolo, ameaças) são escritos **durante** os ciclos, porque depois de 20/11 restam ~10 dias de novembro para análise, redação final, revisão e defesa (Tabela 2 da análise de resultados). Leitura da Tabela 2: a Parte I faz o papel de "setembro" do Ciclo A.
  - **Como confirmo:** P13 e cronograma registrados.
  - **Registro (22/09/2026):** P13 e P14 decididas (R19).

- [x] `C-003` Consolidar P1–P14 num arquivo `cerne-avaliacao/docs/protocolo.md`, com uma seção por decisão, a opção escolhida e a data, e uma seção **"Regras operacionais"**, que é a fonte única das regras de conduta do pesquisador (descrever o sintoma, nunca a solução; mensagens neutras; timebox; edição manual). As regras do RDR e dos artefatos entram na mesma seção pelo `C-004` (`GATE-C01` R7) — **Critério:** as 14 decisões presentes; nenhuma com "a definir"; nenhuma regra operacional duplicada no documento de métricas.
  - **Registro (22/09/2026):** `protocolo.md` com P1–P14 (e P1b, P1c, P5b, P5c), cada uma com opção e data, e a seção 3 "Regras operacionais" (15 regras; RDR e artefatos entram pelo `C-004`). Única dependência explícita: o **modelo** do simulador (P11) é escolhido a partir do HTML do protótipo no `C-006` — a regra está decidida, o valor concreto não. Nenhuma regra operacional duplicada no documento de métricas (§9 da v1.0 só com regras de dados).

### Encerramento da Fase 1 — notas para quem retomar
**Concluída em 22/09/2026.**
- **Gates:** `GATE-C04` (P1, P1b, P1c), `GATE-C05` (P2–P5c), `GATE-C06` (P6–P12), `GATE-C07` (P13, P14). `C-003` entregue.
- **Decisões contra a recomendação, com consequências já propagadas:** P2 (extensão do VS Code: mitigação manual antes de cada mensagem e contagem `n_msgs_contexto_ide`); P4 (uma sessão por comando do Spec Kit: hipótese da §8.3 reformulada para handoff mediado por artefatos, divergência nº 3 no `protocolo.md`); P12 (tudo em inglês, exceto a UI: o pacote da Fase 3 vira tradução fiel, conferida no `GATE-C13`); P13 (assinatura: modo `manual` de coleta e ameaça dos cortes semanais).
- **Achados da documentação atual que mudaram o plano:** `claude-sonnet-5` é snapshot fixo; o Sonnet 5 não tem *extended thinking* manual (esforço controla o raciocínio); `CLAUDE_CODE_EFFORT_LEVEL` prevalece sobre o frontmatter das metodologias; subagentes exigem `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`.
- **Correções de erro:** na P10, eu tinha lido a §2 dos requisitos como autorizando a versão simplificada; o cabeçalho da §2 exclui qualquer implementação funcional. Corrigido antes da decisão final.
- **Ajustes no documento de métricas v1.0 (antes do congelamento):** M2 (tempo ativo), M14 e §5.6 (P4), §8 (`n_msgs_contexto_ide`, `duracao_bruta_s`, `pausa_s`, `motivo_fim`, modo `manual`), §12 (quatro ameaças novas), §13 (item 7 decidido).
- **Pendências que passam adiante:** modelo do simulador (`C-006`/`GATE-C15`); ID do avaliador (antes do `C-021`); `setup-done`, menus e sessão de correção do BMAD (`GATE-C10`); `GATE-C00`/`C-000` (Wagner).
- **Carga nova para a Fase 6:** coleta em três modos (skill, hook, manual).

---

## Fase 2 — Regras específicas de cada metodologia (congeladas juntas)
**Prazo proposto: 25 a 26/09/2026**

As regras do Ciclo B são decididas **agora**, com as do Ciclo A, e congeladas no mesmo ato. Critério geral para as duas: **seguir o fluxo recomendado pela documentação oficial da versão travada**, sem extensões, presets, módulos ou agentes da comunidade, e sem customização além do que a própria instalação pede.

- [x] 🔴 **[MANUAL] `GATE-C08`** — Travar as versões das duas metodologias
  - **Spec Kit:** a linha estável atual é a 1.0.x (v1.0.8 era a mais recente em 22/09/2026). Conferir a mais recente estável no dia do congelamento e travar pelo número exato, com o comando de instalação e o modo de integração com o Claude Code (comandos `/speckit.*` ou modo skills, o que for o padrão da versão).
  - **BMAD-METHOD:** a mais recente é a v6.11.0 (10/08/2026). Essa versão mudou a Fase 4: `bmad-create-story`/`bmad-dev-story` foram depreciados, e a implementação passou a ser a cadeia `bmad-sprint-planning → bmad-build → bmad-code-review`. Travar a versão exata. Um corte da v7 durante o Ciclo B **não** é adotado.
  - **Decidido (22/09/2026, `GATE-C08` R20):**
    - **Spec Kit v1.0.10** (lançada em 22/09/2026, marcada como *Latest*), travada agora; versões posteriores não são adotadas. Instalação: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.10`. Inicialização no repositório do ciclo (que já tem `docs/input/`): `specify init --here --force --non-interactive --integration claude`. O modo de integração (comandos `/speckit.*` ou skills) é o padrão da versão para o Claude Code, registrado na instalação (A1). Sem extensões, presets nem bundles (a extensão `bug`, embutida e opcional, não é instalada).
    - **BMAD-METHOD v6.11.0** (10/08/2026), travada; um corte da v7 não é adotado. Instalação **não interativa**: `npx bmad-method@6.11.0 install --directory <repo> --modules bmm --tools claude-code --yes`, com `--set` para o idioma de comunicação e de documentos em inglês (P12); as chaves exatas são conferidas com `--list-options bmm` e registradas. A instalação por flags substitui o registro das respostas ao instalador interativo.
  - **Notas de versão lidas (24/09/2026):** 1.0.0–1.0.10, todas. Nenhuma muda a sequência do `GATE-C09`. Mudanças que tocam o núcleo, todas já dentro da versão travada: 1.0.5 — o `tasks` passa a exigir as restrições de campo do `data-model.md`; 1.0.7 — o `clarify` passa a limitar o que adia para o planejamento a detalhes de implementação; 1.0.9 — *bundles* oficiais de correção de bug e de avaliação, opcionais (fora do fluxo, pela regra sem bundles); 1.0.10 — correção na injeção de frontmatter das integrações. Aviso de descontinuação futura do `/speckit.taskstoissues` (não usado). A **v1.0.11 saiu em 24/09/2026** e não é adotada, conforme a decisão.
  - **Como confirmo:** as duas versões registradas com o comando exato de instalação; changelog das duas lido até a versão travada.

- [x] 🔴 **[MANUAL] `GATE-C09`** — Fluxo do Ciclo A (Spec Kit)
  - **Setup (uma vez):** `/speckit.constitution` com o prompt `P-SETUP` (Fase 3).
  - **Por unidade de trabalho (F000 e cada RF):** `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement`.
  - **Opcionais — decidir e aplicar igualmente a toda unidade:** `/speckit.checklist` (⭐ não usar: gera checklists de qualidade de requisitos, não entra no fluxo mínimo) e `/speckit.converge` (⭐ usar só se a documentação da versão travada o colocar no fluxo recomendado; se ficar como opcional, não usar).
  - **Achado (README da v1.0.x):** o fluxo **oficial** mudou em relação ao que este gate supunha. O núcleo é `constitution → specify → plan → tasks → implement → converge`, repetindo `implement`/`converge` até o `converge` reportar *Converged*; o `converge` é comando **core**. `clarify` (recomendado antes do `plan`), `analyze` (depois do `tasks`, antes do `implement`) e `checklist` são **opcionais**.
  - **Decidido (22/09/2026, `GATE-C09` R20):** **setup:** `/speckit.constitution` com `P-SETUP`. **Por unidade:** `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement` → `/speckit.converge`, repetindo `implement` → `converge` até *Converged*. ~~`checklist` não é usado.~~ **Revisto (22/09/2026, R22, por simetria com o BMAD completo):** `/speckit.checklist` entra **depois do `clarify`** em toda unidade. Sequência final por unidade: `specify` → `clarify` → `checklist` → `plan` → `tasks` → `analyze` → `implement` → `converge` (laço `implement` → `converge` até *Converged*). Uma sessão por comando (P4). "O agente declara pronto" (P6) passa a ser: o `converge` reporta *Converged*. O laço é limitado só pela timebox (P7).
  - **Como confirmo:** sequência exata registrada, com os opcionais decididos.

- [x] 🔴 **[MANUAL] `GATE-C10`** — Fluxo do Ciclo B (BMAD-METHOD)
  - **Trilha:** ⭐ "BMad Method" (a trilha padrão para produto com PRD e arquitetura). Não usar a Quick Flow (enxuta demais, aproximaria o BMAD do Spec Kit) nem a Enterprise.
  - **Módulos:** ⭐ só o núcleo (BMM). Sem TEA, CIS ou outros.
  - **Fase 1 — Análise (opcional no BMAD):** ⭐ só o product brief, alimentado pelo pacote de entrada. Brainstorming e pesquisa ficam de fora, porque o pacote já traz o problema definido.
  - **Fase 2 — Planejamento:** PRD (obrigatório). **UX design:** ⭐ não rodar o workflow de UX, porque o protótipo congelado é a especificação de UX e vai no pacote. Registrar como adaptação do fluxo, igual à entrega do protótipo ao Spec Kit.
  - **Fase 3 — Solução:** arquitetura → épicos e stories → verificação de prontidão para implementação.
  - **Onde entra o `P-SETUP` (os princípios técnicos).** No Spec Kit, eles viram a constitution, no setup. O análogo mais próximo no BMAD é o arquivo de contexto de projeto (`bmad-project-context` na v6.11). ⭐ Se a versão travada permitir rodá-lo em projeto novo (greenfield), o `P-SETUP` entra nele, durante o setup (B1), e o tempo conta como M1, como no Spec Kit. Se não permitir, o `P-SETUP` entra como primeira mensagem do workflow de arquitetura, e o setup do BMAD fica só com instalação e configuração — registrar a assimetria na M1.
  - **Fase 4 — Implementação (v6.11):** `bmad-sprint-planning` uma vez; por story, `bmad-build` → `bmad-code-review`.
  - **Sessões:** uma sessão nova por workflow, como o BMAD orienta (regra P4).
  - **Respostas ao instalador interativo:** ⭐ só o módulo BMM; Claude Code como ferramenta; idioma de comunicação e de documentos em inglês (P12). *(Substituído pelo `GATE-C08`: instalação não interativa por flags.)*
  - **Timebox do planejamento global (sessões `PLAN`):** o Spec Kit não tem etapa equivalente, então a P7 não cobre. ⭐ Teto de **16 horas de tempo em sessão** para o B2 + B3 juntos. Estourado, o planejamento é encerrado no estado em que está, registrado, e a implementação começa.
  - **Modelo:** conferir que nenhum arquivo de customização de agente do BMAD define um modelo próprio. Todos os agentes rodam no modelo da P1.
  - **Achado (documentação da v6.11):** o fluxo mudou em relação ao que este gate supunha. A verificação de prontidão virou o portão de entrada do `bmad-sprint-planning` (PASS/CONCERNS/FAIL); os nomes atuais são `bmad-prd`, `bmad-ux`, `bmad-architecture`; o caminho de stories por `bmad-spec` usa `bmad-preview-ticketing`, prévia da v7; para projeto, a documentação recomenda retrospectiva a cada fronteira de épico.
  - **Decidido (22/09/2026, `GATE-C10` R21–R22), "BMAD completo", contra a recomendação (que era o caminho enxuto):**
    - **B1 Setup (`SETUP`):** instalação por flags (`GATE-C08`) → `bmad-project-context`, com o `P-SETUP` como regras do projeto.
    - **B2 Análise (`PLAN`):** `bmad-brainstorming` → `bmad-forge-idea` → `bmad-deep-recon` → `bmad-prfaq` → `bmad-product-brief`. Tudo o que o pesquisador responde vem **só do pacote de entrada**, com as respostas novas no RDR (`GATE-C11`); quando a ferramenta pedir ideias que o pacote não tem, a resposta diz isso.
    - **B3 Planejamento (`PLAN`):** `bmad-prd` (criar) → `bmad-prd` (validar) → `bmad-ux`, com o protótipo congelado como fonte, sem alterá-lo.
    - **B4 Solução (`PLAN`):** `bmad-architecture` → `bmad-create-epics-and-stories` → `bmad-sprint-planning` (portão de prontidão e `sprint-status.yaml`).
    - **B5 Implementação:** por story, `bmad-build` → `bmad-code-review` → `bmad-qa-generate-e2e-tests`; por épico, `bmad-retrospective` (sessão `PLAN`, fase `VALID`). `bmad-correct-course` só se ocorrer mudança grande.
    - **Fora:** `bmad-spec` (caminho alternativo de stories, com prévia da v7; rodá-lo junto geraria dois conjuntos de stories), `bmad-walkthrough` (revisão humana), `bmad-build-auto`, `bmad-shard-doc`.
    - **Elicitação avançada e party mode:** aceitos quando oferecidos; o pesquisador **escolhe livremente** o método, o que aceitar e como conduzir, e registra cada escolha no RDR (método escolhido, melhorias aceitas e descartadas). Respostas com `PROCESSO:`.
    - **Ameaças registradas (documento de métricas, §12):** (i) brainstorming e forge-idea pedem ideias ao pesquisador — ideias fora do pacote podem entrar no PRD e mudar o escopo só do Ciclo B; (ii) as escolhas livres na elicitação e no party mode são decisões do pesquisador dentro dos artefatos do B, não reproduzíveis; (iii) `bmad-qa-generate-e2e-tests` acrescenta testes que só o B tem, com efeito na M8 e na M13.
    - **Pendências verificadas na Fase 4, com o BMAD instalado:** nomes exatos das skills na v6.11.0 (`bmad-help` e diretório `.claude/skills/`); se o `bmad-project-context` grava no `AGENTS.md` e se o Claude Code lê esse arquivo; formato dos arquivos de story (a v6.11 aboliu a marcação de checkboxes de critérios de aceite, o que afeta a `M6_tasks` do B — alternativa no `C-022`).
    - **Timebox do planejamento global (R23):** 32 h de tempo ativo para B2–B4 juntos (substitui as 16 h originais); retrospectivas por épico ficam fora dessa timebox.
  - **Como confirmo:** sequência exata de workflows registrada, com o agente de cada um.

- [x] 🔴 **[MANUAL] `GATE-C11`** — Política de resposta às perguntas das metodologias
  - **Problema:** o `/speckit.clarify` e os workflows interativos do BMAD fazem perguntas ao pesquisador. Se as respostas forem improvisadas, cada ciclo recebe informação diferente.
  - ⭐ **Regra:**
    0. Toda resposta começa com `PROCESSO:` (regra 7).
    1. Responder **só com o que está no pacote de entrada**, citando a seção.
    2. Se o pacote não cobre a pergunta, consultar o **Registro de Decisões de Resposta** (`cerne-avaliacao/docs/rdr.md`).
    3. Se o RDR também não cobre, decidir na hora, responder com uma frase curta, e **acrescentar a decisão ao RDR** com data e ciclo.
    4. No Ciclo B, perguntas equivalentes recebem a resposta do RDR, **com o mesmo texto**.
    5. Preferências de gosto ("prefere a opção A ou B?") recebem sempre a resposta padrão: "Use o seu critério técnico, seguindo o pacote de entrada."
  - O RDR é um documento de protocolo, fica em `cerne-avaliacao` e nunca entra no repositório do ciclo. Só as respostas, dadas no chat, chegam ao agente.
  - **Decidido (22/09/2026, `GATE-C11` R23):** ⭐ confirmado, com três ajustes: respostas em inglês (P12) e com `PROCESSO:`; resposta padrão da regra 5: "Use your technical judgment, following the input package."; `bmad-sprint-planning` com CONCERNS → seguir; com FAIL → rodar a skill que o próprio achado indica. Escolhas livres na elicitação avançada e no party mode registradas no RDR (`GATE-C10`).
  - **Como confirmo:** regra registrada; `rdr.md` criado vazio.

- [x] 🔴 **[MANUAL] `GATE-C12`** — Regras de artefatos gerados pelas metodologias
  - O Spec Kit e o BMAD escrevem e atualizam o arquivo de contexto do agente (`CLAUDE.md`) e seus próprios artefatos. ⭐ Regra: o Wagner **nunca** edita esses arquivos à mão; se editar, é `INTERVENÇÃO [edição manual]`.
  - Git: cada metodologia conduz branches e commits como a própria documentação orienta. Ao declarar um RF concluído, o Wagner faz o merge em `main`, se a metodologia não fizer, com o script auxiliar `concluir-rf` (criado no `C-017`), que não altera código. Esse merge não conta como intervenção.
  - **Decidido (22/09/2026, `GATE-C12` R23):** ⭐ confirmado. Os arquivos incluem `CLAUDE.md`, `AGENTS.md`, `.specify/`, `specs/`, os artefatos do BMAD e o `sprint-status.yaml`.
  - **Como confirmo:** regras registradas.

- [x] `C-004` Registrar os `GATE-C08`–`C12` no `protocolo.md`, numa seção "Regras por metodologia", com o fluxo de cada ciclo desenhado como sequência numerada, a **tabela comando/workflow → fase** (`ESPEC`/`IMPL`/`VALID`; `GATE-C02` item 9) e a **lista de gatilhos `PROCESSO`** de cada framework (pausas previstas por comando ou workflow na versão travada) — **Critério:** as duas sequências, as duas tabelas de fase e as duas listas de gatilhos completas, sem "a definir".
  - **Registro (22/09/2026):** `protocolo.md`, seção 4 (versões, sequências numeradas, tabela de fases, gatilhos `PROCESSO` com definição operacional congelada e lista esperada) e seções 3.4–3.5 (regras do RDR e dos artefatos); `docs/rdr.md` criado vazio. A lista de gatilhos é conferida contra o texto dos comandos e skills instalados na Fase 4; itens novos entram pela definição congelada, sem reabrir o gate.

### Encerramento da Fase 2 — notas para quem retomar
**Concluída em 22/09/2026, com uma pendência no `GATE-C08`.**
- **Gates:** `GATE-C09`, `C10`, `C11`, `C12` fechados; `GATE-C08` decidido (Spec Kit v1.0.10; BMAD v6.11.0, instalação por flags), mas aberto até a leitura das notas de versão do Spec Kit 1.0.4–1.0.5 e 1.0.7–1.0.10 no `C-010`. `C-004` entregue; `rdr.md` criado.
- **Achados da documentação que mudaram o plano:** no Spec Kit 1.0.x, `converge` é comando central (laço `implement` → `converge`) e `clarify`/`analyze`/`checklist` são opcionais; no BMAD 6.11, a prontidão virou portão do `bmad-sprint-planning`, os nomes das skills mudaram, e o caminho por `bmad-spec` usa uma prévia da v7.
- **Decisões do Wagner além das recomendações:** Spec Kit com todos os opcionais (`clarify`, `checklist`, `analyze`); BMAD completo (análise inteira, incluindo brainstorming e forge-idea; PRD criar+validar; UX a partir do protótipo; QA e2e por story; retrospectiva por épico); elicitação avançada e party mode aceitos com escolha livre registrada no RDR. Três ameaças novas na §12 do documento de métricas.
- **Timebox do planejamento global do BMAD:** 32 h (era 16 h).
- **Para a Fase 3:** o pacote de entrada precisa de `P-SETUP` que funcione tanto como constitution quanto como regras do `bmad-project-context`; o `P-TECH` vai no `/speckit.plan` e na primeira mensagem do `bmad-architecture`.
- **Para a Fase 4:** conferências da seção 4.6 do `protocolo.md` (nomes de skills, `AGENTS.md`, formato das stories, gatilhos contra o texto instalado).
- **Risco de cronograma:** o Ciclo B ficou bem mais pesado (≈11 workflows de planejamento + 3 skills por story + retrospectivas) dentro de 23/10–13/11, com assinatura sujeita a cortes semanais (P13).

---

## Fase 3 — Pacote de entrada neutro
**Prazo proposto: 26 a 27/09/2026**

O pacote é **tudo** que o agente medido recebe como informação de produto, igual nos dois ciclos. Ele mora em `cerne-avaliacao/entrada/` e é copiado, com o mesmo hash, para `docs/input/` de cada repositório de ciclo no início do ciclo (A0 e B0).

**Nomes (22/09/2026, R25):** em `cerne-avaliacao`, a pasta continua `entrada/`; no repositório de cada ciclo, o pacote fica em **`docs/input/`**, com arquivos em inglês: `requirements.md`, `prototype/`, `backend/`, `prompts/`.

**Verificação de neutralidade em inglês (P12):** nos critérios dos `C-005`, `C-006` e `C-008`, o `grep` passa a usar `grep -n -i -E "stress|cycle|spec kit|spec-kit|bmad|metric|thesis|tcc|compar|hold-out|holdout|very_good_coverage|dcm|measure"`, com cada ocorrência revisada (falsos positivos esperados, ex.: "biometrics").

**Idioma (P12):** todo o pacote é escrito em **inglês**, como tradução fiel dos documentos-fonte, sem acrescentar nem omitir conteúdo. Textos de interface ficam em português, literais, entre aspas. Nomes de endpoints, códigos de erro, IDs (RFxx, RNFxx) e tokens de design não são traduzidos.

- [x] `C-005` Gerar `entrada/requirements.md` — versão neutra do `Requisitos_e_Fluxo_de_Telas_TCC.md`
  - **Fonte:** a versão reconciliada com o backend em 10/09/2026 (`ux/` do repositório do backend), **não** a cópia antiga do projeto — esta ainda traz, por exemplo, "criar/editar/apagar" no RF09, corrigido na reconciliação (entradas são imutáveis, D3). Ver "Itens em aberto".
  - **Remove:** toda a §8 (métricas); as linhas "**Estressa:**" de cada RF; qualquer menção a ciclos, metodologias, TCC, comparação, medição ou ferramentas de medição.
  - **Mantém:** RF01–RF10 com critérios de aceite; §2 (extensões, com a indicação de que não são implementadas); RNF01–RNF09 como requisitos de qualidade, com as metas (ex.: cobertura ≥80% no domínio), mas sem o "como medimos"; §5 (telas); §6 (endpoints); §7; §9–§12.
  - **Corrige:** §10 — `voyage-4` (fixo pelo backend), e a lista de lint e complexidade trocada pela regra de qualidade correspondente, sem nome de ferramenta de medição.
  - **Acrescenta:** a seção "Ordem de entrega" (P9) e a seção "Restrições técnicas" (P8, com a convenção de pastas).
  - **Critério:** `grep -n -i "estressa\|ciclo\|spec kit\|bmad\|métrica\|tcc\|comparaç\|very_good_coverage\|dcm"` vazio — exceto ocorrências legítimas (ex.: "ciclo de vida"), revisadas uma a uma.
  - **Registro (23/09/2026):** `entrada/requirements.md` gerado em inglês a partir dos requisitos reconciliados (SHA-256 `a62d8439…3db0`), com as remoções, acréscimos (§12 ordem de entrega, §13 restrições técnicas) e notas de precedência listados em `docs/revisoes/gate-c13-lista-de-revisao.md`. `grep` em inglês: só falsos positivos ("biometric").

- [x] `C-006` Gerar `entrada/prototype/` — o HTML do protótipo congelado e um extrato neutro do `doc-prototipo.md` (tokens visuais da §4 e a lista de estados). O extrato mantém as recomendações de implementação que já estão no documento (ex.: agrupar famílias de estado num só componente), porque os dois ciclos as recebem iguais — **Critério:** hash do HTML confere com o registrado no congelamento do backend (ver "Itens em aberto"); o extrato passa no mesmo `grep` do `C-005`.
  - **Registro (23/09/2026, R26):** hash do HTML congelado conferido — `61032a92…185d2fff`, igual ao do congelamento do backend (item em aberto resolvido). Os ciclos recebem uma **cópia derivada** (`entrada/prototype/cerne-prototype.html`) com uma única linha neutralizada (a menção ao TCC e às metodologias); o original fica em `cerne-avaliacao` para a M9; hash do derivado calculado no terminal. `prototype-extract.md` em inglês (mapa de navegação, estados, tokens, estados especiais, notas de implementação). Frame 390×844, grid 4 dp — candidatos da P11: iPhone 16e ou iPhone 14.

- [x] `C-007` Gerar `entrada/backend/` — cópia do pacote de handoff (`cerne-backend-handoff`): documentação da API dos 23 endpoints, taxonomia de 13 códigos de erro, mapa de estados de tela, semântica do selo de sincronização (D9) e fixtures. **Sem credenciais** — elas vão para o `.env` de cada ciclo (Fase 5) — e **sem** o roteiro de validação nem a coleção de testes de contrato, que são instrumento, não informação de produto — **Critério:** lista de arquivos conferida contra o pacote de handoff; nenhum segredo (`grep -i "key\|password\|secret"` revisado).
  - **Registro (23/09/2026, R26):** o handoff não era neutro nem estava em inglês; em vez de copiado, foi **traduzido e neutralizado**. `openapi.yaml` com só os textos traduzidos e verificação por script (estrutura idêntica à original sem os campos de texto). Fixtures: 3 mídias, transcrição esperada e 3 textos semeados; fora `textos.json`, D16, roteiro, testes de contrato e credenciais. Varredura de segredos: nenhum.

- [x] `C-008` Escrever os **prompts de intenção** em `prompts/` (fora de `entrada/`; R27) — neutros quanto à metodologia, prontos para colar, cada um com uma seção "Não fazer":
  - **Registro (23/09/2026):** 14 prompts em inglês; **movidos para `cerne-avaliacao/prompts/` (R27)** — ficam fora de `entrada/`, portanto fora de `docs/input/` nos ciclos, e são colados no chat conforme a tabela de entrega; hash registrado à parte do hash do pacote; `grep` só com falsos positivos. Nenhum prompt de RF repete critérios de aceite.

  | ID | Uso | Conteúdo |
  |---|---|---|
  | `P-SETUP` | Setup da metodologia | Princípios do projeto: stack fixa, convenção de pastas, Clean Architecture, `Either`, testes no domínio, tokens centralizados, UI fiel ao protótipo, português na UI. |
  | `P-GLOBAL` | Visão do produto | O que é o Cerne, para quem, o escopo (RF01–RF10), o que fica fora (extensões) e onde está o pacote. |
  | `P-F000` | Fundação | Scaffold, `design_tokens.dart`, cliente HTTP com `Either`, login/cadastro, navegação base, sessão expirada. |
  | `P-RF01` … `P-RF10` | Um por RF | Objetivo do RF, referência à seção do `requirements.md`, telas e estados do protótipo envolvidos, endpoints, dependências de RFs anteriores. |
  | `P-TECH` | Instrução técnica genérica | Texto fixo: "Siga as restrições técnicas de `docs/input/requirements.md` e a arquitetura já existente no projeto." |

  **Regras de redação:** nenhum prompt menciona a metodologia, métricas, o hold-out ou "o outro ciclo". Os prompts de RF **não repetem** os critérios de aceite — eles apontam para a seção do `requirements.md` —, para que o critério nunca apareça em versões diferentes nos dois ciclos.
  - **Critério:** 14 prompts escritos; mesmo `grep` do `C-005` vazio.
  - **Andamento (22/09/2026):** `P-SETUP` e `P-TECH` redigidos em inglês (dependem só de P8, P11 e P12); `grep` revisado — uma ocorrência, falso positivo ("biometrics"). `P-GLOBAL`, `P-F000` e `P-RF01`–`P-RF10` aguardam os requisitos reconciliados e o pacote de handoff.

- [x] `C-009` Escrever a **tabela de entrega dos prompts**, no `protocolo.md` (nunca no pacote):

  | Prompt | Ciclo A (Spec Kit) | Ciclo B (BMAD) |
  |---|---|---|
  | `P-SETUP` | argumento do `/speckit.constitution` (A1) | contexto de projeto no setup (B1) ou primeira mensagem da arquitetura, conforme o `GATE-C10` |
  | `P-GLOBAL` | anexado ao `P-F000` no primeiro `/speckit.specify` | entrada do product brief |
  | `P-F000`, `P-RFxx` | argumento do `/speckit.specify` da unidade | entrada do PRD, todos de uma vez e na ordem. Na implementação, o `bmad-build` é chamado só com a story, como a documentação manda — sem reenviar o `P-RFxx` |
  | `P-TECH` | argumento do `/speckit.plan` de toda unidade | não usado — as restrições entram na arquitetura via `P-SETUP` |

  **O fato de o BMAD receber todos os `P-RFxx` no planejamento, e o Spec Kit um por vez, é a diferença entre as metodologias** (planejamento antecipado × incremental). Não é assimetria de informação: o `requirements.md` completo está no repositório dos dois desde o início. Registrar na monografia.
  - **Critério:** tabela revisada pelo Wagner e congruente com os `GATE-C09`/`C10`.
  - **Registro (22/09/2026, R24):** tabela reescrita para o "BMAD completo" e gravada no `protocolo.md`, seção 5. Decisões: `P-TECH` também no BMAD, como primeira mensagem do `bmad-architecture` (corrige a linha "não usado" acima, que contradizia o encerramento da Fase 2); `P-GLOBAL` como argumento do `bmad-brainstorming`, demais skills de análise sem argumento; `P-F000` e `P-RFxx` todos de uma vez no `bmad-prd` (criar).

- [x] 🔴 **[MANUAL] `GATE-C13`** — Revisão de neutralidade do pacote
  - **O quê:** ler o pacote inteiro perguntando "isto favorece uma das metodologias, ou revela o que será medido?" e, por causa da P12, "a tradução acrescenta, omite ou muda algum requisito, critério ou texto de interface?" (comparação lado a lado com os documentos-fonte).
  - **Como confirmo:** revisão registrada; `sha256sum` de cada arquivo e um hash do pacote inteiro (`find entrada -type f | sort | xargs sha256sum | sha256sum`) gravados no `protocolo.md`.
  - **Registro (24/09/2026):** revisão lado a lado dos requisitos feita com o Wagner (16 blocos, 2 ajustes); protótipo aprovado; backend, fixtures e prompts conferidos por script; defeito nas mídias das fixtures corrigido antes dos hashes. Hash do pacote `dd6eb964…71c2`, dos prompts `d6e888c3…d8c`, do HTML derivado `aa8263b2…ae0b` — calculados pelo Wagner e conferidos contra o zip; registrados no `protocolo.md`, seções 5.1–5.2. Detalhe: `docs/revisoes/gate-c13-lista-de-revisao.md`.

### Encerramento da Fase 3 — notas para quem retomar
**Situação em 24/09/2026: fechada por completo.** `C-005`–`C-009` entregues; `GATE-C13` fechado (revisão lado a lado dos 16 blocos dos requisitos + protótipo + amostra do backend, todos fiéis, com 2 ajustes de tradução; hashes calculados pelo Wagner e conferidos — pacote `dd6eb964…71c2`, prompts `d6e888c3…d8c`, HTML derivado `aa8263b2…ae0b`, todos em `protocolo.md` §5.2).
- **Fontes recebidas:** `ux.zip` (requisitos reconciliados + HTML) e `cerne-backend-handoff-main.zip` (commit `fa998d9e`); os requisitos e o HTML são idênticos nos dois.
- **Achados:** o HTML congelado cita o TCC e as metodologias (cópia derivada neutralizada); o handoff cita os ciclos e está em português (traduzido e neutralizado, não copiado); o `doc-prototipo.md` usa numeração antiga de RF/RNF nos parágrafos "por que existe" (omitidos do extrato); a fonte tem contradições internas na §9 (esquema) e na §12 (10 × 13 códigos), tratadas com nota de precedência.
- **Decididas (R27):** prompts fora de `docs/input/` (em `cerne-avaliacao/prompts/`); limiar de complexidade fora dos requisitos; Tela 6 inteira na unidade RF09.
- **Decididas (R28):** ±4 dp fora; §8 mantida com nota de precedência; biblioteca de componentes incluída no extrato (seção 6).
- **`GATE-C13` fechado em 24/09/2026** (ver registro no gate).

---

## Fase 4 — Ambiente e ferramentas
**Prazo proposto: 27 a 28/09/2026**

- [x] 🔴 **[MANUAL] `GATE-C14`** — Registrar a máquina
  - **O quê:** modelo do Mac, chip, memória, versão do macOS. O macOS **não** é atualizado entre o início do Ciclo A e o fim do Ciclo B.
  - **Como confirmo:** dados registrados no `protocolo.md`, seção "Ambiente".
  - **Registro (25/09/2026):** MacBook Pro (`MacBookPro18,3`), Apple M1 Pro, 16 GB, macOS 27.0 (build `26A428`) — dados do Wagner via `system_profiler SPHardwareDataType`/`sw_vers`, gravados em `protocolo.md` §6.1.

- [x] `C-010` Instalar e travar as ferramentas de linha de comando: `fvm` com a versão de Flutter fixada (P8); Node LTS (para o instalador do BMAD); `uv`/Python (para o CLI do Spec Kit e os scripts do harness); CocoaPods; o CLI do Spec Kit na versão exata do `GATE-C08`. O instalador do BMAD **não** é instalado globalmente: roda via `npx` com a versão fixada, só no B0 — **Critério:** `fvm flutter --version`, `node -v`, `uv --version`, `pod --version` e a versão do CLI do Spec Kit registrados no `protocolo.md`.
  - **Registro (25/09/2026):** Flutter 3.47.5/Dart 3.13.4 (stable do dia, decisão registrada — P8 nunca tinha fixado um número), Node v26.10.0, uv 0.12.19, CocoaPods 1.17.0, Spec Kit CLI 1.0.10. Achado de ambiente corrigido: um `specify` do Homebrew (seguindo "stable", tinha puxado a v1.0.11 não adotada) disputava o PATH com o `uv tool install` correto — desinstalado; `~/.local/bin` também precisou ser adicionado ao PATH manualmente (`uv tool update-shell` não escreveu em `~/.zshrc`). Detalhe completo em `protocolo.md` §6.2.

- [ ] 🔴 **[MANUAL] `GATE-C15`** — Xcode e simuladores
  - **O quê:** travar a versão do Xcode e do runtime de iOS. Criar **dois** simuladores do mesmo modelo (P11): `sim-dev` (desenvolvimento, sem proxy) e `sim-aval` (avaliação, com o certificado do mitmproxy instalado). Separar os dois evita que o proxy de avaliação interfira no desenvolvimento, e que estado de desenvolvimento vaze para a avaliação.
  - **Como confirmo:** `xcrun simctl list devices` mostra os dois; versões registradas.

- [ ] `C-011` Instalar o Claude Code na versão fixada (≥ v2.1.277 — piso revisto em 25/09/2026, Fase 4: v2.1.197 é o exigido pelo Sonnet 5/P1, mas `AGENTS.md` só é lido automaticamente a partir da v2.1.277, condição do `bmad-project-context`/B1; ver `protocolo.md` §4.6) e desligar a atualização automática (`DISABLE_AUTOUPDATER=1`, ou o mecanismo da versão). Criar **dois diretórios de configuração limpos**, `cfg-ciclo-a` e `cfg-ciclo-b`, sem CLAUDE.md pessoal, skills pessoais, MCPs ou plugins, e com um script `abrir-ciclo <a|b>` que exporta `CLAUDE_CONFIG_DIR` e abre o **VS Code** no repositório certo, numa janela própria (P2), para que a extensão herde a configuração do ciclo. Travar as versões do VS Code e da extensão do Claude Code e desligar a atualização automática de extensões. A única coisa instalada nesses diretórios, mais tarde, é a `/coletar-sessao` (`C-016`) — **Critério:** `claude --version` registrado; `abrir-ciclo a` abre uma sessão onde `/context` não mostra nenhuma skill, MCP ou memória pessoal.

- [ ] `C-012` Escrever o `settings.json` único dos dois ciclos: `model: claude-sonnet-5` (P1), `alwaysThinkingEnabled: true` e `env.CLAUDE_CODE_EFFORT_LEVEL=high` (P1b), `env.CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5` + `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` e `env.ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001` (P1c), `allowlist` de permissões (P3), variáveis de ambiente, incluindo as do OpenTelemetry com exportação local, iguais nos dois ciclos (`GATE-C03` item 1) — **Critério:** o mesmo arquivo, com o mesmo hash, em `cfg-ciclo-a` e `cfg-ciclo-b`.

- [ ] `C-013` Instalar as ferramentas de avaliação: Maestro, mitmproxy, o coletor OpenTelemetry local (`GATE-C03` item 1), as dependências Python do harness e o SDK da OpenAI (avaliador), com as versões travadas — **Critério:** versões registradas; `maestro --version` e `mitmproxy --version` respondem.

- [ ] 🔴 **[MANUAL] `GATE-C16`** — Teste de fumaça só de ambiente
  - **O quê:** fora de qualquer repositório de ciclo (ex.: `/tmp/smoke`), `fvm flutter create` de um app de exemplo, rodar no `sim-dev`, conferir o Face ID simulado e a permissão de microfone pelo menu do simulador. Depois apagar o diretório.
  - **Decisão — spike do `whisper_ggml`:** o STT on-device é o ponto de ambiente mais arriscado (modelo pesado, simulador). Se falhar só no meio do Ciclo A, falha também no B, e o problema seria de ambiente, não de metodologia. Opções: (a) ⭐ spike mínimo no `/tmp`, feito pelo Wagner fora de qualquer ciclo, só para confirmar que o pacote roda no simulador desta máquina — o aprendizado é registrado como ameaça (o pesquisador conhece o pacote antes dos dois ciclos, igualmente); (b) não testar e assumir o risco.
  - **Como confirmo:** app de exemplo rodou; decisão do spike registrada, com o resultado.

### Encerramento da Fase 4 — notas para quem retomar
*(preencher ao concluir)*

---

## Fase 5 — Repositórios, credenciais e ambientes de backend
**Prazo proposto: 28/09/2026**

- [ ] 🔴 **[MANUAL] `GATE-C17`** — Criar os repositórios de ciclo
  - **O quê:** `cerne-ciclo-a` e `cerne-ciclo-b` no GitHub, privados e **vazios** (sem README, sem `.gitignore`, sem licença), para que a instalação de cada metodologia seja o primeiro conteúdo.
  - **Como confirmo:** os dois clonados localmente, sem commits.

- [ ] `C-014` Montar o `.env` de cada ciclo a partir das credenciais do pacote de handoff — URL e `anon key` do projeto Supabase do ciclo; **nunca** `service_role` —, guardado em `cerne-avaliacao/segredos/` (fora do Git) e copiado para o repositório do ciclo só no A0/B0 — **Critério:** os dois `.env` existem; `grep service_role` vazio nos dois.
  - **Registro (24/09/2026):** `segredos/.env.ciclo-a` e `.env.ciclo-b` criados, só com `FUNCTIONS_BASE_URL` (`https://<ref>.functions.supabase.co`) e `SUPABASE_ANON_KEY`; `grep service_role` vazio nos dois — confirmado. As credenciais de banco (`service_role`, senha do Postgres) recebidas junto **não são usadas aqui**: guardadas à parte, em `segredos/db.ciclo-a.env`/`db.ciclo-b.env`, para os scripts do `C-015` (`reset-ambiente`, importação/exportação de cache, backfill de embeddings, configuração do worker — todos conectam direto no Postgres, nunca pela API). `P-SETUP.md` do pacote de entrada ajustado para fixar os dois nomes de variável, que antes não estavam definidos.
  - **Pendência para o `GATE-C18`:** confirmar o `TEST_FAULT_KEY` de cada ambiente hospedado (o valor do `.env.local` do backend é só o de desenvolvimento local, não necessariamente o dos ambientes `ciclo-a`/`ciclo-b`).

- [ ] 🔴 **[MANUAL] `GATE-C18`** — Conferir os ambientes de backend
  - **O quê:** com os scripts do repositório do backend, conferir que o hash de schema de `ciclo-a` e `ciclo-b` continua igual ao do congelamento (`scripts/schema-hash.ts`), que o seed está carregado, e que as Edge Functions respondem.
  - **Como confirmo:** hash idêntico ao registrado em 11/09/2026; uma chamada autenticada com a conta seed responde 200 nos dois.

- [ ] 🔴 **[MANUAL] `GATE-C19`** — Estratégia de cache de IA e de reset
  - **Contexto:** o cache de replay (D5) garante respostas de IA idênticas entre os ciclos, mas só para requisições idênticas. No desenvolvimento, cada ciclo vai gerar requisições próprias (textos digitados, conversas de teste), que nunca vão coincidir.
  - ⭐ **Proposta:**
    1. **Durante o desenvolvimento:** `REPLAY_MODE=replay` no ambiente do ciclo — a IA real responde a quem o cache não cobre, e **grava** no cache (achado 24/09/2026: `record` e `replay` são idênticos no código do backend). O que acontece no desenvolvimento não é medido, então o não determinismo ali não afeta métrica, mas o cache de desenvolvimento é descartável e sempre substituído no reset antes da avaliação.
    2. **Na avaliação (Parte IV):** reset **uma única vez** por ciclo antes do início de cada passada da suíte (nunca no meio); uma passada única em `record` da suíte no `ciclo-a`; exportação desse cache para `harness/cache-ciclo-a.json`; reset + reimportação automática nos dois ciclos (`reset-ambiente`, `C-015`); e todas as execuções medidas em `replay_strict`. Como os prompts são montados no servidor (D5), as chaves de cache dependem só dos textos enviados, que a suíte fixa — não da implementação do app.
    3. **Reset:** nunca um `db reset` isolado. Sempre via `scripts/reset-ambiente <a|b>` (`C-015`), que em 4 passos devolve o banco ao seed, reconfigura o worker, reimporta o cache congelado (se já existir) e roda o backfill de embeddings — um reset "nu" apagaria o cache junto com os dados. Contas de desenvolvimento são criadas pelo próprio app (cadastro da F000) e nunca são as contas do seed.
    4. **`--force` do `replay-cache-import.ts`:** nunca usado no fluxo normal. Ele só libera importar sobre um destino não vazio; a inserção em si nunca sobrescreve (`on conflict do nothing`), então um `--force` sobre um destino com cache "sujo" mesclaria, silenciosamente, entradas erradas. Como todo reset deixa o destino vazio antes de importar, `--force` nunca é necessário — se o script recusar, é sinal de que o reset não rodou de verdade, e a correção é refazer o reset, não acrescentar `--force`.
  - **Como confirmo:** proposta aprovada ou ajustada; confirmado nos scripts do backend que a importação de cache aceita mesclar entradas novas num cache não vazio (hoje ela recusa sem `--force` — ver "Itens em aberto").

- [ ] `C-015` Escrever `scripts/reset-ambiente <a|b>` e `scripts/replay-mode <a|b> <modo>` como wrappers dos scripts do backend, com confirmação antes de executar.
  - **Achado (24/09/2026):** `record` e `replay` são idênticos no código do backend — os dois chamam o provedor de verdade e **gravam** no cache; só `replay_strict` nunca grava. E um reset recria o schema `experiment` inteiro do zero (`ai_replay_cache`, `worker_config`), junto com os dados de app. Um reset "nu" no meio da suíte, ou entre a importação e a execução medida, apaga o cache que acabou de entrar — cada chamada de IA vira `REPLAY_MISS`.
  - **`reset-ambiente <ciclo>` passa a ser um procedimento de 4 passos, sempre nesta ordem, nunca só o reset isolado:**
    1. Reset de fato (`supabase db reset` ou equivalente) — apaga dados de app e o schema `experiment`.
    2. Reconfigurar `experiment.worker_config` (`configure-worker.ts`), apagado no passo 1; sem isso os jobs de exportação (RF05) ficam presos em `pending`.
    3. **Se já existir um cache congelado exportado** (`harness/cache-ciclo-a.json` — inexistente só antes da passada `record` do `V-002`): importar com `replay-cache-import.ts --in harness/cache-ciclo-a.json`, sem `--force` (o destino está vazio logo após o reset, então a trava do script não impede a importação).
    4. Rodar `backfill-seed-embeddings.ts` — a conta A fica com as 33 entradas em `embedding_status='pending'` depois de qualquer reset; o script também passa pelo cache de replay, então roda melhor **depois** do passo 3.
  - **Regra:** nenhuma chamada de `reset-ambiente` pode pular os passos 2–4. Isso vale para os dois ciclos, em qualquer momento — inclusive resets do `ciclo-a` depois da sua própria passada `record`.
  - **Critério:** rodado em modo de simulação (`--dry-run`) nos dois ambientes, mostrando os 4 passos; rodado de verdade uma vez em cada ambiente e confirmado que account A tem 34 entradas com só 1 em `failed` e as demais com embedding, e que um job de exportação de teste sai de `pending`.

### Encerramento da Fase 5 — notas para quem retomar
*(preencher ao concluir)*

---

## Fase 6 — Instrumento mínimo pré-ciclo
**Prazo proposto: 29/09/2026**

Só o que precisa existir **antes** da primeira sessão medida. O restante do harness nasce na trilha paralela.

- [ ] `C-016` Escrever a skill `/coletar-sessao` e o script `scripts/coletar_sessao.py`
  - **Onde é instalada:** como **skill de usuário** dentro de `cfg-ciclo-a` e `cfg-ciclo-b` — **fora do repositório do ciclo**. Se fosse skill de projeto (`.claude/skills/` no repositório), o arquivo ficaria na árvore do projeto e o agente poderia encontrá-lo ao listar ou buscar arquivos, mesmo com a skill fora do contexto. (Ajusta a seção 4.1 do documento de métricas v2, que previa skill de projeto.)
  - **Skill** (fonte em `cerne-avaliacao/skills/coletar-sessao/SKILL.md`): frontmatter com `disable-model-invocation: true`; argumento `<ID>` ∈ {`SETUP`, `PLAN`, `F000`, `RF01`…`RF10`}; corpo mínimo que só chama o script, pelo caminho absoluto em `cerne-avaliacao`, e exibe o que ele devolver.
  - **Script:** localiza o JSONL da sessão atual; acha o timestamp da mensagem de invocação e corta tudo a partir dela; soma o `usage` por categoria; calcula o tempo ativo, o tempo bruto e as pausas (P5c) e as marcas de tempo; extrai as mensagens com prefixo `INTERVENÇÃO [tipo|campos]` e separa os campos (tipo, severidade, nível, causa); extrai as mensagens com prefixo `PROCESSO:` (série M5b) para `revisoes_processo.csv`; tem um terceiro modo, `manual`, rodado no terminal com o ID da sessão, para sessões cortadas por limite de uso ou falha, em que a skill não pode rodar (P13), gravando `motivo_fim`; atribui a cada trecho a fase da tabela congelada no `C-004` e soma tempo e tokens por segmento; conta as mensagens do pesquisador que chegaram com contexto injetado pela extensão do VS Code (`n_msgs_contexto_ide`, P2); registra compactações; compara a soma de tokens com o total do OTel da sessão e registra a diferença relativa (coluna `div_otel`), marcando-a quando passa da tolerância fixada aqui; grava em `sessoes.csv`, `segmentos.csv`, `intervencoes.csv` e `revisoes_processo.csv`; copia o JSONL para `dados/<ciclo>/brutos/`; e devolve só o que o `GATE-C03` item 7 permite (confirmação, contagens reconhecidas, avisos de prefixo mal formado), mais o **estado do timebox** da unidade (P7) em faixas — "abaixo de 50%", "50–80%", "acima de 80%", "atingido". O timebox é medido em tempo de sessão, então o pesquisador precisa saber quando parar; as faixas dão isso sem expor o valor exato.
  - **Modos:** skill (corte na mensagem de invocação); hook `SessionEnd` (ID lido do arquivo gravado por `scripts/marcar-sessao`; corte na última mensagem) — `GATE-C03` item 5; e `manual`, rodado no terminal para sessões cortadas por limite de uso ou falha (P13), com corte na última mensagem.
  - **Critério:** testes unitários do script, nos três modos, sobre quatro transcripts sintéticos (sem intervenção; com 3 intervenções de tipos diferentes; com compactação no meio; com um subagente cujos tokens estão em arquivo separado) passam, a soma inclui os tokens do subagente, e o corte exclui a mensagem de invocação e tudo depois dela.

- [ ] `C-017` Escrever os scripts auxiliares do pesquisador:
  - `concluir-rf <ciclo> <ID>`: faz o merge em `main` (se a metodologia não fez), cria a tag `ciclo<X>/<id>-done` e registra data e commit em `dados/<ciclo>/tags.csv`.
  - `rf-incompleto <ciclo> <ID>`: a mesma coisa com a tag `-incompleto` (P7).
  - `instalar-metodologia <a|b>`: roda o instalador da metodologia do ciclo com a versão e os parâmetros congelados (`GATE-C08`), cronometra e grava a duração em `sessoes.csv` com `tipo_sessao = instalacao`; cria a tag `ciclo<X>/instalado`. **Decidido (22/09/2026, `GATE-C01` R5):** esse tempo entra na M1. M1 = instalação + sessões `SETUP`, reportadas também separadamente, ao lado do tempo de calendário (início da instalação → `setup-done`). A definição da M1 na v1.0 declara a assimetria do BMAD se o `P-SETUP` for para a arquitetura (`GATE-C10`).
  - `iniciar-ciclo <a|b>`: copia o pacote de entrada para `docs/input/` e o `.env`; cria um `.gitignore` com uma única linha (`.env`), para o segredo não ser versionado por acidente; confere os hashes; faz o commit inicial e cria a tag `baseline`. A metodologia é instalada **depois**, na sessão de setup.
  - **Critério:** os quatro rodados com sucesso num repositório descartável.
  - **Convenção de tags resultante** (atualiza a seção 3.3 do documento de métricas): `baseline` (pacote copiado) → `instalado` (metodologia instalada) → `setup-done` → `plan-done` (só Ciclo B, fim do planejamento global, `GATE-B03`) → `f000-done` → `rfNN-done` ou `rfNN-incompleto` → `final`.

- [ ] 🔴 **[MANUAL] `GATE-C20`** — Verificar que a skill fica fora do contexto do agente
  - **O quê:** num repositório descartável com a skill instalada, abrir sessões com `abrir-ciclo a` e com `abrir-ciclo b` e rodar `/context`.
  - **Como confirmo:** a `coletar-sessao` **não** aparece no contexto nas duas configurações. Screenshot guardado em `dados/evidencias/`. Se aparecer, ativar o fallback do `GATE-C03` (hook `SessionEnd`) e repetir a verificação.

- [ ] 🔴 **[MANUAL] `GATE-C21`** — Ensaio geral
  - **O quê:** num repositório descartável, simular uma unidade de trabalho completa: `iniciar-ciclo`, sessão com duas intervenções prefixadas com campos diferentes e uma resposta `PROCESSO:`, `/coletar-sessao RF01`, `concluir-rf`. Depois apagar o repositório e as linhas de CSV do ensaio. Na sessão do ensaio, provocar ao menos um subagente e conferir o campo `model` do transcript dele (P1c).
  - **Como confirmo:** CSVs com exatamente as linhas esperadas; subagente em `claude-sonnet-5`; tag criada; transcript copiado; nenhuma sobra do ensaio nos dados reais.

### Encerramento da Fase 6 — notas para quem retomar
*(preencher ao concluir)*

---

## Fase 7 — Especificação do instrumento de avaliação
**Prazo proposto: 29 a 30/09/2026**

O que se congela aqui são **definições em texto**. O código correspondente é escrito na trilha paralela e testado no repositório de calibração, nunca no código dos ciclos.

- [x] `C-018` Escrever `holdout/cenarios.md` — um cenário por critério de aceite dos RF01–RF10 (§1), cada um com: conta do seed e pré-condição; passos pela UI, identificando elementos só por **texto visível do protótipo**; asserção (UI, proxy ou SQL); e se o critério é estrutural (checado estaticamente) em vez de comportamental — **Critério:** todo critério de aceite da §1 tem cenário ou justificativa de exclusão; o critério do RF09 sobre "editar/apagar" segue a versão corrigida no congelamento do backend (entradas são imutáveis, D3).
  - **Registro (24/09/2026):** `holdout/cenarios.md` — 28 cenários para os 27 critérios (3 estruturais: H07-2, H07-3, H10-1), nenhuma exclusão; execução em blocos por causa do cache de replay (IA na conta A antes de qualquer escrita); proxy injeta `X-Test-Now` (âncora do seed) e `X-Test-Key`; ambiguidade registrada no RF02 (gatilho do erro de transcrição = silêncio).

- [x] `C-019` Escrever `holdout/rnf09.md` — os 15 cenários de falha (5 endpoints de escrita × 3 falhas: timeout, resposta malformada, offline), injetados pelo mitmproxy, com o estado de erro esperado na UI — **Critério:** os 5 endpoints conferem com a lista congelada do backend (`entries-create`, `chat-messages-send`, `media-ocr`, `export-summary-create`, `chat-insight-create`).
  - **Registro (24/09/2026):** `holdout/rnf09.md` — 15 cenários nos 5 endpoints congelados; falha injetada pelo backend (`X-Test-Fault`) a partir do cabeçalho posto pelo proxy — divergência com a §7 do documento de métricas ("injeção pelo mitmproxy") levada ao `GATE-C22`; critério de "tratado" em 4 condições.

- [x] `C-020` Escrever `holdout/estados-m9.md` — a lista de estados avaliados na M9 (P10), com o caminho de navegação até cada um e o frame correspondente do protótipo — **Critério:** a lista bate com os 32 estados menos os de extensão.
  - **Registro (24/09/2026):** `holdout/estados-m9.md` — 31 estados, a partir do catálogo oficial de 32 estados extraído do HTML congelado (`frameGroups`), menos "Tela 5 — Planos de Ação" (P10).

- [x] `C-021` **Pré-requisito:** ID exato do modelo avaliador fixado e registrado no `protocolo.md` (`GATE-C02` item 6). Escrever as rubricas e os prompts do avaliador LLM (`harness/juiz/`): aderência ao plano (M6), espaçamento visual (M9), fidelidade de handoff (M14) e reclassificação de severidade (D16) — cada um com formato de saída estruturado e regra de anonimização (sem nome de metodologia, sem ciclo) — **Critério:** cada rubrica aplicada à mão a um exemplo sintético produz a saída esperada.
  - **Andamento (24/09/2026):** ID fixado — `gpt-5.5-2026-04-23`, `reasoning.effort = medium` (R29). `harness/juiz/`: protocolo comum com regras de anonimização e 4 rubricas (M6, M9, M14, D16), cada uma com prompt v1.0, schema, regra de maioria e exemplo sintético. **Lacuna encontrada:** a escala de severidade `Sn` da D16 nunca foi definida (a §8 do documento de métricas remete à "política D16", que só tem bloqueante/não bloqueante); proposta S1–S3 na rubrica, a confirmar. **Falta:** a aplicação à mão dos 4 exemplos pelo Wagner (critério).
  - **Registro (24/09/2026):** os 4 exemplos sintéticos aplicados à mão às rubricas — conferência feita pelo Claude, a pedido do Wagner. M9 e D16 chegam à saída esperada sem ambiguidade. M6: a causa da 2ª divergência admitia `ctx` ou `prd` → acrescentada regra de desempate (`ctx` prevalece quando algo não existe), prompt v1.1. M14: o exemplo admitia `partial` ou `no` → exemplo reescrito para o código usar o caso de uso e também importar o repositório, o que leva a `partial` pela definição. Changelog em `harness/juiz/README.md`.

- [ ] `C-022` Escrever como regras concretas (regex, caminhos, assinaturas): o critério de seleção das 8–10 decisões da M14; as 3–4 convenções da M15; **as regex de referências inexistentes da M6** (arquivos, pacotes, rotas, campos do schema, códigos da taxonomia de erros), com o hash da Especificação Técnica do backend usada como referência (`GATE-C02` item 10); **a lista de tipos de artefato contáveis da M4** por framework — no Ciclo B, lida nas tags `plan-done` e `final`; e **a regra da `M6_tasks` no Ciclo B**: % de checkboxes de tarefas marcados nas stories de cada unidade, atribuídas pelo `mapa-stories.csv` (`GATE-B03`), com o formato dos arquivos de story confirmado na versão travada (`GATE-C01` R6) — **Critério:** cada regra da M15, as regex da M6 e a contagem da M4 são executáveis contra o repositório de calibração; o critério da M14 é aplicável a um `plan.md` qualquer sem julgamento adicional; a regra da `M6_tasks` do B é aplicável a um arquivo de story de exemplo da versão travada.
  - **Andamento (24/09/2026):** `harness/regras.md` — M14 (fontes: constitution + `plan.md` da F000 × arquitetura do BMAD; regra de candidata e seleção das 10 primeiras, R29), M15 (4 convenções, referência na feature do RF01, R29), regex da M6 contra o contrato entregue, tipos da M4, e a `M6_tasks` do B com regra alternativa condicional. **Falta:** a execução das regras contra o repositório de calibração, que só existe na trilha paralela (`H-001`, `H-002`).

- [x] `C-023` Congelar a tabela de preços usada para a M3, com a data e a fonte — **Critério:** preço por categoria de token do modelo da P1 registrado.
  - **Registro (24/09/2026):** `harness/precos.md` — Sonnet 5 (2,00 / 10,00 / 2,50 / 4,00 / 0,20) e Haiku 4.5 (1,00 / 5,00 / 1,25 / 2,00 / 0,10) por MTok, página oficial de preços da Anthropic consultada em 24/09/2026.

- [x] 🔴 **[MANUAL] `GATE-C22`** — Revisão do instrumento de avaliação (decisões R29–R30 já tomadas; falta a leitura final)
  - **O quê:** ler `C-018`–`C-023` perguntando "isto mede o que a §8 diz que mede, igualmente para as duas metodologias?".
  - **Como confirmo:** revisão registrada.
  - **Registro (24/09/2026):** leitura de conferência feita pelo Claude, a pedido do Wagner, por script e à mão: as funções citadas em `holdout/` existem entre as 23 do backend; os tipos de falha (`timeout`, `malformed`, `offline`, `ai_timeout`) existem no backend; as chaves de texto usadas existem em `textos.json` (as 3 novas, `rnf09_mensagem_1..3`, criadas em `holdout/fixtures/textos-instrumento.json`); as contas e as sessões citadas existem no seed; os 31 ids de `estados-m9.md` existem no catálogo do protótipo (ficam de fora só `planos` e as três personas); rubricas ajustadas no `C-021`. Decisões R29–R30 já registradas.

### Encerramento da Fase 7 — notas para quem retomar
**Situação em 24/09/2026: fechada por completo.** `C-018`, `C-019`, `C-020`, `C-023`, `C-021` e `GATE-C22` concluídos; `C-022` escrito, com um único ponto ainda condicional (a regra alternativa da `M6_tasks` do B, a confirmar com a versão instalada do BMAD — já previsto, não é pendência nova).
- **Arquivos:** `holdout/cenarios.md` (28 cenários), `holdout/rnf09.md` (15 falhas), `holdout/estados-m9.md` (31 estados), `harness/juiz/` (protocolo + 4 rubricas), `harness/regras.md` (M4, M6, M14, M15, `M6_tasks` do B), `harness/precos.md`.
- **Decisões (R29–R30):** avaliador `gpt-5.5-2026-04-23`; M14 a partir da constitution + `plan.md` da F000 (A) e da arquitetura (B); M15 com referência na feature do RF01 e 4 convenções; escala de severidade S1–S3 (era uma lacuna: nunca tinha sido definida); `M6_tasks` do B por status `done` se as stories não tiverem checkboxes; falhas da hold-out injetadas pelo backend a partir do cabeçalho posto pelo proxy.
- **Achados:** o HTML traz um catálogo oficial de 32 estados e um painel de tokens *ground truth* — o extrato do protótipo foi refeito com eles (revisar no `GATE-C13`); o backend tem superfície de teste (`X-Test-Key`, `X-Test-Now`, `X-Test-Fault`) que a hold-out passa a usar; a ordem dos cenários precisa respeitar o cache de replay (IA antes de escrita na conta A).
- **Pendências do Wagner:** aplicar à mão os 4 exemplos sintéticos (`C-021`); `GATE-C22`; `GATE-C13` (revisão lado a lado + hashes); `GATE-C00`/`C-000`.
- **Pendências da trilha paralela:** executar as regras do `C-022` e os cenários no repositório de calibração (`H-001`, `H-002`, `H-005`); lista de anonimização (`harness/juiz/anonimizacao.txt`); textos `rnf09_mensagem_1..3` nas fixtures do instrumento.
- **Atenção antes do Ciclo B:** as seções B0–B3 e o bloco-padrão do Ciclo B, na Parte III deste plano, ainda descrevem o fluxo antigo do BMAD (instalador interativo, brief → PRD → UX → arquitetura → épicos → readiness check separado). O que vale é o `GATE-C10` e a seção 4.3 do `protocolo.md`. Reescrever a Parte III até a transição A → B (22/10).

---

## Checklist de congelamento do protocolo (portão de largada)
**Prazo proposto: 30/09/2026**

*Nenhum ciclo começa antes de todos os itens abaixo estarem marcados.*

**Instrumento**
- [ ] `Metricas_e_Skills_Ciclos.md` v1.0 publicado, sem pendência aberta
- [ ] `/coletar-sessao` testada, verificada fora do contexto (`GATE-C20`) e ensaiada (`GATE-C21`)
- [ ] Cenários da hold-out, estados da M9, rubricas, regras da M14/M15 e tabela de preços escritos (Fase 7)

**Protocolo**
- [ ] `protocolo.md` com P1–P14, regras por metodologia e tabela de entrega dos prompts
- [ ] `rdr.md` criado, vazio
- [ ] `desvios.md` criado, vazio

**Pacote de entrada**
- [ ] Pacote completo, revisado quanto à neutralidade (`GATE-C13`)

**Ambiente**
- [ ] Máquina, Xcode, simuladores, Flutter, Claude Code, Spec Kit, BMAD, Maestro, mitmproxy com versões travadas e registradas
- [ ] `settings.json` idêntico nas duas configurações
- [ ] Repositórios de ciclo vazios; `.env` prontos; ambientes de backend conferidos (`GATE-C18`)
- [ ] Estratégia de cache de IA e de reset aprovada (`GATE-C19`); wrappers testados em `--dry-run` (`C-015`)

**Congelamento**
- [ ] 🔴 **[MANUAL] `GATE-C23`** — Congelar
  - **O quê:** gerar `docs/hashes-congelamento.md` com o SHA-256 de: `Metricas_e_Skills_Ciclos.md`, `protocolo.md`, cada arquivo do pacote de entrada e o hash do pacote inteiro, a skill e seu script, os scripts auxiliares, `settings.json`, os arquivos de `holdout/` e de `harness/juiz/`. Commit e tag `protocolo-v1.0` em `cerne-avaliacao`.
  - **Como confirmo:** tag criada; `hashes-congelamento.md` versionado. A partir daqui, qualquer mudança nesses arquivos exige uma entrada em `desvios.md`.

---

# MARCO DE BIFURCAÇÃO

Até aqui, tudo foi feito uma vez e vale para os dois ciclos. A partir daqui, cada ciclo segue sua trilha. **O primeiro ato divergente é a instalação da metodologia no repositório.**

| Dimensão | Compartilhado (idêntico nos dois ciclos) | Diverge (cada metodologia faz do seu jeito) |
|---|---|---|
| Informação de produto | Pacote de entrada, mesmo hash | Quando e em que forma cada prompt entra (tabela de entrega, `C-009`) |
| Agente | Modelo, raciocínio, versão do Claude Code, `settings.json`, superfície | Topologia: agente único × agentes especializados |
| Ambiente | Máquina, Xcode, simulador, Flutter, backend do ciclo (schema idêntico) | — |
| Unidade de trabalho | F000 + 10 RFs, mesma ordem, mesmo timebox, mesma definição de "concluído" | Como a unidade é decomposta (spec/plan/tasks × PRD/épico/story) |
| Sessões | `/coletar-sessao` como última ação; nunca retomar; contexto reiniciado a cada fase nos dois (P4) | Quantas sessões cada método gera (comandos do Spec Kit × workflows do BMAD) |
| Intervenção | Prefixo, taxonomia, mensagens neutras, RDR | Quantas e quais perguntas a metodologia faz (série M5b) |
| Artefatos | Regra de não editar à mão | Quais artefatos existem e onde ficam |
| Medição | Todo o instrumento, os mesmos scripts, a mesma suíte | — |

---

# PARTE II — CICLO A (GitHub Spec Kit)
**Prazo proposto: 01/10 a 21/10/2026**

Tudo aqui acontece em `cerne-ciclo-a`, aberto sempre com `abrir-ciclo a`.

## A0 — Instalação e baseline
**Prazo proposto: 01/10/2026**

- [ ] `A-001` Rodar `iniciar-ciclo a` — **Critério:** tag `cicloA/baseline` criada; hash do `docs/input/` igual ao do congelamento.

- [ ] 🔴 **[MANUAL] `GATE-A01`** — Instalar o Spec Kit
  - **O quê:** no terminal, fora de sessão do Claude Code, rodar `scripts/instalar-metodologia a`, que executa o `specify init` da versão travada com os parâmetros registrados no `GATE-C08` e grava a duração em `sessoes.csv` com `tipo_sessao = instalacao` (parte da M1). Commit do resultado.
  - **Como confirmo:** estrutura do Spec Kit presente (`.specify/`, comandos ou skills do Spec Kit para o Claude Code); tag `cicloA/instalado`.

- [ ] 🔴 **[MANUAL] `GATE-A02`** — Conferência de largada
  - **O quê:** abrir uma sessão com `abrir-ciclo a`, rodar `/context` e conferir: modelo correto, nenhuma skill além das do Spec Kit, `coletar-sessao` ausente do contexto. Fechar a sessão **sem** mandar nenhuma mensagem.
  - **Como confirmo:** screenshot em `dados/evidencias/`. Essa sessão não é medida — nenhuma mensagem foi enviada, logo não há `/coletar-sessao`.

## A1 — Setup (constitution)
**Prazo proposto: 01 a 02/10/2026**

- [ ] 🧪 **[SESSÃO] `A-002`** — Nova sessão; `/speckit.constitution` com o conteúdo de `P-SETUP`. Responder às perguntas conforme o `GATE-C11`.
- [ ] 📏 **[COLETA]** `/coletar-sessao SETUP` e encerrar a sessão.
- [ ] 📏 **[COLETA]** Tag `cicloA/setup-done` (via `concluir-rf a SETUP`).

---

## Bloco-padrão de unidade — Ciclo A

*Todas as unidades A2–A12 seguem este bloco. Os blocos específicos abaixo só acrescentam o que é próprio de cada unidade. Regra P4: **uma sessão por comando**.*

1. Para cada comando, na ordem — `/speckit.specify` (prompt da unidade: `P-F000` + `P-GLOBAL` na F000; `P-RFxx` nas demais), `/speckit.clarify`, `/speckit.checklist`, `/speckit.plan` (com `P-TECH`), `/speckit.tasks`, `/speckit.analyze`, `/speckit.implement`, `/speckit.converge` — e de novo `implement` → `converge` até o `converge` reportar *Converged* (`GATE-C09`):
   1. 🧪 **[SESSÃO]** Nova sessão com `abrir-ciclo a`; fechar editores e desligar o anexo de contexto antes de cada mensagem (P2).
   2. 🧪 **[SESSÃO]** O comando, com o argumento indicado. No `clarify` e nas pausas previstas, respostas com `PROCESSO:`, conforme o `GATE-C11` (série M5b; toda resposta nova vai para o RDR). No `analyze`, se houver problemas, o agente resolve conforme o fluxo do Spec Kit; o pesquisador só confirma o avanço (`PROCESSO:` ou neutra).
   3. 📏 **[COLETA]** `/coletar-sessao <ID>` e encerrar a sessão. Se o comando não terminar na sessão (limite de uso, falha), a sessão seguinte repete o mesmo comando; o corte é registrado.
2. 🔴 **[MANUAL] Verificação de "concluído"** (P6), fora de sessão: `flutter analyze` sem erros; testes do agente passando; o app roda no `sim-dev`; o pesquisador percorre os critérios de aceite do RF.
3. 🧪 **[SESSÃO]** Se houver problemas: **sessão nova de correção**, aberta pela própria mensagem `INTERVENÇÃO [correção|Sn|causa]:` com a descrição do sintoma — nunca da solução —, sem comando da metodologia (fase `IMPL` na segmentação). `/coletar-sessao <ID>` ao fim. Repetir 2–3 até passar ou até o timebox (P7), que soma todas as sessões da unidade.
4. 📏 **[COLETA]** `concluir-rf a <ID>` (merge, se necessário, e tag `cicloA/<id>-done`) — ou `rf-incompleto a <ID>` se o timebox estourou.
5. 🔴 **[MANUAL]** Preencher as **notas de encerramento** da unidade neste arquivo (em `cerne-avaliacao`): datas, número de sessões, intervenções marcantes, respostas novas no RDR, bloqueios, desvios. **Sem números de métrica** (regra 8).

**Atenção:** a regra "descrever o sintoma, nunca a solução" (passo 3) vale igual no Ciclo B. A forma da sessão de correção no BMAD (com ou sem workflow) é confirmada no `GATE-C10`, buscando simetria com esta. Uma intervenção que dita a solução mede o pesquisador, não a metodologia.

---

## A2 — F000 Fundação
**Prazo proposto: 02 a 04/10/2026 · Timebox: 12 h em sessão**
- **Prompt:** `P-F000` + `P-GLOBAL`.
- **Escopo:** scaffold com a convenção de pastas (P8); `design_tokens.dart`; cliente HTTP com `Either<Failure, T>` e a taxonomia de 13 códigos; Tela 0 (splash); Tela 0.1a (login/cadastro); casca de navegação e Tela 3 (menu lateral, só navegação); tratamento de sessão expirada.
- **Backend:** §6.1 (autenticação e sessão).
- **Atenção:** o cadastro cria a conta de desenvolvimento do ciclo — nunca usar as contas do seed.
- **Notas de encerramento:** *(preencher)*

## A3 — RF03 Cofre de autenticação biométrica
**Prazo proposto: 04 a 05/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF03`. **Depende de:** F000.
- **Tela:** 0.1 (Cofre). **Backend:** nenhum endpoint próprio (biometria 100% local, D2).
- **Atenção:** Face ID pelo menu Features do simulador; o critério de 5 minutos em background exige espera real na verificação.
- **Notas de encerramento:** *(preencher)*

## A4 — RF01 Captura multimodal
**Prazo proposto: 05 a 07/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF01`. **Depende de:** F000, RF03.
- **Tela:** 2 (Modal de Inserção). **Backend:** §6.2.
- **Atenção:** sem câmera no simulador; foto testada pela galeria (arrastar imagem para o simulador); microfone do Mac.
- **Notas de encerramento:** *(preencher)*

## A5 — RF02 Processamento STT/OCR
**Prazo proposto: 07 a 08/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF02`. **Depende de:** RF01.
- **Tela:** 2 (indicador de transcrição, 4 estados). **Backend:** §6.2 (OCR). STT on-device (`whisper_ggml`).
- **Atenção:** ver resultado do spike do `GATE-C16`.
- **Notas de encerramento:** *(preencher)*

## A6 — RF07 Histórico multi-fonte (timeline)
**Prazo proposto: 08 a 10/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF07`. **Depende de:** F000, RF01.
- **Tela:** 4 (Meus Registros — timeline; tags manuais **não**, P10). **Backend:** §6.2.
- **Notas de encerramento:** *(preencher)*

## A7 — RF06 Busca semântica e filtros
**Prazo proposto: 10 a 11/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF06`. **Depende de:** RF07.
- **Tela:** 4 (busca e filtros); Tela 0 (sincronização de cache na splash). **Backend:** §6.4.
- **Notas de encerramento:** *(preencher)*

## A8 — RF04 Chat interativo com memória (RAG)
**Prazo proposto: 11 a 13/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF04`. **Depende de:** F000.
- **Tela:** 1 (Home/Chat); Tela 3 (histórico de sessões e botão "Novo Chat"). **Backend:** §6.3 (inclui o streaming).
- **Notas de encerramento:** *(preencher)*

## A9 — RF10 Salvar mensagem do chat como entrada
**Prazo proposto: 13 a 14/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF10`. **Depende de:** RF01, RF04.
- **Tela:** 1 (botão em mensagens do usuário). **Backend:** §6.2 (`POST /entries` com origem `chat`).
- **Notas de encerramento:** *(preencher)*

## A10 — RF08 Insights proativos
**Prazo proposto: 14 a 16/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF08`. **Depende de:** RF04.
- **Tela:** 1. **Backend:** §6.3 (insight).
- **Atenção:** o gatilho de 2 minutos de inatividade exige espera real na verificação.
- **Notas de encerramento:** *(preencher)*

## A11 — RF05 Exportação de resumo pessoal
**Prazo proposto: 16 a 18/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF05`. **Depende de:** RF07 (a exportação é acessada por Meus Registros).
- **Tela:** 4 (exportação, 5 estados). **Backend:** §6.5.
- **Notas de encerramento:** *(preencher)*

## A12 — RF09 Resumos temporais / dashboard
**Prazo proposto: 18 a 20/10/2026 · Timebox: 8 h**
- **Prompt:** `P-RF09`. **Depende de:** F000.
- **Tela:** 6 (Configurações — dashboard; seletor de persona **não**, P10; apagar conta, RNF05). **Backend:** §6.6, §6.7.
- **Notas de encerramento:** *(preencher)*

## Encerramento do Ciclo A
**Prazo proposto: 21/10/2026**

- [ ] `A-003` Conferir a completude dos dados do ciclo: toda sessão do transcript tem linha em `sessoes.csv`, exceto a sessão de conferência do `GATE-A02`, registrada em `dados/evidencias/`; toda unidade tem tag `-done` ou `-incompleto`; todos os JSONL copiados — **Critério:** script de conferência sem pendências. (Conferir completude não é olhar métrica: o script só conta linhas e arquivos.)
- [ ] 📏 **[COLETA]** Tag `cicloA/final`.
- [ ] 🔴 **[MANUAL] `GATE-A03`** — Nota de encerramento do Ciclo A: o que aconteceu de inesperado, desvios registrados, decisões novas no RDR.

---

# TRANSIÇÃO A → B
**Prazo proposto: 22/10/2026**

- [ ] `X-001` Conferir que nada do instrumento mudou: recalcular os hashes de `hashes-congelamento.md` e comparar — **Critério:** todos idênticos, ou cada diferença com entrada correspondente em `desvios.md`.
- [ ] `X-002` Conferir que o ambiente não mudou: versões de macOS, Xcode, Flutter, Claude Code e o ID do modelo ainda disponível na API — **Critério:** versões iguais às do `protocolo.md`. Se o modelo tiver sido descontinuado, **parar** e decidir com a orientadora antes de seguir.
- [ ] 🔴 **[MANUAL] `GATE-X01`** — Conferir o backend do Ciclo B
  - **O quê:** hash de schema do `ciclo-b` idêntico ao do congelamento (o `GATE-12` do backend); seed carregado; `REPLAY_MODE=replay` para o desenvolvimento (`GATE-C19`).
  - **Como confirmo:** hash conferido; chamada autenticada responde 200.
- [ ] 🔴 **[MANUAL] `GATE-X02`** — Registro do efeito de aprendizado
  - **O quê:** escrever em `dados/cicloB/aprendizado-previo.md` o que o pesquisador aprendeu no Ciclo A que pode influenciar o B (armadilhas do simulador, comportamento do backend, pacotes que falharam). A partir daqui: **não abrir o repositório `cerne-ciclo-a`** até o fim do Ciclo B.
  - **Como confirmo:** arquivo escrito e versionado. Ele vira uma subseção de ameaças à validade (ordem fixa A → B, D18).

---

# PARTE III — CICLO B (BMAD-METHOD)
**Prazo proposto: 23/10 a 13/11/2026**

Tudo aqui acontece em `cerne-ciclo-b`, aberto sempre com `abrir-ciclo b`. Unidades de trabalho, ordem, timebox, definição de "concluído", regras de intervenção e o RDR são os mesmos do Ciclo A.

## B0 — Instalação e baseline
**Prazo proposto: 23/10/2026**

- [ ] `B-001` Rodar `iniciar-ciclo b` — **Critério:** tag `cicloB/baseline`; hash do `docs/input/` igual ao do congelamento.
- [ ] 🔴 **[MANUAL] `GATE-B01`** — Instalar o BMAD
  - **O quê:** `scripts/instalar-metodologia b` (instalador via `npx` na versão travada). As respostas ao instalador interativo são as registradas no `GATE-C10` (módulos, ferramenta, idiomas). Commit do resultado.
  - **Como confirmo:** estrutura do BMAD presente; tag `cicloB/instalado`.
- [ ] 🔴 **[MANUAL] `GATE-B02`** — Conferência de largada, igual ao `GATE-A02`.

## B1 — Setup
**Prazo proposto: 23 a 24/10/2026**

- [ ] 🧪 **[SESSÃO] `B-002`** — Se o `GATE-C10` decidiu pelo contexto de projeto: nova sessão, workflow de contexto de projeto com `P-SETUP`. Caso contrário, esta tarefa não existe, e o setup do BMAD fica só com a instalação.
- [ ] 📏 **[COLETA]** `/coletar-sessao SETUP` (se houve sessão) e tag `cicloB/setup-done`.

## B2 — Planejamento global
**Prazo proposto: 24 a 28/10/2026**

*Sem equivalente no Ciclo A. Todas as sessões desta etapa usam o ID `PLAN`. Uma sessão nova por workflow (P4).*

- [ ] 🧪 **[SESSÃO] `B-003`** — Product brief (agente Analyst), com `P-GLOBAL`. → `/coletar-sessao PLAN`.
- [ ] 🧪 **[SESSÃO] `B-004`** — PRD (agente PM), com `P-F000` e `P-RF01`…`P-RF10`, **na ordem de entrega**. → `/coletar-sessao PLAN`.
- [ ] 🧪 **[SESSÃO] `B-005`** — Arquitetura (agente Architect); `P-SETUP` como primeira mensagem, **se** não entrou no B1. → `/coletar-sessao PLAN`.
- [ ] 🧪 **[SESSÃO] `B-006`** — Épicos e stories. → `/coletar-sessao PLAN`.
- [ ] 🧪 **[SESSÃO] `B-007`** — Verificação de prontidão para implementação. → `/coletar-sessao PLAN`.
- [ ] 🔴 **[MANUAL] `GATE-B03`** — Mapa story → unidade
  - **O quê:** registrar em `dados/cicloB/mapa-stories.csv` a que unidade (F000, RF01–RF10) pertence cada story gerada. Uma story que cobre dois RFs é atribuída ao que vem primeiro na ordem de entrega, com nota. **Não corrigir** a decomposição feita pelo BMAD — ela é dado. O mapa é usado pela `M6_tasks` e pela `/julgar-rf` (M6) do Ciclo B, que recebem as stories da unidade (`C-022`).
  - **Como confirmo:** toda story mapeada; toda unidade com pelo menos uma story.
  - **Se uma unidade ficar sem story:** registrar como achado (é dado sobre perda de escopo no planejamento) e mandar **uma** mensagem `INTERVENÇÃO [redirecionamento|prd]` pedindo que o requisito do pacote seja coberto, pelo workflow que o BMAD indicar. Mesma lógica do `GATE-B04`: desvio de escopo ou de ordem em relação ao pacote leva uma intervenção registrada, nunca uma correção manual.
- [ ] 📏 **[COLETA]** Tag `cicloB/plan-done`.

## B3 — Sprint planning
**Prazo proposto: 28/10/2026**

- [ ] 🧪 **[SESSÃO] `B-008`** — `bmad-sprint-planning`. → `/coletar-sessao PLAN`.
- [ ] 🔴 **[MANUAL] `GATE-B04`** — Conferir a ordem do sprint contra a ordem de entrega congelada. Se divergir, **uma** mensagem `INTERVENÇÃO [redirecionamento|prd]` pedindo que siga a ordem do pacote. (No Ciclo A, a ordem é garantida por construção, porque o pesquisador escolhe qual `P-RFxx` especificar; aqui o método decide, e a correção é registrada.)

---

## Bloco-padrão de unidade — Ciclo B

*Todas as unidades B4–B14 seguem este bloco. Escopo, telas, backend, dependências e atenções de cada unidade são os mesmos dos blocos A2–A12.*

1. Para cada story da unidade, na ordem do sprint:
   1. 🧪 **[SESSÃO]** Nova sessão; `bmad-build` com a story. → `/coletar-sessao <ID>`.
   2. 🧪 **[SESSÃO]** Nova sessão; `bmad-code-review` da story. → `/coletar-sessao <ID>`.
   3. Se o review devolver a story para ajustes, repetir 1.1–1.2, conforme o fluxo da versão travada.
2. 🔴 **[MANUAL] Verificação de "concluído"** (P6), idêntica à do Ciclo A. Problemas viram `INTERVENÇÃO [correção|Sn|causa]` descrevendo o sintoma, numa **sessão nova** com o workflow de implementação — é assim que o BMAD trabalha, e a regra P4 manda seguir a metodologia. → `/coletar-sessao <ID>`.
3. 📏 **[COLETA]** `concluir-rf b <ID>` ou `rf-incompleto b <ID>`.
4. 🔴 **[MANUAL]** Notas de encerramento da unidade, sem números de métrica.

| Bloco | Unidade | Prazo proposto | Timebox | Espelha |
|---|---|---|---|---|
| B4 | F000 Fundação | 29 a 30/10 | 12 h | A2 |
| B5 | RF03 Cofre | 30 a 31/10 | 8 h | A3 |
| B6 | RF01 Captura | 31/10 a 02/11 | 8 h | A4 |
| B7 | RF02 STT/OCR | 02 a 03/11 | 8 h | A5 |
| B8 | RF07 Timeline | 03 a 04/11 | 8 h | A6 |
| B9 | RF06 Busca | 04 a 05/11 | 8 h | A7 |
| B10 | RF04 Chat | 05 a 07/11 | 8 h | A8 |
| B11 | RF10 Salvar do chat | 07 a 08/11 | 8 h | A9 |
| B12 | RF08 Insights | 08 a 09/11 | 8 h | A10 |
| B13 | RF05 Exportação | 09 a 11/11 | 8 h | A11 |
| B14 | RF09 Dashboard | 11 a 12/11 | 8 h | A12 |

**Notas de encerramento por unidade:**
- **B4 — F000:** *(preencher)*
- **B5 — RF03:** *(preencher)*
- **B6 — RF01:** *(preencher)*
- **B7 — RF02:** *(preencher)*
- **B8 — RF07:** *(preencher)*
- **B9 — RF06:** *(preencher)*
- **B10 — RF04:** *(preencher)*
- **B11 — RF10:** *(preencher)*
- **B12 — RF08:** *(preencher)*
- **B13 — RF05:** *(preencher)*
- **B14 — RF09:** *(preencher)*

## Encerramento do Ciclo B
**Prazo proposto: 13/11/2026**

- [ ] `B-009` Conferência de completude dos dados, igual ao `A-003`, incluindo o `mapa-stories.csv`.
- [ ] 📏 **[COLETA]** Tag `cicloB/final`.
- [ ] 🔴 **[MANUAL] `GATE-B05`** — Nota de encerramento do Ciclo B.

---

# TRILHA PARALELA — Construção do harness de avaliação
**Prazo proposto: 01/10 a 06/11/2026 (data de corte da suíte hold-out: 06/11)**

Roda em `cerne-avaliacao`, em paralelo aos ciclos, **fora das sessões medidas**. Implementa as definições congeladas na Fase 7 — não as altera. Todo script é testado no repositório de calibração; **nenhum** script de medição roda sobre o código de um ciclo antes da Parte IV (regra 8).

- [ ] `H-001` Criar o repositório de calibração em `calibracao/`: app Flutter mínimo, na convenção de pastas (P8), com violações plantadas e documentadas num gabarito (`calibracao/gabarito.md`), incluindo a complexidade ciclomática de **cada** método do domínio calculada à mão pela regra da M12 (`GATE-C02` item 2): import proibido domínio → Flutter, import de `data/` no domínio, BLoC importando BLoC, chat importando repositório de entradas, cor e fonte hardcoded fora de `design_tokens.dart`, método com complexidade 12, repositório sem `Either`, teste que passa na tag `v1` e falha na `v2`, teste apagado na `v2`, e um teste de domínio que cobre um método sem asserção sobre o resultado (mutante sobrevivente plantado, para a M8b) — **Critério:** o gabarito lista cada violação com arquivo e linha.

- [ ] `H-002` Harness estático (`harness/estatico/`), cada módulo com teste contra o gabarito:
  - M4 — contagem de artefatos por tipo;
  - M6 (parte D) — % de tarefas marcadas (`tasks.md` no A; checkboxes das stories da unidade no B, via `mapa-stories.csv`), cruzamento plano × diff e referências inexistentes (regex do `C-022`);
  - M7 — varredura de imports com o mapa de camadas, só a regra do RNF06; o mesmo módulo emite à parte as regras estruturais do RF07 e do RF10, que contam na M11 (`GATE-C02` item 1);
  - M8 — cobertura do domínio, rodando os testes numa cópia temporária e gravando o lcov fora do repositório;
  - M9 (parte D) — hardcodes fora de `design_tokens.dart`;
  - M10 (parte D) — assinaturas `Either` nos repositórios;
  - M12 — complexidade ciclomática, pelo CLI Dart `harness/m12/` (`GATE-C02` item 2; `GATE-C03` item 3);
  - M8b — mutation score do domínio, só para a tag `final` (condicional: `GATE-C02` item 8);
  - M13 — lista de IDs de testes aprovados por tag e comparação com a tag anterior, incluindo apagados;
  - M14 (parte D) e M15 — regras do `C-022`.
  - **Critério:** cada módulo encontra exatamente as violações do gabarito — nem mais, nem menos.

- [ ] `H-003` Teste de introspecção tipográfica (M9): teste de integração **injetado na cópia temporária**, que percorre a árvore de widgets e extrai `fontFamily` e `fontSize` de cada texto, comparando com os tokens da §4 do `doc-prototipo.md` — **Critério:** no app de calibração, detecta a fonte plantada fora do token.

- [ ] `H-004` Amostragem de cor (M9, parte D): leitura de pixels nos screenshots, comparando com o hex primário do protótipo — **Critério:** acerta num par de imagens sintéticas (uma certa, uma errada).

- [ ] `H-005` Suíte hold-out (`holdout/`):
  - fluxos Maestro, um por cenário do `C-018` e por estado do `C-020`, com captura de screenshots;
  - addon do mitmproxy para os 15 cenários do `C-019` (injeção de falha) e para contagem de requisições (debounce do RF06);
  - asserções SQL contra o banco do ciclo.
  - **Validação possível antes da Parte IV:** o addon do proxy e as asserções SQL são testados direto contra o backend (requisições HTTP e banco no estado do seed). Os fluxos Maestro **não** podem ser validados num app real antes da Parte IV sem violar a regra 8; são revisados por leitura contra os textos do protótipo.
  - **Critério:** addon e asserções SQL verdes contra o backend; todo cenário do `C-018`/`C-019`/`C-020` tem implementação correspondente.

- [ ] `H-006` Skills de avaliação em `cerne-avaliacao/.claude/skills/`: `/avaliar-rf`, `/julgar-rf`, `/avaliar-ciclo`, `/validar-juiz`, como especificado nas seções 4.2–4.5 do documento de métricas — **Critério:** as quatro rodam de ponta a ponta sobre o repositório de calibração, gerando os CSVs com o esquema do `C-002`.

- [ ] 🔴 **[MANUAL] `GATE-H01`** — Data de corte da suíte hold-out (06/11)
  - **O quê:** se o `H-005` não estiver completo, ativar o fallback do `GATE-C02` (item 3): escrever o checklist manual roteirizado a partir do `C-018`/`C-019` e registrar o desvio. Na mesma data, se o módulo da M8b não encontrar o mutante plantado no repositório de calibração, a M8b sai e a ameaça de validação circular é declarada (`GATE-C02` item 8).
  - **Como confirmo:** duas decisões registradas: suíte ou checklist; M8b mantida ou retirada.

- [ ] 🔴 **[MANUAL] `GATE-H02`** — Congelar o código do harness
  - **O quê:** hash de todos os arquivos de `harness/`, `holdout/` e das skills de avaliação, acrescentado a `hashes-congelamento.md`, com commit e tag `harness-v1.0`. A partir daqui, o harness só muda por desvio registrado.
  - **Como confirmo:** tag criada antes do início da Parte IV.

---

# PARTE IV — AVALIAÇÃO
**Prazo proposto: 14 a 20/11/2026**

Só começa depois do `GATE-B05` e do `GATE-H02`. É o primeiro momento em que números de métrica são calculados e vistos.

- [ ] 🔴 **[MANUAL] `GATE-V01`** — Portão da avaliação
  - **O quê:** conferir que os dois ciclos têm tag `final`, que os hashes do instrumento batem (`X-001` de novo), que a decisão do `GATE-H01` (suíte ou checklist) está registrada e que `desvios.md` está atualizado.
  - **Como confirmo:** conferência registrada.

- [ ] `V-001` Rodar a parte estática da `/avaliar-rf` para todas as tags de unidade dos dois ciclos — **Critério:** uma linha em `rf.csv` por unidade e por ciclo.

- [ ] `V-002` Suíte hold-out, conforme a estratégia do `GATE-C19`:
  0. **Build:** cada app é compilado a partir da sua tag `final` numa cópia temporária, com o `.env` do ciclo injetado (ele não é versionado), e instalado no `sim-aval`. Nenhum arquivo é gravado no repositório do ciclo.
  1. `reset-ambiente a` (1º reset de `ciclo-a`; sem cache ainda, o passo 3 do wrapper é pulado); `replay-mode a record`; uma passada completa da suíte com o app do Ciclo A, no `sim-aval`. Todos os resets internos que `cenarios.md`/`rnf09.md` pedem, se algum, acontecem sempre via `reset-ambiente` — nunca um `db reset` isolado.
  2. Exportar o cache do `ciclo-a` (`replay-cache-export.ts`) para `harness/cache-ciclo-a.json`, versionado em `dados/evidencias/`.
  3. `reset-ambiente a` (agora reimporta `cache-ciclo-a.json` automaticamente — passo 3 do wrapper); `reset-ambiente b` (idem, primeira importação do B).
  4. `replay-mode a replay_strict` e `replay-mode b replay_strict`; rodar a suíte nos dois ciclos, na tag `final` de cada um, **sem nenhum reset adicional depois deste ponto** — se `cenarios.md` pedir um reset entre blocos, ele passa pelo wrapper completo (reimporta o cache automaticamente) e a suíte segue.
  5. Um `REPLAY_MISS`, em **qualquer um dos dois ciclos**, significa que o app enviou uma requisição que não está no cache congelado (esperado sobretudo no B, mas o protocolo trata os dois igual). Isso é achado sobre o app, não defeito do cache: registrar, rerodar só aquele cenário em `replay`, e marcar o resultado como "IA ao vivo".
  6. **Correções na suíte** (seletor errado, texto que não bate com o protótipo): permitidas só quando a falha é da suíte, não do app; aplicadas igualmente aos dois ciclos; cada uma registrada em `desvios.md` **antes** de rerodar.
  - **Achado e corrigido (24/09/2026):** a versão anterior tinha o reset do passo 3 **depois** da importação e **sem** reimportação automática — um reset "nu" ali apagaria o cache recém-importado antes da execução medida, produzindo `REPLAY_MISS` em tudo. Corrigido fazendo `reset-ambiente` sempre reimportar (ver `C-015`).
  - **Critério:** resultados de M10 e M11 por unidade nos dois ciclos; screenshots dos estados da M9 nos dois ciclos.

- [ ] `V-003` Rodar as partes determinísticas da M9 (cor, tipografia) sobre os screenshots e a árvore de widgets dos dois ciclos — **Critério:** uma linha por estado avaliado, por ciclo.

- [ ] `V-004` Rodar a `/julgar-rf` (M6) para todas as unidades dos dois ciclos, com as 3 execuções por item — **Critério:** `julgamentos.jsonl` completo; itens sem maioria marcados para a amostra humana.

- [ ] `V-005` Rodar a `/avaliar-ciclo` para A e B: agregação de M1–M5 (incluindo a linha de planejamento global e a série M5b), M14 (seleção pelo critério do `C-022`, checks estáticos e avaliador), M15, espaçamento da M9 pelo avaliador com visão e score final da M9 — **Critério:** `ciclo.csv` com M1–M15 para os dois ciclos.

- [ ] 🔴 **[MANUAL] `GATE-V02`** — Validação cega do avaliador (`/validar-juiz`)
  - **O quê:** classificar a amostra sorteada sem ver o voto do avaliador nem o ciclo de origem.
  - **Como confirmo:** kappa calculado por métrica julgada. Métrica abaixo do limiar do `GATE-C02` passa a exploratória, e a amostra humana vira o dado principal dela.

- [ ] `V-006` Gerar as tabelas e gráficos da monografia a partir de `ciclo.csv`, `rf.csv` e `validacao.csv` — **Critério:** cada número das tabelas é rastreável até uma linha de CSV.

- [ ] 🔴 **[MANUAL] `GATE-V03`** — Lacrar os dados
  - **O quê:** hash de `dados/` inteiro, commit e tag `dados-v1.0`. Nenhum dado muda depois disso sem entrada em `desvios.md`.
  - **Como confirmo:** tag criada; hash registrado no apêndice de reprodutibilidade da monografia.

---

# FECHAMENTO

## Cronograma consolidado

| Etapa | Proposta | Portão de saída |
|---|---|---|
| Fase 0 — Instrumento | 23 a 24/09 | `C-001` (métricas v1.0) |
| Fase 1 — Protocolo | 24 a 25/09 | `C-003` |
| Fase 2 — Regras por metodologia | 25 a 26/09 | `C-004` |
| Fase 3 — Pacote de entrada | 26 a 27/09 | `GATE-C13` |
| Fase 4 — Ambiente | 27 a 28/09 | `GATE-C16` |
| Fase 5 — Repositórios e backend | 28/09 | `C-015` |
| Fase 6 — Instrumento mínimo | 29/09 | `GATE-C21` |
| Fase 7 — Especificação da avaliação | 29 a 30/09 | `GATE-C22` |
| Congelamento | 30/09 | `GATE-C23` (tag `protocolo-v1.0`) |
| Ciclo A | 01 a 21/10 | `GATE-A03` (tag `cicloA/final`) |
| Transição | 22/10 | `GATE-X02` |
| Ciclo B | 23/10 a 13/11 | `GATE-B05` (tag `cicloB/final`) |
| Trilha paralela | 01/10 a 06/11 | `GATE-H02` (tag `harness-v1.0`) |
| Avaliação | 14 a 20/11 | `GATE-V03` (tag `dados-v1.0`) |

**Folga:** a Parte I cabe em 8 dias apertados. Se escorregar, a primeira compressão é na Fase 7 (as definições da avaliação podem ser congeladas até o início da trilha paralela, desde que **antes** de qualquer tag de unidade do Ciclo A). A segunda é no Ciclo B, que tem cerca de 4 dias a menos de implementação que o A (15 × 19) — compensados, em princípio, pelo planejamento global antecipado, que já tem seus próprios 5 dias.

## Registro de desvios de protocolo

*Vive em `cerne-avaliacao/docs/desvios.md`. Toda mudança em algo congelado entra aqui **antes** de ser aplicada.*

| # | Data | Item congelado | O que mudou | Por quê | Afeta | Ciclos já executados com a versão anterior |
|---|---|---|---|---|---|---|
| — | — | — | — | — | A / B / ambos | — |

## Itens em aberto — confirmar antes de depender

- **Hash do protótipo.** ~~Documentos anteriores citam `21f8787c…`; confirmar `61032a92…`.~~ **Resolvido (23/09/2026):** o HTML recebido tem `61032a92f082044f979cc52f65ae2d6cb461f0420f2bd9bc676f6115185d2fff`.
- **Versão canônica dos requisitos.** **Resolvido (23/09/2026):** recebida a versão reconciliada (`a62d8439…3db0`), base do `C-005`. *Texto original:* A cópia usada no planejamento ainda traz "criar/editar/apagar" no RF09 e "`voyage-3` ou `voyage-4`" na §10; a versão reconciliada fica no `ux/` do repositório do backend. O `C-005` parte da reconciliada.
- **Importação de cache.** ~~O `replay-cache-import.ts` recusa importar sobre cache não vazio sem `--force`. Confirmar se `--force` mescla ou sobrescreve.~~ **Resolvido (24/09/2026):** `--force` só libera a importação sobre um destino não vazio; a inserção em si é sempre `on conflict do nothing` — nunca sobrescreve, só ignora silenciosamente a `cache_key` repetida (o que é perigoso se o destino tiver cache próprio não intencional). Por isso a regra do `V-002` é nunca usar `--force`: todo reset antes de importar já deixa o destino vazio de verdade.
- **`disable-model-invocation`.** Há relatos de versões do Claude Code em que a descrição continua no contexto. Confirmado ou não no `GATE-C20`.
- **Modelo dos subagentes do Claude Code** (P1c). Configurável pela documentação (`CLAUDE_CODE_SUBAGENT_MODEL` + `_FORCE`); falta a verificação no `GATE-C21`.
- **`/speckit.converge`.** **Resolvido (22/09/2026, `GATE-C09`):** comando central da v1.0.x, usado em laço com o `implement`.
- **Contexto de projeto do BMAD em greenfield** (`bmad-project-context`). Decidido no `GATE-C10`; falta conferir, com a versão instalada, se grava no `AGENTS.md` e se o Claude Code lê esse arquivo.
- **Corte da v7 do BMAD.** A v6.11.0 anuncia remoções no corte da v7. Se a v7 sair durante o Ciclo B, a versão travada continua.
- **`whisper_ggml` no simulador.** Resolvido pelo spike do `GATE-C16`, se ele for feito.
- **Dimensões do dispositivo** (P11). **Resolvido (23/09/2026):** frame 390×844 (declarado no HTML); candidatos iPhone 16e ou iPhone 14, escolha no `GATE-C15`.

## Apêndice — Erros comuns a evitar

| Armadilha | Por que importa |
|---|---|
| Abrir este plano ou `cerne-avaliacao` numa sessão medida | O agente passa a conhecer as métricas |
| Retomar uma sessão onde a `/coletar-sessao` rodou | O relatório de coleta vira contexto do trabalho seguinte |
| Deixar a skill de coleta dentro do repositório do ciclo | O agente pode encontrá-la ao listar arquivos |
| Intervenção sem prefixo | Some da contagem da M5 |
| Intervenção que dita a solução em vez do sintoma | Mede o pesquisador, não a metodologia |
| Responder a uma pergunta da metodologia fora do pacote sem registrar no RDR | O outro ciclo recebe informação diferente |
| Usar `/clear`, ou rodar dois comandos do Spec Kit (ou dois workflows do BMAD) na mesma sessão | Quebra a regra P4: uma sessão por comando ou workflow |
| Mandar mensagem com editor aberto ou com o anexo de contexto ligado | A extensão injeta contexto invisível ao protocolo (P2) |
| Rodar a suíte hold-out durante um ciclo | Ela vira guia de desenvolvimento |
| Gravar cobertura ou relatório no repositório do ciclo | O agente vê os números |
| Olhar métrica do Ciclo A antes do fim do B | O pesquisador ajusta o comportamento no B |
| Usar `ultrathink`, `Option+T`, `/effort` ou `/model` numa sessão medida | O raciocínio e o custo variam por prompt, não por metodologia (P1b) |
| Usar alias de modelo | O modelo pode mudar no meio de um ciclo |
| Atualizar Claude Code, Xcode, Flutter ou macOS entre os ciclos | O ambiente deixa de ser o mesmo |
| Editar `CLAUDE.md` ou artefatos da metodologia à mão | Intervenção invisível |
| Corrigir à mão a decomposição do BMAD em stories | Apaga o dado sobre o planejamento dele |
| Ajustar a suíte ou o harness depois de ver um resultado sem registrar desvio | Destrói o valor do instrumento |
| Gravar o cache de IA duas vezes, uma por ciclo | Anula o mecanismo de replay (D5) |
| Usar as contas do seed no desenvolvimento | Suja o estado que a avaliação pressupõe |

---

*Checklist mestre gerado a partir dos documentos-fonte listados no cabeçalho. Em caso de divergência entre este arquivo e os documentos-fonte, os documentos-fonte prevalecem até o congelamento; depois dele, prevalece o protocolo congelado, e toda divergência vai para o registro de desvios.*
