# Protocolo experimental — Ciclos comparativos (app Cerne)

**Destino:** `cerne-avaliacao/docs/protocolo.md`
**Documento cumulativo.** Cada fase da Parte I do `plano-ciclos.md` acrescenta suas decisões. Congelado com hash no `GATE-C23` (tag `protocolo-v1.0`); depois disso, toda mudança passa por `docs/desvios.md`.
**Documento irmão:** `Metricas_e_Skills_Ciclos.md` v1.0 — o que é medido e como. Este protocolo diz **como o experimento é conduzido**, e é a fonte única das regras operacionais de conduta (Métricas v1.0, §9).

| Fase | Situação |
|---|---|
| 0 — Instrumento de medição | Decidida em 22/09/2026 (pendente só o repositório: `GATE-C00`, `C-000`) |
| 1 — Protocolo (P1–P14) | Decidida em 22/09/2026 (`GATE-C04`–`C07`; `C-003`) |
| 2 — Regras por metodologia | Decidida em 22/09/2026 (`GATE-C08`–`C12`; `C-004`); leitura das notas de versão do Spec Kit pendente (`C-010`) |
| 3 — Pacote de entrada e tabela de entrega | Gerado em 23/09/2026 (`C-005`–`C-009`); revisão no `GATE-C13` pendente |
| 4 — Ambiente | A preencher |

---

## 1. Decisões do instrumento de medição (Fase 0)

Todas registradas em 22/09/2026. Detalhe e justificativa: `Metricas_e_Skills_Ciclos.md` v1.0 e `docs/revisoes/gate-c01-roteiro-revisao.md`.

### 1.1 Base
| Decisão | Registro |
|---|---|
| Base do instrumento | Revisão v2 do documento de métricas, publicada como v1.0 (`GATE-C01` R1; `C-001` aprovado) |
| Pendências | 12 itens (11 da v2 + tags da hold-out), todos decididos; 2 subitens adiados com dono (Métricas v1.0, §13) |

### 1.2 Coleta por sessão (`GATE-C03`)
| # | Decisão |
|---|---|
| 1 | Fonte primária: transcript JSONL (principal + subagentes). OpenTelemetry ligado nos dois ciclos, só como conferência (`div_otel`); divergência reportada, nunca corrigida |
| 2 | IDs: `SETUP`, `PLAN`, `F000`, `RF01`–`RF10`. `PLAN` = planejamento global do BMAD; linha zerada no Spec Kit por construção |
| 3 | Linguagem: Python; CLI Dart só para a M12 (AST) |
| 4 | Transcripts brutos (principal e subagentes) copiados para `dados/<ciclo>/brutos/` no mesmo ato |
| 5 | Fallback: hook `SessionEnd` + `scripts/marcar-sessao <ID>` antes de fechar; corte na última mensagem |
| 6 | Repositório de calibração sintético, com violações plantadas e gabarito, único alvo de teste do harness |
| 7 | Exibição: confirmação; contagem de intervenções e `PROCESSO:` reconhecidas; avisos de prefixo mal formado; faixa da timebox. Nunca tokens, tempo, custo, `div_otel` |
| — | Skill `/coletar-sessao` como skill de **usuário** em `cfg-ciclo-a`/`cfg-ciclo-b`, nunca no repositório do app |

### 1.3 Marcação de mensagens
| Decisão | Registro |
|---|---|
| Intervenção | `INTERVENÇÃO [tipo\|Sn\|N1-N2\|causa]:` — severidade só em `correção`, na escala **S1** cosmético (nenhum critério afetado) · **S2** funcional com contorno (critério falha em parte, fluxo utilizável) · **S3** bloqueante (critério impossível, crash ou perda de dados) (R30); nível só em `edição manual`; causa (`ctx`/`chk`/`inc`/`prd`/`amb`/`out`) obrigatória em `redirecionamento`, `correção`, `edição manual` (`GATE-C01` R2-Q6) |
| Série M5b | Resposta a pausa **prevista pela metodologia** (lista de gatilhos congelada na Fase 2) começa com `PROCESSO:` e não é intervenção (R2-Q4, Q5) |
| Mensagem neutra | Confirmação a pausa **espontânea** do agente, e colar erro pedido pelo agente — sem prefixo (P5b) |

### 1.4 Métricas e ferramentas (`GATE-C02`)
| Item | Decisão |
|---|---|
| M1 | Instalação (fora de sessão) + sessões `SETUP`; componentes e calendário lado a lado (R5-Q15) |
| M2/M3 por fase | Segmentação `ESPEC`/`IMPL`/`VALID` mantida; tabela comando/workflow → fase congelada na Fase 2 (R3-Q7) |
| M4 | No BMAD, lida em `plan-done` e `final`; tipos contáveis no `C-022` (R6-Q18) |
| M6 | `M6_tasks` do BMAD = checkboxes das stories da unidade via `mapa-stories.csv`; regex no `C-022` (R6-Q17, Q18) |
| M7 | Script próprio; só RNF06. RF07/RF10 contam só na M11 (R6-Q16; R8) |
| M8b | Só na `final`, se detectar o mutante plantado até 06/11; senão, ameaça declarada (R4-Q11) |
| M9 | Estados e dispositivo → `GATE-C06` |
| M10/M11 | Hold-out automática só na tag `final`; fallback para checklist manual em 06/11 (R4-Q10; R8) |
| M12 | CLI Dart sobre a AST, regra de McCabe documentada, validada à mão; desvio da §8.2 dos requisitos declarado (R8) |
| M13 | Suíte do agente, tag a tag; testes apagados em `M13_apagados`; M13 com e sem (R4-Q10; R9) |
| §5.6 | Leitura dimensional final adotada como análise descritiva (22/09/2026) |
| Opcionais | Estimativa prévia e estabilidade da M14: não adotadas (R7-Q19) |

### 1.5 Avaliador LLM (`GATE-C02` item 6)
| Decisão | Registro |
|---|---|
| Família | OpenAI (GPT), com entrada de imagem |
| ID exato | `gpt-5.5-2026-04-23` (decidido em 24/09/2026; substituto indicado pela OpenAI para os snapshots que saem do ar em 11/12/2026, portanto disponível na Parte IV) |
| Parâmetros | `reasoning.effort = medium`, explícito em toda chamada; demais no padrão, todos registrados |
| Amostra e limiar | ≥20 itens por métrica julgada + itens sem maioria; κ ≥ 0,61 |
| κ abaixo do limiar | Métrica rotulada exploratória; J com ressalva e humano ao lado; D16 com humano primário; nada trocado após ver dados |

### 1.6 Plano de análise
| Decisão | Registro |
|---|---|
| Par principal por RF | Só fases `IMPL` + `VALID`; `ESPEC` comparada no nível do ciclo (R3-Q8) |
| Censura | Unidade no teto entra com o valor do teto, marcada; sensibilidade sem os censurados (R3-Q9) |
| Zeros no Wilcoxon | Método de Pratt (R7-Q21) |

---

## 2. Decisões de protocolo P1–P14 (Fase 1)

### P1 — Modelo *(22/09/2026, `GATE-C04`)*
`claude-sonnet-5` no campo `model` do `settings.json` único dos dois ciclos. ID canônico e fixo (desde a geração 4.6, IDs sem data são snapshots, não aliases). Alias `sonnet` proibido. Claude Code ≥ v2.1.197.

### P1b — Raciocínio *(22/09/2026, `GATE-C04`)*
Esforço `high`, fixado por `CLAUDE_CODE_EFFORT_LEVEL=high` no `env` do `settings.json` (prevalece sobre `effort` em frontmatter de skills e subagentes). `alwaysThinkingEnabled: true`. Proibidos nas sessões medidas: `ultrathink`, `Option+T`, `/effort`, `/model`.

### P1c — Subagentes e tarefas de fundo *(22/09/2026, `GATE-C04`)*
`CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5` + `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`. Tarefas de fundo: `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001`. Verificação no `GATE-C21` pelo campo `model` dos transcripts de subagentes; falha vira ameaça registrada.

### P2 — Superfície *(22/09/2026, `GATE-C05`, contra a recomendação)*
Extensão do Claude Code no VS Code, nos dois ciclos; Xcode só como simulador. `abrir-ciclo <a|b>` abre o VS Code no repositório do ciclo com `CLAUDE_CONFIG_DIR` do ciclo. Versões do VS Code e da extensão travadas; atualização automática de extensões desligada. **Antes de cada mensagem:** fechar todos os editores e desligar o anexo de contexto (ícone de olho). Ocorrências de contexto injetado contadas em `n_msgs_contexto_ide`.

### P3 — Permissões *(22/09/2026, `GATE-C05`)*
Allowlist idêntica nos dois ciclos, no `settings.json` único, incluindo o comando que executa o script de coleta. Pedido de permissão aprovado **só daquela vez**; "não perguntar de novo" proibido. Aprovar não é intervenção; negar é `INTERVENÇÃO [permissão negada]`.

### P4 — Sessões e contexto *(22/09/2026, `GATE-C05`, contra a recomendação)*
Spec Kit: **uma sessão por comando** (`constitution`, `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`). BMAD: uma sessão por workflow. Correções após a verificação: sessão nova aberta pela mensagem `INTERVENÇÃO [correção|…]` (forma no BMAD confirmada no `GATE-C10`). Compactação automática permitida e registrada; `/clear` proibido; comando interrompido continua numa sessão nova com o mesmo comando. Divergência em relação à §8.3 dos requisitos: ver seção 7.

### P5 — Edição manual *(22/09/2026, `GATE-C05`)*
Proibida como rotina. Quando inevitável: `INTERVENÇÃO [edição manual|N1 ou N2|causa]`, seguida de mensagem que descreve o que foi editado. Editar no editor do VS Code é edição manual.

### P5b — Mensagens neutras *(22/09/2026, `GATE-C01` R2)*
Sem prefixo só: confirmação a uma pausa espontânea do agente, fora da lista de gatilhos; colar a saída de um erro que o agente pediu. Resposta a pausa prevista pela metodologia leva `PROCESSO:`. Qualquer outra mensagem livre é intervenção.

### P5c — Tempo ativo *(22/09/2026, `GATE-C05`)*
Intervalos que terminam numa ação do agente contam inteiros; esperas pelo pesquisador contam até 30 min cada; excedente em `pausa_s`; tempo bruto também gravado. A timebox usa o tempo ativo.

### P6 — RF concluído *(22/09/2026, `GATE-C06`)*
Os quatro juntos: (a) o agente declara pronto (Spec Kit: o `converge` reporta *Converged*; BMAD: code review aprova a última story da unidade); (b) `flutter analyze` sem erros; (c) testes do próprio agente passam; (d) o pesquisador percorre no simulador os critérios de aceite da §1 dos requisitos do pacote. A suíte hold-out não entra.

### P7 — Timebox *(22/09/2026, `GATE-C06`)*
8 h de tempo ativo por RF; 12 h na F000; soma de todas as sessões da unidade, inclusive correções. Estourado: tag `rfNN-incompleto`, `timebox_censurado`, ciclo segue; dependentes são tentados, com o bloqueio registrado. Faixas exibidas pela coleta: <50%, 50–80%, >80%, atingido.

### P8 — Stack *(22/09/2026, `GATE-C06`)*
**Fixo:** Flutter e Dart na versão travada (via fvm); `flutter_bloc`; Clean Architecture em três camadas; `fpdart` (`Either<Failure, T>`); `mocktail`; `whisper_ggml`; `design_tokens.dart` como fonte única de tokens visuais; Voyage `voyage-4`; iOS; convenção de pastas `lib/core/` + `lib/features/<feature>/{data,domain,presentation}/`. **Livre:** roteamento, cliente HTTP, cache local, injeção de dependência, armazenamento seguro, biometria, gráficos.

### P9 — Granularidade e ordem *(22/09/2026, `GATE-C06`)*
Uma unidade por RF, antecedida da F000: F000 → RF03 → RF01 → RF02 → RF07 → RF06 → RF04 → RF10 → RF08 → RF05 → RF09. Forçados: RF10 depois de RF01 e RF04; RF08 depois de RF04. Ordem no pacote de entrada, igual nos dois ciclos.

### P10 — Telas de extensão *(22/09/2026, `GATE-C06`)*
Não são construídas (requisitos §2: "não recebem implementação funcional em nenhum dos dois ciclos"). Placeholders de menu aceitos. Se o agente começar a construir uma: uma `INTERVENÇÃO [redirecionamento|prd]` apontando a §2. Estados das telas de extensão fora da M9.

### P11 — Plataforma e dispositivo *(22/09/2026, `GATE-C06`)*
Só iOS. Simulador de um único modelo, com dimensões lógicas iguais às dos frames do protótipo — modelo escolhido a partir do HTML (`C-006`) e travado no `GATE-C15`; o mesmo para desenvolvimento e avaliação, em instâncias separadas (`sim-dev`, `sim-eval`). Android fora. Limites do simulador: sem câmera (foto do RF01 pela galeria), Face ID pelo menu Features, microfone do Mac.

### P12 — Idioma *(22/09/2026, `GATE-C06`, contra a recomendação)*
**Inglês** para prompts, pacote de entrada, artefatos das metodologias, respostas `PROCESSO:`, RDR e código. **Textos de interface em português**, literais do protótipo. O pacote de entrada é tradução fiel dos documentos-fonte (conferida no `GATE-C13`); endpoints, códigos de erro, IDs e tokens não são traduzidos. Os marcadores `INTERVENÇÃO` e `PROCESSO:` ficam em português, como tokens fixos, com o corpo da mensagem em inglês. Instalador do BMAD configurado em inglês.

### P13 — Cobrança *(22/09/2026, `GATE-C07`, contra a recomendação)*
Assinatura, o mesmo plano nos dois ciclos; plano e limites vigentes registrados no início de cada ciclo. Sessão cortada por limite de uso ou falha: coletada no terminal pelo script em modo `manual` (`motivo_fim`), e retomada numa sessão nova com o mesmo comando. M3 em USD sempre pela tabela de preços congelada.

### P14 — Cronograma *(22/09/2026, `GATE-C07`)*
| Etapa | Datas |
|---|---|
| Parte I (Fases 0–7 + congelamento) | 23/09 a 30/09 |
| Ciclo A | 01/10 a 21/10 |
| Transição A → B | 22/10 |
| Ciclo B | 23/10 a 13/11 |
| Trilha paralela do harness | 01/10 a 06/11 (corte da hold-out e da M8b: 06/11) |
| Parte IV — Avaliação | 14/11 a 20/11 |

Condição: capítulos da monografia sem dependência de dados são escritos durante os ciclos.

## 3. Regras operacionais (fonte única)

Regras de conduta do pesquisador durante os ciclos. O documento de métricas (§9) traz só as regras que afetam os dados e remete para cá.

### 3.1 Antes e durante cada sessão
1. Abrir toda sessão com `abrir-ciclo <a|b>`; nunca abrir `cerne-avaliacao` numa sessão medida.
2. **Antes de cada mensagem:** fechar todos os editores do VS Code e desligar o anexo de contexto (P2).
3. Uma sessão por comando do Spec Kit, uma por workflow do BMAD; nunca `/clear`; nunca rodar dois comandos ou workflows na mesma sessão (P4).
4. Nunca usar `ultrathink`, `Option+T`, `/effort` ou `/model` (P1b).
5. Pedido de permissão: aprovar só daquela vez; nunca "não perguntar de novo"; negar é `INTERVENÇÃO [permissão negada]` (P3).
6. Última ação: `/coletar-sessao <ID>`; depois, fechar a sessão e nunca retomá-la. Sessão cortada por limite de uso ou falha: coleta no terminal, modo `manual` (P13).

### 3.2 O que escrever ao agente
7. Sem prefixo, só: confirmação a uma pausa espontânea do agente; colar a saída de um erro que ele pediu (P5b).
8. Resposta a uma pausa prevista pela metodologia (lista de gatilhos, seção 4): começa com `PROCESSO:`.
9. Qualquer outra mensagem é intervenção, com `INTERVENÇÃO [tipo|campos]:` (seção 1.3).
10. Em correções, **descrever o sintoma, nunca a solução**: o que se esperava, o que aconteceu, onde (tela e ação) e a mensagem de erro, se houver. Nunca indicar arquivo, classe, biblioteca ou abordagem.
11. Se o agente começar a construir uma tela de extensão: uma `INTERVENÇÃO [redirecionamento|prd]` apontando a §2 dos requisitos (P10).

### 3.3 Fora das sessões
12. Não editar código nem artefatos. Se inevitável: `INTERVENÇÃO [edição manual|N1 ou N2|causa]` e mensagem descrevendo a edição (P5).
13. Verificação de "concluído" fora de sessão, pelos quatro critérios da P6. Correção: sessão nova aberta pela mensagem `INTERVENÇÃO [correção|Sn|causa]:`.
14. Timebox: acompanhar a faixa exibida pela coleta; no teto, `rf-incompleto <ID>` e seguir (P7).
15. Não consultar números de sessão (tokens, tempo, custo) nem rodar métricas de produto antes do fim do Ciclo B (cegamento).

### 3.4 Respostas às metodologias (`GATE-C11`)
16. Toda resposta a uma pausa prevista (seção 4.5) começa com `PROCESSO:` e é escrita em inglês.
17. Responder **só com o que está no pacote de entrada**, citando a seção.
18. Se o pacote não cobre, consultar o RDR (`docs/rdr.md`); se o RDR cobre, usar **o mesmo texto**.
19. Se nem o pacote nem o RDR cobrem: decidir na hora, responder com uma frase curta e acrescentar a decisão ao RDR (data, ciclo, pergunta, resposta).
20. Pergunta de preferência ("A ou B?"): "Use your technical judgment, following the input package."
21. `bmad-sprint-planning`: CONCERNS → seguir; FAIL → rodar a skill que o achado indica.
22. Elicitação avançada e party mode (BMAD): aceitar quando oferecidos; a escolha é livre, mas cada uma vai para o RDR (método escolhido; melhorias aceitas e descartadas).
23. Brainstorming e forge-idea (BMAD): contribuir só com o conteúdo do pacote; quando a ferramenta pedir mais ideias do que o pacote tem, dizer isso ("The input package does not cover further ideas.") e registrar no RDR.

### 3.5 Artefatos das metodologias (`GATE-C12`)
24. Nunca editar à mão `CLAUDE.md`, `AGENTS.md`, `.specify/`, `specs/`, artefatos do BMAD ou `sprint-status.yaml`. Se editar: `INTERVENÇÃO [edição manual|N1 ou N2|causa]`.
25. Branches e commits seguem cada metodologia. Ao declarar a unidade concluída, `concluir-rf` faz o merge em `main` (se a metodologia não fizer) e cria a tag; isso não é intervenção.

## 4. Regras por metodologia (Fase 2)

Critério geral: seguir o fluxo da documentação oficial da versão travada, sem extensões, presets, bundles, módulos extras ou agentes da comunidade. As escolhas além do fluxo mínimo (opcionais do Spec Kit; BMAD completo) estão registradas nos `GATE-C09` e `C10` do plano.

### 4.1 Versões e instalação (`GATE-C08`)
| | Spec Kit | BMAD-METHOD |
|---|---|---|
| Versão | **v1.0.10** (22/09/2026) | **v6.11.0** (10/08/2026) |
| Instalação | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.10` | `npx bmad-method@6.11.0 install --directory <repo> --modules bmm --tools claude-code --yes` + `--set` de idioma (inglês), chaves conferidas com `--list-options bmm` |
| Inicialização | `specify init --here --force --non-interactive --integration claude` | — (a instalação já configura) |
| Modo no Claude Code | Padrão da versão para `claude` (registrado na instalação) | Skills em `.claude/skills/` |
| Versões posteriores | Não adotadas | Corte da v7 não adotado |

### 4.2 Sequência do Ciclo A — Spec Kit (`GATE-C09`)
1. **Setup (`SETUP`):** `/speckit.constitution` com `P-SETUP`.
2. **Por unidade (F000, RF03, RF01, RF02, RF07, RF06, RF04, RF10, RF08, RF05, RF09), uma sessão por comando:**
   1. `/speckit.specify` com o prompt da unidade
   2. `/speckit.clarify`
   3. `/speckit.checklist`
   4. `/speckit.plan` com `P-TECH`
   5. `/speckit.tasks`
   6. `/speckit.analyze`
   7. `/speckit.implement`
   8. `/speckit.converge`
   9. Se o `converge` não reportar *Converged*: voltar ao passo 7 (laço `implement` → `converge`).
3. **Verificação de concluído** (P6), fora de sessão; correções em sessão aberta por `INTERVENÇÃO [correção|…]`.

### 4.3 Sequência do Ciclo B — BMAD (`GATE-C10`)
1. **B1 Setup (`SETUP`):** instalação por flags → `bmad-project-context` com `P-SETUP`.
2. **B2 Análise (`PLAN`):** `bmad-brainstorming` → `bmad-forge-idea` → `bmad-deep-recon` → `bmad-prfaq` → `bmad-product-brief`.
3. **B3 Planejamento (`PLAN`):** `bmad-prd` (criar) → `bmad-prd` (validar) → `bmad-ux` (fonte: protótipo congelado, sem alterá-lo).
4. **B4 Solução (`PLAN`):** `bmad-architecture` → `bmad-create-epics-and-stories` → `bmad-sprint-planning` (portão de prontidão e `sprint-status.yaml`). Tag `cicloB/plan-done`. Timebox de B2–B4: 32 h de tempo ativo.
5. **Mapa de stories:** `dados/cicloB/mapa-stories.csv` (story → unidade).
6. **B5 Implementação, por story, uma sessão por skill:** `bmad-build` → `bmad-code-review` → `bmad-qa-generate-e2e-tests`. Ao fim de cada épico: `bmad-retrospective` (`PLAN`, fora da timebox de B2–B4). `bmad-correct-course` só em mudança grande.
7. **Verificação de concluído** por unidade (P6), fora de sessão; correções em sessão aberta por `INTERVENÇÃO [correção|…]`.
8. **Fora do fluxo:** `bmad-spec`, `bmad-preview-ticketing` (prévia da v7), `bmad-walkthrough`, `bmad-build-auto`, `bmad-shard-doc`, módulos TEA/CIS/BMB.

### 4.4 Tabela comando/workflow → fase (M2, M3, M5; `segmentos.csv`)
Mensagens sem marcador herdam a fase do marcador anterior. Sessões de correção abertas por intervenção: `IMPL`.

| Spec Kit | Fase | BMAD | Fase |
|---|---|---|---|
| `constitution` | `ESPEC` | `bmad-project-context` | `ESPEC` |
| `specify` | `ESPEC` | `bmad-brainstorming`, `bmad-forge-idea`, `bmad-deep-recon`, `bmad-prfaq`, `bmad-product-brief` | `ESPEC` |
| `clarify` | `ESPEC` | `bmad-prd` (criar), `bmad-ux` | `ESPEC` |
| `checklist` | `VALID` | `bmad-prd` (validar) | `VALID` |
| `plan` | `ESPEC` | `bmad-architecture`, `bmad-create-epics-and-stories` | `ESPEC` |
| `tasks` | `ESPEC` | `bmad-sprint-planning` | `VALID` |
| `analyze` | `VALID` | `bmad-correct-course` | `ESPEC` |
| `implement` | `IMPL` | `bmad-build` | `IMPL` |
| `converge` | `VALID` | `bmad-code-review`, `bmad-qa-generate-e2e-tests`, `bmad-retrospective` | `VALID` |

### 4.5 Gatilhos `PROCESSO` (série M5b)
**Definição operacional (congelada):** é gatilho toda pausa em que um comando ou skill da metodologia, pelo seu próprio texto na versão travada, pede ao usuário uma resposta, escolha, confirmação ou aprovação. A resposta a um gatilho leva `PROCESSO:`. Pausa espontânea do agente, fora disso, não é gatilho (P5b).

**Lista esperada, pelos documentos das versões travadas** (conferida contra o texto dos comandos e skills instalados na Fase 4; item novo encontrado na conferência entra pela definição acima e é registrado aqui):

| Framework | Comando/skill | Pausa |
|---|---|---|
| Spec Kit | `constitution` | Pedido de valores que o prompt não trouxe |
| | `specify` | Perguntas de esclarecimento sobre marcações de ambiguidade |
| | `clarify` | Perguntas sequenciais de esclarecimento |
| | `checklist` | Perguntas sobre foco e escopo do checklist |
| | `analyze` | Oferta de sugerir correções para os problemas encontrados |
| | `implement` | Confirmação para seguir com checklists incompletos |
| | `converge` | Confirmação para acrescentar o trabalho restante como tarefas, se pedida |
| BMAD | `bmad-project-context` | Regras que o usuário quer seguidas |
| | `bmad-brainstorming`, `bmad-forge-idea` | Perguntas e pedidos de ideias ao usuário |
| | `bmad-deep-recon` | Escolha do modo e do tipo de pesquisa |
| | `bmad-prfaq`, `bmad-product-brief`, `bmad-prd`, `bmad-ux`, `bmad-architecture`, `bmad-create-epics-and-stories` | Perguntas de descoberta; menus de continuar; oferta de elicitação avançada e party mode; aprovação de seções |
| | `bmad-prd` | Pergunta de intenção (criar, atualizar, validar) |
| | `bmad-sprint-planning` | Seguir ou não com CONCERNS |
| | `bmad-build` | Parada quando não consegue fixar a intenção |
| | `bmad-code-review` | Triagem dos achados |
| | `bmad-retrospective` | Aceitar ou não o épico; discussão opcional |
| | `bmad-correct-course` | Aprovação da proposta de mudança |

### 4.6 Pendências verificadas na Fase 4 (com as metodologias instaladas)
- Spec Kit: modo de integração padrão para o Claude Code; notas de versão 1.0.4–1.0.5 e 1.0.7–1.0.10 (`C-010`); texto dos comandos contra a seção 4.5.
- BMAD: nomes exatos das skills (`.claude/skills/`, `bmad-help`); chaves de idioma do `--set`; se o `bmad-project-context` grava no `AGENTS.md` e se o Claude Code lê esse arquivo; formato das stories (efeito na `M6_tasks`, `C-022`); nenhuma definição de agente com modelo próprio (neutralizada pelo `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, P1c); texto das skills contra a seção 4.5.

## 5. Tabela de entrega dos prompts (Fase 3, `C-009`)

Nunca entra no pacote. Decidida em 22/09/2026 (R24).

| Prompt | Ciclo A — Spec Kit | Ciclo B — BMAD |
|---|---|---|
| `P-SETUP` | Argumento do `/speckit.constitution` (A1) | Regras do `bmad-project-context` no setup (B1) |
| `P-GLOBAL` | Anexado ao `P-F000` no primeiro `/speckit.specify` | Argumento do `bmad-brainstorming` (primeira skill de análise). As demais skills de análise são chamadas sem argumento; quando perguntam de onde partir, a resposta vem do pacote, com `PROCESSO:` e texto fixado no RDR |
| `P-F000`, `P-RF01`…`P-RF10` | Argumento do `/speckit.specify` da unidade, uma por vez, na ordem da P9 | Todos de uma vez, na ordem da P9, como entrada do `bmad-prd` (criar). O `bmad-build` recebe só a story, sem reenviar o `P-RFxx` |
| `P-TECH` | Argumento do `/speckit.plan` de toda unidade | Primeira mensagem do `bmad-architecture` (uma vez) |
| — | `clarify`, `checklist`, `tasks`, `analyze`, `implement`, `converge`: sem argumento | `bmad-prd` (validar), `bmad-ux`, `bmad-create-epics-and-stories`, `bmad-sprint-planning`, `bmad-code-review`, `bmad-qa-generate-e2e-tests`, `bmad-retrospective`: sem argumento além do que a própria skill pede |

**Diferença de método, não de informação:** o BMAD recebe todos os `P-RFxx` no planejamento, e o Spec Kit um por vez. O `requirements.md` completo está no repositório dos dois desde o início. Declarar na monografia.

### 5.1 Composição do pacote de entrada (`C-005`–`C-008`, 23/09/2026)
| Item | Decisão |
|---|---|
| Local nos ciclos | `docs/input/` (em `cerne-avaliacao`: `entrada/`) |
| Idioma | Inglês; textos de interface em português, literais (P12) |
| Protótipo | Cópia derivada do HTML congelado, com a linha que citava o TCC e as metodologias neutralizada. Original `61032a92…185d2fff` fica em `cerne-avaliacao` para a M9. Hash do derivado: *(terminal)* |
| Requisitos | Tradução neutra dos requisitos reconciliados `a62d8439…3db0` |
| Backend | Handoff traduzido e neutralizado; `openapi.yaml` com só os textos traduzidos (estrutura verificada idêntica) |
| Fixtures | Áudio, 2 imagens de OCR, transcrição esperada, 3 textos semeados; fora `textos.json`, D16, roteiro, testes de contrato, credenciais |
| Prompts | Fora do pacote: `cerne-avaliacao/prompts/`, colados no chat pela tabela de entrega; hash à parte (R27) |
| Complexidade | Limiar da M12 fora dos requisitos do pacote (sem requisito de produto correspondente; R27) |
| Tela 6 | Inteira na unidade RF09: dashboard, nome, "Sair", "Apagar conta" (RNF05) (R27) |
| Simulador (P11) | Frame 390×844 → candidatos iPhone 16e / iPhone 14; escolha no `GATE-C15` |
| Hash do pacote | *(terminal, `GATE-C13`)* |

## 6. Ambiente (Fase 4)
*A preencher (`GATE-C14`, `C-010`–`C-013`).*

## 7. Divergências em relação aos documentos-fonte

Decisões que contrariam o texto de um documento-fonte, tomadas antes do congelamento e declaradas na monografia.

| # | Documento-fonte | O que diz | Decisão | Onde | Data |
|---|---|---|---|---|---|
| 1 | Requisitos §3 (RNF09) | 15 cenários de falha testados com `mocktail`, escritos pelo agente | Medidos pela suíte hold-out (caixa-preta); `mocktail` do agente como dado secundário | Métricas v1.0, M10 | já na v2 |
| 2 | Requisitos §8.2 | Complexidade via DCM ou fork do `dart_code_metrics` | CLI Dart próprio sobre a AST, regra de McCabe documentada | Métricas v1.0, M12; `GATE-C02` item 2 | 22/09/2026 |
| 3 | Requisitos §8.3 | Contraste "pipeline de agente único (Spec Kit) × fluxo com reset de contexto entre fases (BMAD)"; M14 mede perda de contexto entre fases | Reset de contexto a cada fase nos dois ciclos (P4); hipótese reformulada para fidelidade do handoff mediado por artefatos | P4; Métricas v1.0, M14, §5.6, §12 | 22/09/2026 |
| 4 | Requisitos §10 | Voyage `voyage-3` ou `voyage-4` | `voyage-4`, fixo pelo backend | Pacote de entrada (`C-005`) | plano |
| 5 | `doc-prototipo.md` (abertura) | App Flutter para iOS e Android | Desenvolvimento e avaliação só no iOS (P11) | P11 | 22/09/2026 |

## 8. Especificação da avaliação (Fase 7)

| Item | Decisão | Data |
|---|---|---|
| Fontes das decisões da M14 | Spec Kit: constitution + `plan.md` da F000; BMAD: arquitetura | 24/09/2026 (R29) |
| Convenções da M15 | Referência na feature do RF01; C1 subpastas, C2 sufixo de repositório, C3 nome de falha, C4 nomes de BLoC/evento/estado | 24/09/2026 (R29) |
| Injeção de falhas da hold-out | Cabeçalho `X-Test-Fault` posto pelo proxy, efeito executado pelo backend (determinístico, com log) | 24/09/2026 (R30) |
| Escala de severidade `Sn` (D16) | S1 cosmético · S2 funcional com contorno · S3 bloqueante | 24/09/2026 (R30) |
| `M6_tasks` no Ciclo B sem checkboxes | % de stories `done` no `sprint-status.yaml`, declarado como granularidade mais grossa | 24/09/2026 (R30) |
| Tabela de preços da M3 | `harness/precos.md` (consulta de 24/09/2026) | 24/09/2026 |

