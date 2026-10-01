# Protocolo experimental — Ciclos comparativos (app Cerne)

**Destino:** `cerne-avaliacao/docs/protocolo.md`
**Documento cumulativo.** Cada fase da Parte I do `plano-ciclos.md` acrescenta suas decisões. Congelado com hash no `GATE-C23` (tag `protocolo-v1.0`); depois disso, toda mudança passa por `docs/desvios.md`.
**Documento irmão:** `Metricas_e_Skills_Ciclos.md` v1.0 — o que é medido e como. Este protocolo diz **como o experimento é conduzido**, e é a fonte única das regras operacionais de conduta (Métricas v1.0, §9).

| Fase | Situação |
|---|---|
| 0 — Instrumento de medição | Concluída em 24/09/2026 |
| 1 — Protocolo (P1–P14) | Decidida em 22/09/2026 (`GATE-C04`–`C07`; `C-003`) |
| 2 — Regras por metodologia | Decidida em 22/09/2026 (`GATE-C08`–`C12`; `C-004`); notas de versão lidas em 24/09/2026 |
| 3 — Pacote de entrada e tabela de entrega | Concluída em 24/09/2026 (`C-005`–`C-009`; `GATE-C13` com hashes) |
| 4 — Ambiente | `GATE-C14`–`C16` concluídos em 27/09/2026 (pivô de simulador para iPhone 16 Pro físico no `GATE-C16`); `C-024` (isolamento dev/avaliação) escrito, verificação de rede pendente |
| 5 — Repositórios, credenciais e ambientes de backend | Concluída em 29/09/2026 (`GATE-C17`–`C-015`) |

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

### P11 — Plataforma e dispositivo *(22/09/2026, `GATE-C06`; revisado 27/09/2026, `GATE-C16`)*
Só iOS. Simulador de um único modelo, com dimensões lógicas iguais às dos frames do protótipo — modelo escolhido a partir do HTML (`C-006`) e travado no `GATE-C15`; o mesmo para desenvolvimento e avaliação, em instâncias separadas (`sim-dev`, `sim-eval`). Android fora. Limites do simulador: sem câmera (foto do RF01 pela galeria), Face ID pelo menu Features, microfone do Mac.

**Revisão (27/09/2026, achado do `GATE-C16`):** o `whisper_ggml` (P8) não roda no simulador iOS — limitação documentada do FFmpeg que ele empacota, confirmada em pesquisa externa, não é peculiaridade desta máquina. Decisão: **dispositivo físico único, iPhone 16 Pro do Wagner, para os dois ciclos inteiros** (não só para RF02) — substitui o simulador por completo. Frame do HTML (390×844, iPhone 16e/14) superado pelas dimensões reais do iPhone 16 Pro (402×874 pts); tratado como desvio (seção 7, item 6), não como reabertura da escolha de modelo do `GATE-C15`. Câmera real disponível agora (não precisa mais da galeria para a foto do RF01 — ver se isso muda alguma decisão de unidade). Face ID: biometria real do aparelho, não mais simulada pelo menu Features. Microfone: do próprio iPhone, não mais do Mac. Isolamento dev/avaliação (antes `sim-dev`/`sim-eval` como duas instâncias separadas): como só há um aparelho físico, vira um procedimento de reset manual entre fases (`C-024`).

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
| Instalação | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.0.10` | `npx bmad-method@6.11.0 install --directory <repo> --modules bmm --tools claude-code --yes` + idioma inglês via `--communication-language`/`--document-output-language` (flags do `install`, não chave de `--set`; correção de 25/09/2026 — ver `GATE-C14`/Fase 4 abaixo) |
| Inicialização | `specify init --here --force --non-interactive --integration claude` | — (a instalação já configura) |
| Modo no Claude Code | Padrão da versão para `claude` (registrado na instalação) | Skills em `.claude/skills/` |
| Versões posteriores | Não adotadas | Corte da v7 não adotado |

### 4.2 Sequência do Ciclo A — Spec Kit (`GATE-C09`)
*Nomes dos comandos corrigidos em 25/09/2026 (Fase 4): a versão instalada usa hífen (`/speckit-constitution`), não ponto (`/speckit.constitution`, forma antiga usada por engano nas Fases 0–2 deste documento e no `plano-ciclos.md`).*
1. **Setup (`SETUP`):** `/speckit-constitution` com `P-SETUP`.
2. **Por unidade (F000, RF03, RF01, RF02, RF07, RF06, RF04, RF10, RF08, RF05, RF09), uma sessão por comando:**
   1. `/speckit-specify` com o prompt da unidade
   2. `/speckit-clarify`
   3. `/speckit-checklist`
   4. `/speckit-plan` com `P-TECH`
   5. `/speckit-tasks`
   6. `/speckit-analyze`
   7. `/speckit-implement`
   8. `/speckit-converge`
   9. Se o `converge` não reportar *Converged*: voltar ao passo 7 (laço `implement` → `converge`).
3. **Verificação de concluído** (P6), fora de sessão; correções em sessão aberta por `INTERVENÇÃO [correção|…]`.
4. **Fora do fluxo:** `speckit-taskstoissues` (converte tasks em issues do GitHub; existe na instalação, não é usado — achado de 25/09/2026, Fase 4).

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
| | `converge` | ~~Confirmação para acrescentar o trabalho restante como tarefas, se pedida~~ — **não é gatilho na v1.0.10** (correção de 25/09/2026, Fase 4): o texto do comando instalado só imprime um resumo dos achados antes de gravar (“no file writes yet”), sem nenhum “ask the user” antes de acrescentar as tarefas em `tasks.md`. Não conta como `PROCESSO:` pela definição operacional acima. |
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
- Spec Kit: modo de integração padrão para o Claude Code; texto dos comandos contra a seção 4.5. (Notas de versão 1.0.0–1.0.10 lidas em 24/09/2026, sem mudança de fluxo; a v1.0.11, de 24/09/2026, não é adotada.)
- BMAD: nomes exatos das skills (`.claude/skills/`, `bmad-help`); chaves de idioma do `--set`; se o `bmad-project-context` grava no `AGENTS.md` e se o Claude Code lê esse arquivo; formato das stories (efeito na `M6_tasks`, `C-022`); nenhuma definição de agente com modelo próprio (neutralizada pelo `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, P1c); texto das skills contra a seção 4.5.

**Registro (25/09/2026) — conferência textual em diretórios descartáveis (fora de `cerne-avaliacao`, nunca a instalação definitiva do `C-010`/B0):**
- Spec Kit v1.0.10 instalado via `uv tool install` + `specify init --here --force --non-interactive --integration claude` (flag confirmada correta). Comandos reais usam **hífen**: `/speckit-constitution`, `/speckit-specify`, `/speckit-clarify`, `/speckit-checklist`, `/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge` — corrigido nas seções 4.2 e 5 (a forma com ponto não existe no CLI instalado). `clarify`/`analyze`/`checklist` confirmados "optional" pelo próprio CLI. `implement` e `analyze` confirmados como gatilhos reais (texto citado na seção 4.5). `converge` **não** confirmado como gatilho — corrigido na 4.5. Skill extra fora do fluxo: `speckit-taskstoissues` — registrada na 4.2.
- BMAD v6.11.0 instalado via `npx bmad-method@6.11.0 install --directory . --modules bmm --tools claude-code --yes` (49 skills → `.claude/skills`). `--list-options bmm` só lista `bmm.user_skill_level`, `bmm.planning_artifacts`, `bmm.implementation_artifacts`, `bmm.project_knowledge` — **nenhuma é de idioma**; idioma é `--communication-language`/`--document-output-language`, flags do próprio `install` — corrigido na 4.1. `bmad-project-context` confirmado pela descrição da skill: grava um bloco verificado dentro de `AGENTS.md`. `bmad-prd` confirmado como skill única com detecção de intenção Create/Update/Validate (pergunta se ambíguo) — bate com a 4.5. Nenhum `SKILL.md` das 49 skills declara `model:` no frontmatter (grep vazio) — confirma "nenhuma definição de agente com modelo próprio", sem precisar do `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` para neutralizar nada nas skills em si.
- **Demais skills conferidas contra a seção 4.5, texto real batendo com a tabela:** `bmad-sprint-planning` (gate `PASS`/`CONCERNS`/`FAIL`, literal); `bmad-code-review` (descrição: "structured triage" — bate com "Triagem dos achados"); `bmad-retrospective` (verdict de aceitação do épico com fail-safe na Fase 4 do workflow, discussão de "going-in concerns" opcional); `bmad-correct-course` ("Get explicit user approval for complete proposal", literal); `bmad-deep-recon` (escolha explícita Run/Draft + tipo de pesquisa inferido, confirmado só se ambíguo); `bmad-brainstorming`/`bmad-forge-idea` (perguntas abertas de descoberta, confirmação de premissas); `bmad-architecture` (escolha Coaching/Fast path como passo de ativação, decisões estruturais "shown, not silently made").
- **Achado importante (25/09/2026):** o Claude Code só lê `AGENTS.md` automaticamente a partir da **v2.1.277** (antes disso, ignora o arquivo por completo), e mesmo a partir daí só se **não existir `CLAUDE.md`** na hierarquia do projeto (senão `CLAUDE.md` prevalece, a menos que `claude-md-and-agents-md` seja configurado em "Project instructions"). Fonte: documentação oficial (`memory.md`, seção "AGENTS.md"). Nem o instalador do Spec Kit nem o do BMAD criam `CLAUDE.md`/`AGENTS.md` sozinhos (conferido nos dois diretórios descartáveis — só `.claude/skills/`); o `AGENTS.md` só nasce quando `bmad-project-context` roda de verdade. **Isto afeta o `C-011`:** a versão mínima ali travada é "≥ v2.1.197" — abaixo de v2.1.277, o bloco que o `bmad-project-context` grava em `AGENTS.md` no B1 simplesmente não seria lido pelo Claude Code, e a suposição do protocolo (que o Claude Code lê esse arquivo) ficaria falsa sem nenhum aviso. Preciso que o Wagner trave o `C-011` em **≥ v2.1.277**, não só "≥ v2.1.197", e confirme que nenhum `CLAUDE.md` pessoal/do projeto sobra em `cfg-ciclo-b` nem no repositório do Ciclo B.
- **Ainda em aberto desta conferência:** `bmad-build` ("Parada quando não consegue fixar a intenção" da 4.5 — só achei HALT por falha do `uv`, não por intenção ambígua; precisa de leitura mais funda do `SKILL.md` ou de um teste real); `bmad-create-epics-and-stories` (nenhuma menção a elicitação/party mode/aprovação de seção encontrada por palavra-chave — pode ser texto diferente do esperado, não necessariamente ausência); `bmad-prfaq`/`bmad-product-brief`/`bmad-ux` (confirmados quanto a perguntas de descoberta, mas não especificamente quanto a "oferta de elicitação avançada e party mode"); formato real das stories geradas por `bmad-create-epics-and-stories` (só dá para confirmar rodando de verdade, não só lendo o `SKILL.md`).

## 5. Tabela de entrega dos prompts (Fase 3, `C-009`)

Nunca entra no pacote. Decidida em 22/09/2026 (R24).

| Prompt | Ciclo A — Spec Kit | Ciclo B — BMAD |
|---|---|---|
| `P-SETUP` | Argumento do `/speckit-constitution` (A1) | Regras do `bmad-project-context` no setup (B1) |
| `P-GLOBAL` | Anexado ao `P-F000` no primeiro `/speckit-specify` | Argumento do `bmad-brainstorming` (primeira skill de análise). As demais skills de análise são chamadas sem argumento; quando perguntam de onde partir, a resposta vem do pacote, com `PROCESSO:` e texto fixado no RDR |
| `P-F000`, `P-RF01`…`P-RF10` | Argumento do `/speckit-specify` da unidade, uma por vez, na ordem da P9 | Todos de uma vez, na ordem da P9, como entrada do `bmad-prd` (criar). O `bmad-build` recebe só a story, sem reenviar o `P-RFxx` |
| `P-TECH` | Argumento do `/speckit-plan` de toda unidade | Primeira mensagem do `bmad-architecture` (uma vez) |
| — | `clarify`, `checklist`, `tasks`, `analyze`, `implement`, `converge`: sem argumento | `bmad-prd` (validar), `bmad-ux`, `bmad-create-epics-and-stories`, `bmad-sprint-planning`, `bmad-code-review`, `bmad-qa-generate-e2e-tests`, `bmad-retrospective`: sem argumento além do que a própria skill pede |

**Diferença de método, não de informação:** o BMAD recebe todos os `P-RFxx` no planejamento, e o Spec Kit um por vez. O `requirements.md` completo está no repositório dos dois desde o início. Declarar na monografia.

### 5.1 Composição do pacote de entrada (`C-005`–`C-008`, 23/09/2026)
| Item | Decisão |
|---|---|
| Local nos ciclos | `docs/input/` (em `cerne-avaliacao`: `entrada/`) |
| Idioma | Inglês; textos de interface em português, literais (P12) |
| Protótipo | Cópia derivada do HTML congelado, com a linha que citava o TCC e as metodologias neutralizada. Original `61032a92…185d2fff` fica em `cerne-avaliacao` para a M9. Hash do derivado: `aa8263b221d110a599f58877935152eba2fe5802a5b272c04d16ee84864cae0b` |
| Requisitos | Tradução neutra dos requisitos reconciliados `a62d8439…3db0` |
| Backend | Handoff traduzido e neutralizado; `openapi.yaml` com só os textos traduzidos (estrutura verificada idêntica) |
| Fixtures | Áudio, 2 imagens de OCR, transcrição esperada, 3 textos semeados; fora `textos.json`, D16, roteiro, testes de contrato, credenciais |
| Prompts | Fora do pacote: `cerne-avaliacao/prompts/`, colados no chat pela tabela de entrega; hash à parte (R27) |
| Complexidade | Limiar da M12 fora dos requisitos do pacote (sem requisito de produto correspondente; R27) |
| Tela 6 | Inteira na unidade RF09: dashboard, nome, "Sair", "Apagar conta" (RNF05) (R27) |
| Simulador (P11) | Frame 390×844 → candidatos iPhone 16e / iPhone 14; escolha no `GATE-C15` |
| Hash do pacote | `dd6eb964b2ff50a2ce72b8b2f3fb26e86866e584156c93b4805247225d8b71c2` — `find entrada -type f -not -name '.DS_Store' \| LC_ALL=C sort \| xargs -I{} shasum -a 256 "{}" \| shasum -a 256`, calculado pelo Wagner no terminal em 24/09/2026 e conferido contra o zip (`GATE-C13`) |
| Hash dos prompts | `d6e888c3ad18858fdc70dd202b5c537a98d22796ef31fd8b53f92f1728d91d8c` (mesma fórmula sobre `prompts/`) |

### 5.2 Hashes por arquivo do pacote (`GATE-C13`, 24/09/2026)

```text
85763596609724f6ffa2342e77f8046fc9f017a006b4c97591fdbff4a3b2a196  entrada/backend/README.md
82376248daf57648a46265bacfc9c337eba181f8df940cc65f659d350a925a02  entrada/backend/api/openapi.yaml
0c996614fa19930d97e8c56cfdea163b5a78177c18a83a0a8957c7ad00f0f5b0  entrada/backend/error-taxonomy.md
adff962fb13fb8e099fdeb485b227745513443361449e84e4c460ba40926ba66  entrada/backend/export-screen-states.md
b9302d2f886006853ec6daab840d87b2e3f483e29b55f4fcf9f37202d8193203  entrada/backend/fixtures/README.md
b833ed4f72c0f01354a1c5fcb2dd184408a654073e3ffaa64b8661aa5c18dd8b  entrada/backend/fixtures/expected-transcription.md
3ff3df21d186a8c2d300788bf53af2e2c70a1480a5941a640b94674a66584e1a  entrada/backend/fixtures/media/audio_fixture_01.wav
7ed3068dc0d2381259081a92feab4266867b5a0b89bb87925e0b5ed2025fc31d  entrada/backend/fixtures/media/ocr_fixture_01.png
0ed46c03c60f5428a4f645549a1c90b0256f3e81b609a6978c18f555d8efdbd8  entrada/backend/fixtures/media/ocr_fixture_ilegivel.png
957971e9a65de24311294a32a8638eb2883bd0407326f11fa29a4517a730e5da  entrada/backend/fixtures/seeded-search-entries.md
042adc95e16e8e224390c20cbd3a3e1dd56b0199e740b848967254ad90232f52  entrada/backend/known-bugs.md
5a83f0cc23f383a28fdf8abad93024d7dc74bcbeb8ce7fa4589a29e08211bda8  entrada/backend/sync-badge.md
aa8263b221d110a599f58877935152eba2fe5802a5b272c04d16ee84864cae0b  entrada/prototype/cerne-prototype.html
306004c7789dc1b8f798ea3d5a7a4cce456b7900ac139fdde3b6edcbd1995207  entrada/prototype/prototype-extract.md
6f7915d16617d60ebbd79195020f65e003a140efa51c4600cb3763ac4973c37b  entrada/requirements.md
```

## 6. Ambiente (Fase 4)

### 6.1 Máquina (`GATE-C14`)
| Item | Valor |
|---|---|
| Modelo | MacBook Pro (`MacBookPro18,3`) |
| Chip | Apple M1 Pro |
| Memória | 16 GB |
| macOS | 27.0 (build `26A428`) |

**Registro (25/09/2026):** dados coletados pelo Wagner via `system_profiler SPHardwareDataType` e `sw_vers`. O macOS não é atualizado entre o início do Ciclo A e o fim do Ciclo B (Apêndice — Erros comuns a evitar, `plano-ciclos.md`).

### 6.2 Ferramentas de linha de comando (`C-010`)
| Ferramenta | Versão travada |
|---|---|
| Flutter (via `fvm`) | 3.47.5 • channel stable |
| Dart | 3.13.4 |
| Node | v26.10.0 (LTS, para o instalador do BMAD) |
| uv | 0.12.19 |
| CocoaPods | 1.17.0 |
| Spec Kit CLI (`specify`) | 1.0.10 (`GATE-C08`) |

**Achado — Flutter sem versão fixa no plano:** `P8`/`C-010` diziam "a versão travada (via fvm)" sem nunca ter fixado um número. Decisão (25/09/2026): travar no **stable mais recente do dia** (mesmo critério do `GATE-C08` para o Spec Kit — "a mais recente estável no dia do congelamento"), resolvido para Flutter 3.47.5/Dart 3.13.4 via `fvm install stable && fvm global stable`.

**Achado — conflito de instalação do Spec Kit CLI:** a máquina tinha um `specify` instalado via **Homebrew** (`brew info specify`: mesmo projeto, mas a fórmula segue "stable" sem trava de tag — tinha puxado a v1.0.11, a versão **não adotada** citada na 4.6), na frente do `specify-cli` correto (instalado via `uv tool install --from git+.../spec-kit.git@v1.0.10`) no `PATH`. Corrigido com `brew uninstall specify`. Em seguida, `~/.local/bin` (diretório de binários do `uv tool`) não estava no `PATH` — o `uv tool update-shell` não escreveu em `~/.zshrc`; corrigido manualmente com `export PATH="$HOME/.local/bin:$PATH"`. Confirmado ao final: `specify` → `~/.local/bin/specify` → `1.0.10`. **Fica registrado para quem reproduzir o ambiente:** não instalar `specify` via Homebrew; usar só `uv tool install` com a tag travada.

**Registro (25/09/2026):** todas as seis versões acima conferidas por comando real, na máquina do Wagner (MacBook Pro, `GATE-C14`). BMAD **não** instalado globalmente — confirmado que só entra via `npx bmad-method@6.11.0` no B0, conforme o `C-010` original.

### 6.3 Xcode e simuladores (`GATE-C15`)
| Item | Valor |
|---|---|
| Xcode | 27.0 (build `27A266a`) |
| Runtime iOS | 27.0 (build `24A434`) |
| Modelo do simulador | iPhone 16e — escolhido entre os dois candidatos do P11/"Itens em aberto" (iPhone 16e vs. iPhone 14, ambos com frame 390×844); iPhone 16e por ser o aparelho atual da linha Apple, mais representativo de hardware corrente em 2026 |
| `sim-dev` (desenvolvimento, sem proxy) | UDID `37026B12-65F7-420A-9031-28576897CD1F` |
| `sim-aval` (avaliação, com certificado do mitmproxy) | UDID `A583D8DA-BC53-48A2-83CA-BE8E9B4FCA8C` — certificado do mitmproxy instalado só no `C-013` |

**Registro (25/09/2026):** os dois simuladores criados via `xcrun simctl create <nome> "iPhone 16e" "com.apple.CoreSimulator.SimRuntime.iOS-27-0"`, confirmados em estado `Shutdown` por `xcrun simctl list devices`.

**Revisão (27/09/2026, achado do `GATE-C16`):** `sim-dev`/`sim-aval` **substituídos** por um único **iPhone 16 Pro físico** (Wagner) para os dois ciclos inteiros — `whisper_ggml` não roda em simulador (ver P11, revisão 27/09/2026, e seção 7 item 6). Os dois simuladores continuam criados (não apagados), mas deixam de ser o ambiente de desenvolvimento/avaliação. Xcode/runtime seguem os mesmos, usados para parear o iPhone via cabo/wireless.

### 6.4 Claude Code, VS Code e diretórios de configuração (`C-011`)
| Item | Valor |
|---|---|
| Claude Code CLI | 2.1.282 (acima do piso `v2.1.277`) |
| Extensão Claude Code (VS Code) | 2.1.282 |
| VS Code | 1.139.1 |
| Diretórios de config | `~/cerne/cfg-ciclo-a`, `~/cerne/cfg-ciclo-b` (limpos, sem `CLAUDE.md`/skills/MCPs/plugins pessoais do repositório) |
| Script | `~/cerne/bin/abrir-ciclo <a|b>` — exporta `CLAUDE_CONFIG_DIR`, abre VS Code em janela própria |
| Atualização automática | Claude Code: `DISABLE_AUTOUPDATER` vai no `settings.json` do `C-012`. VS Code: `update.mode: none`. Extensões: `extensions.autoUpdate: false` |

**Achado — VS Code já instalado:** o cask do Homebrew recusou por já existir `/Applications/Visual Studio Code.app`; resolvido com o app existente + "Shell Command: Install 'code' command in PATH" pela paleta de comandos, sem reinstalar.

**Verificação do `/context` em `abrir-ciclo a`:** modelo mostrou `claude-opus-5-5` (esperado — o `settings.json` do `C-012`, que fixaria `claude-sonnet-5`, ainda não existe nessa checagem). Categoria "Skills" não veio zerada (2,1k tokens). Investigado com o Wagner: é uma skill pessoal da conta dele, sem relação com o trabalho de desenvolvimento do TCC (nome omitido a pedido dele). **Ameaça registrada:** como não é um arquivo dentro de `cfg-ciclo-a`/`cfg-ciclo-b` nem do repositório de ciclo, provavelmente é carregada pela conta/marketplace independente do `CLAUDE_CONFIG_DIR` — apareceria de forma simétrica nos dois ciclos, sem favorecer Spec Kit ou BMAD. Não é `CLAUDE.md`, skill de desenvolvimento nem MCP pessoal ligado a este projeto.

**Registro (25/09/2026):** critério do `C-011` considerado satisfeito com a ressalva acima.

### 6.5 `settings.json` único (`C-012`)

```json
{
  "model": "claude-sonnet-5",
  "alwaysThinkingEnabled": true,
  "env": {
    "CLAUDE_CODE_EFFORT_LEVEL": "high",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5",
    "CLAUDE_CODE_SUBAGENT_MODEL_FORCE": "1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-haiku-4-5-20251001",
    "DISABLE_AUTOUPDATER": "1",
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317"
  },
  "permissions": {
    "allow": []
  }
}
```

`permissions.allow` fica vazio de propósito: o P3 pede que a allowlist inclua "o comando que executa o script de coleta", mas o `/coletar-sessao` (`C-016`) só existe na Fase 6. Será preenchido então, mantendo os dois arquivos idênticos.

**Registro (25/09/2026):** arquivo colado em `~/cerne/cfg-ciclo-a/settings.json` e `~/cerne/cfg-ciclo-b/settings.json`; `diff` vazio; hash SHA-256 idêntico nos dois: `fdb4628757e596db7ea6bc57ec523309bf1c1591ac175f83caa2e07ea8285369`.

### 6.6 Ferramentas de avaliação (`C-013`)
| Ferramenta | Versão travada |
|---|---|
| Maestro | 2.10.0 |
| Java (dependência do Maestro) | `openjdk@21` (Homebrew) |
| mitmproxy | 12.2.3 |
| Coletor OpenTelemetry local | `otelcol-contrib` 0.161.0 — binário oficial (GitHub Releases, não há formula pronto no Homebrew, só `opentelemetry-cpp`, que é biblioteca, não o coletor). Config em `~/cerne/otelcol/config.yaml`: recebe OTLP grpc em `localhost:4317` (mesmo endpoint do `settings.json`, `C-012`), exporta para `~/cerne/otelcol/output.jsonl` |
| SDK OpenAI (avaliador) | 3.19.2, em ambiente Python `~/cerne/harness-venv` (`uv venv`) |
| Dependências Python do harness | Só a SDK da OpenAI travada por enquanto — os scripts do harness (M7, M12, `div_otel`, etc.) ainda não existem (Fase 6+); demais dependências entram quando os scripts forem escritos, registradas aqui |

**Registro (25/09/2026):** todas as versões acima conferidas por comando real, na máquina do Wagner.

### 6.7 Teste de fumaça só de ambiente (`GATE-C16`)

App descartável (`fvm flutter create smoke` em `/tmp/smoke`, fora de qualquer repositório de ciclo) com `whisper_ggml` adicionado (`flutter pub add`).

**Resultado (27/09/2026):** builda e roda com sucesso no **iPhone 16 Pro físico** (ambiente definitivo, ver revisão do P11/`GATE-C15` acima). No `sim-dev`, o mesmo build falha por completo — achado que motivou a mudança de plataforma (detalhe em §7 item 6 e no registro do `plano-ciclos.md`). Sequência de correções até funcionar, todas normais para assinatura de desenvolvedor pessoal em device real (nada relacionado ao `whisper_ggml`):
1. Deployment target do `Podfile` subido para 15.6 (exigência do próprio `whisper_ggml`).
2. Bundle Identifier trocado de `com.example.smoke` (namespace reservado, não registrável) para `com.wagnerduarte.smoke`.
3. Certificado "Apple Development: wagnerofduarte@gmail.com" confiado no aparelho (Ajustes → Geral → VPN e Gerenciamento de Dispositivo).

Permissão de microfone: **não testada** — o app é só o modelo padrão do `flutter create`, sem nenhum código que chame gravação de áudio; o critério original previa o microfone do Mac (cenário de simulador, superado pela mudança de plataforma). Fica para quando o RF02 for implementado de verdade.

`/tmp/smoke` apagado ao final, confirmado pelo Wagner.

**Registro (27/09/2026):** critério do `GATE-C16` satisfeito — ambiente de desenvolvimento/avaliação (iPhone 16 Pro físico) confirmado funcional, incluindo o ponto de maior risco (`whisper_ggml`). Falta só o `C-024` (§6.8) para fechar a Fase 4 por completo.

### 6.8 Isolamento dev/avaliação no dispositivo único (`C-024`)

Procedimento (substitui `sim-dev`/`sim-aval`):
1. **Desenvolvimento:** app instalado sem proxy configurado; certificado do mitmproxy **não** instalado no iPhone.
2. **Avaliação (Parte IV):** instalar o certificado do mitmproxy (via `http://mitm.it` com o proxy manual do Wi-Fi apontando para o Mac, porta 8080) + confiança total em Ajustes → Geral → Sobre → Configurações de Confiança de Certificado; configurar o proxy manual do Wi-Fi.
3. **Voltar ao desenvolvimento:** desligar o proxy manual do Wi-Fi e remover o certificado (Ajustes → Geral → VPN e Gerenciamento de Dispositivo → remover o perfil).

**Pendência (27/09/2026):** passos escritos e o caminho de rede confirmado alcançável (`http://192.168.18.27:8080` direto no Safari responde com `502` do próprio `mitmproxy`), mas a interceptação de tráfego geral **não foi confirmada** — `http://mitm.it` não mostrou a página de certificado mesmo com o proxy manual configurado corretamente (IP/porta certos, Private Relay desligado, sem perfil de MDM, testado em duas redes Wi-Fi diferentes — 5 GHz e 2,4 GHz — e após reconectar o Wi-Fi). Causa não identificada (possível isolamento de cliente no roteador doméstico). **Decisão do Wagner (27/09/2026):** documentar o procedimento como está e adiar a verificação completa para mais perto da Parte IV, quando o proxy for de fato necessário pela primeira vez — não travar o fechamento da Fase 4 por um problema de rede doméstica. Proxy do Wi-Fi desligado e `mitmproxy` parado no Mac ao final desta tentativa.

## 7. Divergências em relação aos documentos-fonte

Decisões que contrariam o texto de um documento-fonte, tomadas antes do congelamento e declaradas na monografia.

| # | Documento-fonte | O que diz | Decisão | Onde | Data |
|---|---|---|---|---|---|
| 1 | Requisitos §3 (RNF09) | 15 cenários de falha testados com `mocktail`, escritos pelo agente | Medidos pela suíte hold-out (caixa-preta); `mocktail` do agente como dado secundário | Métricas v1.0, M10 | já na v2 |
| 2 | Requisitos §8.2 | Complexidade via DCM ou fork do `dart_code_metrics` | CLI Dart próprio sobre a AST, regra de McCabe documentada | Métricas v1.0, M12; `GATE-C02` item 2 | 22/09/2026 |
| 3 | Requisitos §8.3 | Contraste "pipeline de agente único (Spec Kit) × fluxo com reset de contexto entre fases (BMAD)"; M14 mede perda de contexto entre fases | Reset de contexto a cada fase nos dois ciclos (P4); hipótese reformulada para fidelidade do handoff mediado por artefatos | P4; Métricas v1.0, M14, §5.6, §12 | 22/09/2026 |
| 4 | Requisitos §10 | Voyage `voyage-3` ou `voyage-4` | `voyage-4`, fixo pelo backend | Pacote de entrada (`C-005`) | plano |
| 5 | `doc-prototipo.md` (abertura) | App Flutter para iOS e Android | Desenvolvimento e avaliação só no iOS (P11) | P11 | 22/09/2026 |
| 6 | Protótipo HTML (frame) + P11/`GATE-C15` | Frame 390×844 (iPhone 16e/14), simulador único para dev e avaliação | `whisper_ggml` (P8) não roda em simulador iOS (limitação documentada do FFmpeg empacotado, confirmada externamente) — dev e avaliação passam a um único iPhone 16 Pro físico do Wagner (402×874 pts), nos dois ciclos inteiros; isolamento dev/avaliação vira reset manual entre fases (`C-024`) | P11; `GATE-C15`/`GATE-C16` | 27/09/2026 |
| 7 | `protocolo.md` §9 (achado 24/09/2026) | "Um reset recria o schema `experiment` inteiro do zero (`ai_replay_cache`, `worker_config`)" | Isso vale para `supabase db reset` **local** (`dev`). Nos ambientes hospedados (`ciclo-a`/`ciclo-b`), não existe esse comando contra projeto remoto (`docs/roteiro_de_congelamento.md`, achado no Passo 7) — o reset real ali é um `TRUNCATE` manual de só `entries, chat_sessions, chat_messages, insights, export_jobs`, que **não toca** `experiment.worker_config` nem `experiment.ai_replay_cache`. Os passos 2 (reconfigurar worker) e 3 (reimportar cache) do `reset-ambiente` (`C-015`) não são estritamente necessários a cada execução nesses ambientes — mantidos mesmo assim, por decisão do Wagner, como garantia redundante idempotente (não fazem mal repetir) | `C-015` | 29/09/2026 |

## 9. Cache de IA e reset (`GATE-C19`, achado e corrigido em 24/09/2026)

- **`--force` do `replay-cache-import.ts`:** confirmado, lendo o script — sempre mescla (`on conflict (cache_key) do nothing`), nunca sobrescreve. `--force` só libera a importação sobre um destino não vazio. **Nunca usado no fluxo normal**: todo reset deixa o destino vazio antes de importar.
- **Achado crítico:** `record` e `replay` são idênticos no código do backend (os dois gravam no cache); um reset recria o schema `experiment` inteiro (cache, config do worker). Um reset "nu" entre a importação do cache e a execução medida — como a v1 do `V-002` tinha — apagaria o cache e produziria `REPLAY_MISS` em tudo.
- **Correção:** `scripts/reset-ambiente <a|b>` (`C-015`) nunca é um reset isolado; é sempre reset → reconfigurar `worker_config` → reimportar `harness/cache-ciclo-a.json` (se existir) → rodar `backfill-seed-embeddings.ts`. Todo reset, em qualquer ponto do plano ou da suíte, passa por esse wrapper. `V-002` e `holdout/cenarios.md`/`rnf09.md` atualizados de acordo.
- **Registro (29/09/2026):** proposta aprovada pelo Wagner sem ajustes. `GATE-C19` fechado — a confirmação do comportamento de `--force` já estava satisfeita por leitura direta do código-fonte (achado de 24/09/2026, acima), sem pendência de máquina. Próximo passo: `C-015`, escrever os wrappers de verdade.
- **Divergência achada ao escrever o `C-015` (29/09/2026):** o "achado crítico" acima ("reset recria o schema `experiment` inteiro") vale só para `supabase db reset` local (`dev`). Não existe esse comando contra projeto remoto — nos ambientes hospedados (`ciclo-a`/`ciclo-b`), o reset real (`docs/roteiro_de_congelamento.md`, Passo 7) é um `TRUNCATE` manual de `entries, chat_sessions, chat_messages, insights, export_jobs`, que não inclui as tabelas do schema `experiment`. Ver `§7` item 7. Decisão do Wagner: manter os 4 passos do wrapper mesmo assim (idempotentes, sem custo real); e implementar o truncate+seed em Deno puro (biblioteca `postgres`), sem depender de `psql` — mesma lógica do `configure-worker.ts` (achado: o Mac não tem `psql` por padrão).
- **Execução real, `C-015` fechado (29/09/2026):** `scripts/db-truncate-and-seed.ts`, `scripts/reset-ambiente <a|b>` e `scripts/replay-mode <a|b> <modo>` escritos em `cerne-avaliacao/scripts/`. `reset-ambiente` roda em `--dry-run` (4 passos exibidos, passo 3 corretamente pulado sem cache congelado) e de verdade nos dois ambientes, sem erro; os 33 embeddings do backfill vieram do cache de replay (0 chamadas novas à Voyage). Contagem confirmada via SQL Editor nos dois: 34 entradas da conta A, 1 `failed`, 33 `ready`. Teste de exportação real (`export-summary-create` + `export-status-get`, autenticado com a conta seed): job criado em `pending`, concluído em `done` nos dois ambientes (`entryCount: 34`, `downloadAvailable: true`), confirmando que `configure-worker.ts` deixou o worker de exportação funcional. `replay-mode a replay` testado de verdade — `supabase secrets set` concluído e `REPLAY_MODE` confirmado presente em `supabase secrets list --project-ref fgzqqkwxwfxlxbdktwzo`. **Achado lateral, sem ação:** a mesma listagem de secrets mostrou que `TEST_FAULT_KEY` já existe no ambiente hospedado (só a chave, não o valor) — mantém-se adiado para a Parte IV, conforme decisão já registrada em `§10.2`.

## 8. Especificação da avaliação (Fase 7)

| Item | Decisão | Data |
|---|---|---|
| Fontes das decisões da M14 | Spec Kit: constitution + `plan.md` da F000; BMAD: arquitetura | 24/09/2026 (R29) |
| Convenções da M15 | Referência na feature do RF01; C1 subpastas, C2 sufixo de repositório, C3 nome de falha, C4 nomes de BLoC/evento/estado | 24/09/2026 (R29) |
| Injeção de falhas da hold-out | Cabeçalho `X-Test-Fault` posto pelo proxy, efeito executado pelo backend (determinístico, com log) | 24/09/2026 (R30) |
| Escala de severidade `Sn` (D16) | S1 cosmético · S2 funcional com contorno · S3 bloqueante | 24/09/2026 (R30) |
| `M6_tasks` no Ciclo B sem checkboxes | % de stories `done` no `sprint-status.yaml`, declarado como granularidade mais grossa | 24/09/2026 (R30) |
| Tabela de preços da M3 | `harness/precos.md` (consulta de 24/09/2026) | 24/09/2026 |

## 10. Repositórios, credenciais e ambientes de backend (Fase 5)

### 10.1 Repositórios de ciclo (`GATE-C17`)
| Repositório | Situação |
|---|---|
| `WagnerofDuarte/cerne-ciclo-a` | Criado, privado, vazio |
| `WagnerofDuarte/cerne-ciclo-b` | Criado, privado, vazio |

**Registro (27/09/2026):** os dois clonados localmente, `git log --oneline` vazio nos dois — confirmado.

### 10.2 Credenciais e ambientes de backend (`C-014`, `GATE-C18`)

**Achado crítico de processo (28/09/2026):** o registro original do `C-014` (24/09/2026) descrevia `segredos/.env.ciclo-a`/`.env.ciclo-b` como criados — mas foi escrito numa sessão de nuvem anterior, que criou os arquivos no próprio container efêmero dela, nunca na máquina real do Wagner. O container foi reciclado, os arquivos nunca existiram de fato fora daquela sessão. Só descoberto agora, ao tentar usá-los de verdade para o `GATE-C18`. **Isto é um risco geral de todo trabalho feito em sessão de nuvem sem o passo explícito de "peça para o usuário confirmar/criar na máquina dele": um registro "concluído" pode descrever um artefato que só existiu dentro do container.** Vale reconferir os outros artefatos supostamente criados em sessões de nuvem anteriores (ex.: `segredos/db.ciclo-a.env`/`db.ciclo-b.env`, mencionados no mesmo registro do `C-014`) antes de depender deles no `C-015`.

`segredos/.env.ciclo-a`/`.env.ciclo-b` recriados de fato em 28/09/2026, com `FUNCTIONS_BASE_URL` e `SUPABASE_ANON_KEY` pegos direto no painel do Supabase (Project Settings → API, valores públicos por design). `grep -c service_role` = `0` nos dois.

**`GATE-C18` — conferência dos ambientes:**
| Item | `ciclo-a` | `ciclo-b` |
|---|---|---|
| Hash do schema (`schema-hash.ts`) | `f33a12b44912ae129a4702bcf7c8fffdcd93d7defad15df2323171cf779868e2` | idêntico |
| Estrutura | extensões=6, colunas=91, tabelas com RLS=12, constraints=39, índices=17, triggers=2, funções=14, políticas=32, grants=83 (idêntico nos dois) | — |
| Login (`auth-login`, conta `cenario-cheio@cerne.test`) | `200` | `200` |
| Chamada autenticada (`entries-list`) | `200`, 20 entradas (= `limit` default do endpoint) | `200`, 20 entradas |

Não foi possível comparar o hash com o valor exato registrado em 11/09/2026 — o roteiro de congelamento do `cerne-backend` documenta o procedimento, mas não guarda o hash em texto (só foi impresso no terminal na hora). A comparação feita é `ciclo-a` == `ciclo-b`, que é o que importa para a validade do experimento (nenhum ciclo começa com estrutura diferente do outro).

**Achados reais de ambiente durante a conferência (não são erro de configuração do Wagner):**
- A connection string **direta** do Supabase (`db.<ref>.supabase.co:5432`) exige IPv6; a rede do Wagner não tem saída IPv6 — a conexão trava para sempre (nunca dá erro claro), em vez de falhar rápido. Resolvido usando a connection string do **pooler** (`aws-0-sa-east-1.pooler.supabase.com:5432`, usuário `postgres.<project-ref>`).
- A senha do Postgres contém um `@` literal — precisa de `%40` na connection string; sem isso, o parser da URL quebra silenciosamente (o `@` da senha vira parte do host) e a conexão também trava, com o mesmo sintoma do problema de IPv6 (mais difícil de diferenciar).
- URL correta dos endpoints das Edge Functions: `{FUNCTIONS_BASE_URL}/<x-cerne-function>` (nome da função, com hífen — ex.: `auth-login`, `entries-list`), **não** o path do OpenAPI (`/auth/login`, `/entries`) — documentado no próprio `openapi.yaml`, linha 6-8, mas fácil de errar na primeira leitura.

**Nota de segurança (28/09/2026):** a senha do banco do `ciclo-a` apareceu em texto puro no chat desta sessão durante o diagnóstico do `%40`. Recomendado ao Wagner trocar essa senha no painel do Supabase (Project Settings → Database → Reset database password) antes do `GATE-C23`.

**`segredos/db.ciclo-a.env`/`db.ciclo-b.env`:** também eram fantasmas (mesma causa do `.env.ciclo-*`) — recriados de verdade em 28/09/2026 com a connection string do pooler (`%40` na senha); `schema-hash.ts` reconfirmado com os dois, mesmo hash de antes (`f33a12b4...9868e2`).

**Pendência — `TEST_FAULT_KEY`:** tentativa de confirmar o valor configurado nos ambientes hospedados via teste leve e seguro (`X-Test-Now` no `dashboard-aggregate-get`, sem sujar a conta seed) esbarrou num erro de app não relacionado — `404 NOT_FOUND "perfil do usuário autenticado não encontrado"` para a conta `cenario-cheio@cerne.test` nesse endpoint específico (achado à parte, pode ser relevante para a avaliação real — anotado aqui, não investigado agora). **Decisão do Wagner (28/09/2026):** adiar a confirmação do `TEST_FAULT_KEY` para mais perto da Parte IV, quando o proxy de falhas for montado de qualquer forma — não bloqueia a Fase 5.

## 11. Instrumento mínimo pré-ciclo (Fase 6)

### 11.1 Formato do transcript JSONL do Claude Code (`C-016`)

**Risco de base:** a documentação oficial do Claude Code avisa que o formato interno do transcript "muda entre versões" e recomenda `/export` ou `claude -p --output-format json` em vez de parsing direto — não há schema público estável. Os campos abaixo foram confirmados contra uma sessão **real** do Wagner (Claude Code 2.1.282, 01/10/2026), não contra a documentação oficial, que não os garante entre versões. Qualquer atualização do Claude Code travado (`C-011`) exige reconferir isto antes de confiar nos dados coletados.

**Confirmado de verdade, por inspeção de sessão real:**
- Caminho do transcript: `~/.claude/projects/<cwd-com-não-alfanuméricos-trocados-por-"->/<session-id>.jsonl`; desloca por completo com `CLAUDE_CONFIG_DIR` (a mesma variável que isola `cfg-ciclo-a`/`cfg-ciclo-b`, `C-011`).
- `timestamp`: ISO 8601 com milissegundos e `Z` (ex.: `2026-10-01T02:07:11.454Z`), em todo tipo de registro.
- Mensagem de usuário humana: `{"type": "user", "origin": {"kind": "human"}, "message": {"role": "user", "content": [...]}}`. Mensagens/eventos de sistema (ex.: slash command) não têm `origin.kind: "human"` — é o campo usado para nunca confundir uma mensagem do pesquisador com qualquer outra coisa.
- Resposta do assistente: `{"type": "assistant", "message": {"id": "msg_...", "model": "...", "usage": {...}}}`. `usage` por mensagem, incluindo `cache_creation.ephemeral_5m_input_tokens`/`ephemeral_1h_input_tokens` — bate exatamente com a regra 2 do `harness/precos.md` (preços diferentes para escrita de cache de 5 min e de 1h). Mensagens do mesmo turno podem repetir o mesmo `message.id` em mais de uma linha (um bloco de conteúdo por linha) — o script deduplica por esse campo antes de somar.
- Slash command / skill invocada: `{"type": "system", "subtype": "local_command", "commandRun": {"command": "<nome>", "args": "..."}}` — é o sinal usado para a segmentação por fase (`protocolo.md` §4.4).
- **Achado não previsto no plano original:** o contexto que a extensão do Claude Code no VS Code injeta (arquivo aberto, seleção) **não** aparece como um campo/atributo separado da mensagem — aparece como um **bloco de texto próprio**, dentro do mesmo `message.content` da mensagem do usuário, envolto em `<ide_selection>...</ide_selection>`, antes do texto que o pesquisador de fato escreveu. `n_msgs_contexto_ide` (P2) é contado em cima desse marcador. Sessões abertas pelo terminal (`entrypoint: "cli"`) nunca têm esse bloco; sessões abertas pela extensão (`entrypoint: "claude-vscode"`) só têm quando havia de fato um arquivo com seleção ativa no momento de enviar a mensagem.

**Não confirmado empiricamente** (nenhuma sessão de teste gerou o evento de verdade; implementado por relato de comunidade, com degradação segura para 0/vazio se não bater, nunca por suposição silenciosa) — **confirmar no `GATE-C21`**, que já previa provocar um subagente de propósito:
- Caminho dos transcripts de subagentes (esperado: diretório irmão do `.jsonl` principal, `<session-id>/subagents/workflows/<run>/agent-*.jsonl`).
- Formato do evento de compactação automática (`{"type": "system", "subtype": "compact_boundary", "compactMetadata": {...}}`).

**Decisão própria do script, sem valor congelado em nenhuma fonte, pendente de revisão do Wagner antes do `GATE-C23`:** tolerância de `div_otel` fixada em 2%.

### 11.2 `C-016` — estado

`scripts/coletar_sessao.py` (parser + CLI nos 3 modos: `skill`, `hook`, `manual`) e `skills/coletar-sessao/SKILL.md` escritos em `cerne-avaliacao`. 12 testes unitários (`scripts/tests/test_coletar_sessao.py`) cobrindo os 4 cenários do critério do plano (sem intervenção; 3 intervenções de tipos diferentes; compactação no meio; subagente com tokens em arquivo separado) × os 3 modos — todos passando, incluindo a confirmação de que o corte do modo `skill` exclui a mensagem de invocação e tudo depois, e que os tokens do subagente somam nas colunas `sub_*` sem se misturar com os do principal. Falta: `C-017`, e a verificação real (não sintética) nos `GATE-C20`/`GATE-C21`.
