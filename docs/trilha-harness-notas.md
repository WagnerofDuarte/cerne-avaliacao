# Trilha do harness — notas de trabalho

**Arquivo da trilha** (não está no rol de congelados). Sessão na nuvem, branch `harness`, início 08/11/2026. Nova data de corte da suíte: **13/11/2026** (D-095). Fora de escopo: **H-007** (com o guia).

## 1. Resumo da leitura (T0)

| Item | O que pede | Critério |
|---|---|---|
| H-001 | App Flutter sintético de calibração em `calibracao/` com violações plantadas + `gabarito.md` (arquivo:linha; CC à mão de cada método do domínio) | Gabarito lista cada violação com arquivo e linha |
| H-002 | Módulos estáticos em `harness/estatico/` (M4, M6-D, M7+RF07/RF10, M9-D, M10-D, M13, M14-D, M15), CLI Dart `harness/m12/`, M8 (cópia temporária, lcov fora do repo), M8b (condicional) | Cada módulo acha exatamente as violações do gabarito |
| H-003 | Teste de introspecção tipográfica (fontFamily/fontSize) injetado na cópia temporária | Detecta a fonte plantada fora do token |
| H-004 | Amostragem de cor em screenshots | Acerta num par sintético (certa/errada) |
| H-005 | Suíte hold-out: Maestro (C-018 e C-020), addon mitmproxy (C-019 + debounce RF06), SQL (Deno + lib `postgres`) | Addon e SQL verdes contra servidor falso/Postgres local; todo cenário tem implementação |
| H-006 | Skills `/avaliar-rf`, `/julgar-rf`, `/avaliar-ciclo`, `/validar-juiz` em `.claude/skills/` | Rodam de ponta a ponta na calibração, CSVs no esquema C-002 |
| H-007 | **Fora de escopo** (guia) | — |

Regras que guiam o desenho: cegamento (testes só na `calibracao/`), nenhum output de medição em repositório de app, avaliador `gpt-5.5-2026-04-23` com `reasoning.effort=medium` (simulado nos testes), arquivos congelados somente leitura.

**Ordem de trabalho:** T0 → H-001 → H-002 (módulo a módulo) → checklist manual → H-003/H-004 → H-005 → H-006 → (opcional) V-006.

## 2. Ferramentas no ambiente (08/11/2026)

- Inicialmente: `python3` 3.13 e `node` 22 presentes; **ausentes** `dart`, `flutter`, `deno`, `mitmdump`. Rede (pip, storage.googleapis.com, github releases, npm) responde; instalação em `/root/tools` (ver seção de status).
- Sem simulador, Maestro, iPhone: fluxos Maestro apenas escritos e revisados por leitura.
- `entrada/`, `dados/`, `segredos/` não existem neste checkout (de propósito): o M6 (referências ao backend) recebe `openapi.yaml`/taxonomia por argumento e é testado com versões sintéticas.

## 3. Decisões

**D-T0-1 — Como a calibração tem `v1` e `v2`.** Opções: (a) sub-repositório git aninhado; (b) duas pastas de snapshot. **Escolhido: (b) + montagem em repositório git temporário.** `calibracao/v1/` e `calibracao/v2/` são snapshots rastreáveis, revisáveis e sem `.git` aninhado (que o repositório externo trataria como gitlink e que não sobe ao GitHub). O script `calibracao/montar-repo.sh <destino>` cria, fora do repositório, um git real com dois commits e as tags `v1` e `v2`; o harness mede **por tag** nesse repositório montado (mesma interface que terá nos ciclos: `git worktree`/checkout da tag em cópia temporária). Alternativa (a) descartada por não ser versionável no repositório externo.

(demais decisões entram abaixo conforme o trabalho avança)

## 4. Status por item (08/11/2026, sessão na nuvem; branch `harness`)

Ferramentas instaladas nesta sessão em `/root/tools` (fora do repositório): Dart 3.13.7, Flutter 3.47.9, Deno 2.9.8, mitmproxy 12.3.1 (venv), pytest, PyYAML, Pillow; Postgres 16 do sistema para o teste das asserções SQL. Pub.dev, GitHub, npm e PyPI responderam; **deno.land não** (por isso `npm:postgres`).

| Item | Estado | Verificado (como) | Parcial / não verificável |
|---|---|---|---|
| T0 | feito | — | — |
| **H-001** | **atendido** | `calibracao/v1`, `v2` montam em git temporário (`montar-repo.sh`); `flutter test` v1: 10 passam; v2: 8 passam, 1 falha, 1 apagado; `gabarito.json`/`gabarito.md` com arquivo:linha e CC à mão | — |
| **H-002** | **atendido na calibração** (11 módulos + CLI Dart) | 1 teste por módulo contra `gabarito.json`: achou exatamente as violações, nem mais nem menos. M12: CC à mão = CLI. M8b: lista de 17 mutantes derivada à mão **antes** de rodar = resultado | M6 (formato real de `openapi.yaml`/taxonomia/README) e M4-BMAD (caminhos) **não verificáveis** aqui; M8: denominador de linhas é o da VM (ver gabarito) |
| Plano B | escrito, **não executado** | `holdout/checklist-manual.md` revisado por leitura contra `cenarios.md`/`rnf09.md`/`estados-m9.md` (28+15+31) | — |
| **H-003** | **atendido** | widget test injetado em cópia temporária detecta `Courier`/17 fora do token e não acusa página limpa | tokens reais: ver `holdout/tokens-prototipo.json` (lidos do protótipo; conferir com `doc-prototipo.md`) |
| **H-004** | **atendido** | par sintético certo/errado (+ quase/longe) | tolerância ΔE76 = 4,0 é escolha do harness |
| **H-005** | **parcial: atendido onde o critério permite** | addon: 14 testes (mitmdump real × backend **falso**: cabeçalhos, 15 falhas, 2ª chamada, corte de SSE, 401 forjado, offline, reescrita, contagem/debounce); SQL: Deno + `npm:postgres` num Postgres **local** com schema sintético, positivo e negativo; Maestro: 71 fluxos (25+15+31) + manifesto, **só revisados por leitura** (`verificar.py`: cobertura, sintaxe, texto × protótipo) | Maestro nunca rodou; nomes de função/SSE/401/colunas SQL/posições de ícone são **suposições** (ver README-suite) |
| **H-006** | **atendido na calibração com avaliador simulado** | `harness/avaliador/tests`: avaliar-rf (linha de `rf.csv` bate com o gabarito), julgar-rf (voto, anonimização, log), avaliar-ciclo (`ciclo.csv`, `estados_m9.csv`, M14), validar-juiz (amostra cega, κ) | **chamada real ao `gpt-5.5-2026-04-23` nunca exercitada** (sem chave, por desenho); M1–M3/M5 agregados só em CSVs sintéticos |
| V-006 (opcional) | **não feito** | — | falta de tempo/prioridade |
| H-007 | fora de escopo (guia) | — | — |

**M8b:** mantida. O módulo encontrou o mutante plantado (`validate_entry.dart:5`, `<=`→`<`) e os demais sobreviventes/mortos coincidem com a derivação à mão (17 mutantes, 9 mortos, 8 sobreviventes, 0,5294). Ferramenta: módulo próprio em Python; `mutation_test` (pub.dev) **não foi avaliado**. Custo medido: ~1 min para 17 mutantes numa suíte de 10 testes.

### Interpretações adotadas (todas deterministas e documentadas no código; nenhuma contradiz texto congelado)
- **M7:** `package:flutter` = `package:flutter/`; BLoC = `*_bloc.dart`/`*_cubit.dart`; RF10 = arquivo de chat importa, na feature de entradas, algo em `data/` ou com `repository|datasource` no nome. **Os nomes das features são parâmetros por ciclo** (`--chat-feature`, `--entries-feature`).
- **M9 hardcodes:** `Colors.<x>` (exceto `transparent`) conta como cor; espaçamento = `EdgeInsets.*`/`SizedBox(width|height)` com literal ≠ 0.
- **M10:** `M10_assinaturas` conta assinaturas (a §5.2 diz "repositórios fora do padrão"; a saída traz também `repositorios_fora`).
- **M12:** `for` de coleção e braço de `switch` expression não contam (não estão na lista); closure conta no método que a contém; só declarações com corpo.
- **M6:** referências inexistentes por token distinto por categoria; (c2)/(c3) só em arquivos `data/`; citados × alterados usa `plan.md` e arquivos `lib/**.dart` do diff.
- **M14:** dedup por identificadores iguais/subconjunto; verbos de prescrição ampliados; check estático = existência, "nunca importa" ou juiz.
- **M15:** divergência = diferença simétrica por subpasta (C1) e por papel (C4); por classe (C2/C3).
- **M8:** o lcov só lista arquivos importados por algum teste; o módulo injeta na cópia um teste que importa todo o domínio.
- **M9 score:** soma de cor_ok + tipografia_ok + espacamento_ok.

## 5. Rascunhos de desvio (prontos para colar em `docs/desvios.md`; numeração a cargo do guia)

| # | Data | Item congelado | O que mudou | Por quê | Afeta | Ciclos já executados com a versão anterior |
|---|---|---|---|---|---|---|
| H-A | 08/11/2026 | `harness/juiz/` (hash combinado) | **Arquivo novo** `harness/juiz/anonimizacao.txt` (lista de termos, cabeçalhos e diretórios do README, "Anonimização", item 3). Escrito de memória quanto a nomes de persona e cabeçalhos de template do BMAD/Spec Kit: **conferir com a instalação real** | Previsto pelo plano (README manda "lista congelada em `anonimizacao.txt`, escrita na trilha paralela") | Hash combinado de `harness/juiz/` muda (README e rubricas intactos) | Nenhum (sem avaliação feita) |
| H-B | 08/11/2026 | `holdout/fixtures/textos-instrumento.json` | **Nenhuma mudança necessária:** `rnf09_mensagem_1..3` já estão no arquivo. A exceção prevista no plano não foi usada; o hash dessa pasta **não** muda por esse motivo | Verificado por leitura | — | — |
| H-C | 08/11/2026 | `holdout/cenarios.md` × protótipo congelado | **Textos que não batem com o HTML de referência** (achado da revisão por leitura dos fluxos): (a) H09-1 "Comece a registrar para ver sua evolução aqui" → protótipo: "Ainda não há registros suficientes para mostrar sua evolução. Comece a escrever para ver seu gráfico aqui."; (b) H09-1 "Ainda é cedo pra ver um padrão — volte em alguns dias." → protótipo: "Você deu o primeiro passo. Continue registrando para ver padrões surgirem ao longo do tempo."; (c) H06-4 "INTERVALO DE DATA" → protótipo: "PERÍODO"; (d) H02-1/F07–F09 "Salvar só a foto" **não existe** no protótipo (estado de erro do OCR: "Não foi possível reconhecer o texto — tente outra foto." + "Tentar novamente"); (e) "Baixar dados brutos" existe, "Baixar PDF" também. Os fluxos Maestro usam o texto do **protótipo** e levam `# DIVERGENCIA` | `cenarios.md` §0: "se um texto do app diferir do protótipo, o passo falha"; o app deveria seguir o protótipo | M11 (H09-1, H06-4, H02-1), M10 (F07–F09) se a suíte fosse executada com os textos de `cenarios.md` | **Decisão do Wagner/guia:** corrigir `cenarios.md` (desvio, antes da execução, aplicado igual aos dois ciclos — `V-002` passo 6) ou manter os textos dos fluxos |
| H-D | 08/11/2026 | `harness/regras.md` §3, §2 (interpretações) | **Sem edição.** Interpretações de implementação (M6, M7, M10, M12, M14, M15, M9) listadas na seção 4 destas notas; nenhuma altera o texto congelado | Transparência: o texto fixa o critério, não todos os detalhes de contagem | M6/M7/M10/M12/M14/M15 | — |
| H-E | 08/11/2026 | `docs/Metricas_e_Skills_Ciclos.md` §7 (cenários H07-2) | O cenário estrutural **H07-2** (selo de sincronização independente da autenticação) **não tem módulo no H-002** (a lista do plano só cobre RF07 "BLoC importa BLoC" e RF10): fica por leitura de código (no checklist manual, §5). Recomenda-se declará-lo "verificação manual por leitura" | O plano não o inclui no H-002 | M11 (RF07) | — |

## 6. Pendências e decisões que dependem do Wagner / do guia

1. **H-C acima:** os 5 textos de `cenarios.md` que não existem no protótipo (corrigir `cenarios.md` por desvio, ou manter?). Sem decisão, a suíte automatizada e o checklist divergem.
2. **Formatos reais não vistos** (`entrada/` ausente): `openapi.yaml`, `error-taxonomy.md`, tabela do `backend/README.md` (M6 c1–c4); caminhos de saída do **BMAD** e `mapa-stories.csv` (M4, M6_tasks no B). Rodar o M6 e o M4-BMAD sobre a **versão real** de cada um e ajustar parâmetros (sem mudar a regra) **antes** do GATE-H02.
3. **Suposições do addon/SQL/Maestro** (backend não está aqui): nome da função (`x-cerne-function` vs `/functions/v1/<fn>`), formato do SSE (`event: token`), corpo do 401 forjado, chaves do JSON da narrativa e do status, esquema das tabelas, posições dos ícones (medidas no protótipo, ±4 px), `pressKey: Home` e esperas reais no iOS físico (`extendedWaitUntil optional`), `maestro` em dispositivo físico. Conferir contra `cerne-backend` e contra um ensaio **fora dos ciclos** (ex.: no app de calibração ou em app descartável).
4. **Chamada real ao avaliador** (`gpt-5.5-2026-04-23`, esforço `medium`): nunca exercitada; testar com 1 item de calibração e a chave no ambiente, conferindo o formato da Responses API (`text.format.json_schema`, entrada de imagem).
5. **Anonimização:** conferir `harness/juiz/anonimizacao.txt` com a instalação real (nomes de persona/cabeçalhos).
6. **Tokens de design:** `holdout/tokens-prototipo.json` foi lido do HTML de referência; conferir com a §4 do `doc-prototipo.md` (corPrimária `#1F3D34`; famílias Karla/Fraunces/IBM Plex Mono).
7. **Nomes das features por ciclo** para o M7/RF10 e a feature do RF01 para o M15 (`--ref-feature`, ou `detectar_ref` com a tag anterior ao RF01).
8. **GATE-H02:** hashes de `harness/`, `holdout/` e `.claude/skills/` (atenção: o checkout é parcial e `.claude/` entrou com `git add --sparse`) e a tag `harness-v1.0` ficam com o Wagner.
9. **Decisão de M8b (D-095 item 2):** a recomendação é **manter**.

## 7. Como reproduzir (ambiente desta sessão)

```bash
export PATH=/root/tools/flutter/bin:/root/tools/dart-sdk/bin:/root/tools:$PATH FLUTTER_ALLOW_ROOT=true
git config --global --add safe.directory /root/tools/flutter
calibracao/montar-repo.sh /tmp/cal                           # repositório de calibração com tags v1 e v2
python3 -m pytest -q                                         # tudo (~5 min): estático, M9, proxy, Maestro (leitura), avaliador
(cd harness/m12 && dart pub get && dart test)                # CLI da M12
DATABASE_URL=$(holdout/sql/pg_local.sh up) deno test --allow-net --allow-env --allow-read holdout/sql/tests/; holdout/sql/pg_local.sh down
python3 holdout/maestro/gerar.py && python3 holdout/maestro/verificar.py      # fluxos e revisão por leitura
python3 -m harness.estatico.m7_camadas --repo /tmp/cal --tag v2              # exemplo de módulo isolado
```

---

## BLOCO PARA O GUIA (08/11/2026, fim da sessão na nuvem; branch `harness`)

**Estado dos itens** (detalhe na seção 4): H-001 atendido · H-002 atendido na calibração (11 módulos + CLI Dart, cada um acha exatamente o gabarito) · Plano B (`holdout/checklist-manual.md`) escrito, não executado · H-003 e H-004 atendidos · H-005 **parcial** (addon e SQL verdes contra servidor falso/Postgres local; 71 fluxos Maestro só revisados por leitura) · H-006 atendido na calibração com avaliador **simulado** · V-006 não feito · H-007 fora de escopo.

**M8b (D-095 item 2): manter.** O módulo achou o mutante plantado (`validate_entry.dart:5`, `<=`→`<`); 17 mutantes, 9 mortos, 8 sobreviventes (0,5294), igual à derivação à mão.

**Commits e branch:** `harness` (push feito). Sem tags, sem PR, sem push fora da `harness`. `.claude/skills/` entrou com `git add --sparse` (o checkout parcial não o inclui).

**Rascunhos de desvio:** H-A (nova `harness/juiz/anonimizacao.txt`), H-B (nenhuma mudança em `fixtures/textos-instrumento.json`: as três mensagens já existiam), H-C (**textos de `cenarios.md` ausentes do protótipo**: 5 casos), H-D (interpretações de contagem, sem edição), H-E (H07-2 sem módulo). Texto pronto na seção 5.

**Decisões que dependem do Wagner:** (1) H-C: corrigir `cenarios.md` por desvio ou manter; (2) conferir contra o material real, que não existe neste checkout: `openapi.yaml`/taxonomia/README (M6), caminhos do BMAD e `mapa-stories.csv` (M4/M6_tasks no B), `doc-prototipo.md` §4 (tokens), `cerne-backend` (funções, SSE, 401, esquema SQL); (3) um ensaio real do avaliador (chave no ambiente) e do Maestro **fora dos ciclos**; (4) GATE-H02: hashes e tag `harness-v1.0`.

**Riscos:** (a) fluxos Maestro nunca rodaram (posições de ícones medidas no protótipo, ±4 px; esperas reais no iOS físico por `extendedWaitUntil optional`); (b) suposições do addon/SQL listadas na seção 6; (c) o avaliador real não foi chamado; (d) a nova data de corte (13/11) só vale se esses ensaios forem feitos antes: se não der, vale o checklist manual (D-095); (e) o M6 e o M4-BMAD podem precisar de ajuste de parâmetro (não de regra) quando virem os arquivos reais; (f) nenhum dado de `dados/`, `segredos/`, `entrada/` ou dos repositórios dos ciclos foi lido; nenhuma métrica de ciclo foi calculada; nenhum backend hospedado foi tocado.
