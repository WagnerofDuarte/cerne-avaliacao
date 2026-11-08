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

## 4. Status por item (08/11/2026, sessão na nuvem)

Ferramentas instaladas nesta sessão (em `/root/tools`, fora do repositório): Dart 3.13.7, Flutter 3.47.9 (stable), Deno 2.9.8, mitmproxy 12.3.1 (venv Python), pytest, PyYAML, Pillow. Pub.dev, GitHub e npm responderam pelo proxy da sessão.

| Item | Estado | Verificado | Falta / não verificável |
|---|---|---|---|
| T0 | feito | — | — |
| H-001 | **atendido** | v1/v2 montam, testes rodam (v1: 10 passam; v2: 8 passam, 1 falha, 1 apagado); gabarito com arquivo:linha e CC à mão | — |
| H-002 | **atendido na calibração** (M4, M6-D, M7+RF07/RF10, M8, M8b, M9-D, M10-D, M12, M13, M14-D, M15) | 1 módulo = 1 teste contra `gabarito.json`; nem mais, nem menos | Formatos reais de `openapi.yaml`/taxonomia/README (M6) e os caminhos de saída do BMAD (M4) não foram vistos: ver pendências |
| Plano B | escrito, **não executado** | revisado por leitura contra `cenarios.md`/`rnf09.md`/`estados-m9.md` | execução é do Wagner/guia |
| H-003 | (a fazer) | | |
| H-004 | (a fazer) | | |
| H-005 | (a fazer) | | |
| H-006 | (a fazer) | | |
| H-007 | fora de escopo (guia) | | |

**M8b:** o módulo encontrou o mutante plantado (`validate_entry.dart:5`, `<=`→`<`) e reproduziu exatamente a lista de 17 mutantes (9 mortos, 8 sobreviventes, score 0,5294) derivada à mão antes da execução. **Recomendação: manter a M8b** (condição do GATE-C02 item 8 satisfeita). Ferramenta: módulo próprio (Python), `mutation_test` do pub.dev não foi avaliado a fundo.

### Interpretações adotadas (nenhuma contradiz texto congelado; todas deterministas e documentadas no código)

- M7: "`package:flutter`" = `package:flutter/`; BLoC = arquivo `*_bloc.dart`/`*_cubit.dart`; RF10 = arquivo de chat importa, na feature de entradas, algo em `data/` ou com `repository|datasource` no nome. Os nomes das features (`chat`, `entries`) são parâmetros (`--chat-feature`, `--entries-feature`): **para cada ciclo é preciso informar os nomes reais** (ou detectar pelo diff de `rf10-done`).
- M9 hardcodes: `Colors.<x>` (exceto `transparent`) conta como cor; espaçamento = `EdgeInsets.*` e `SizedBox(width|height)` com literal numérico ≠ 0.
- M10: `M10_assinaturas` conta **assinaturas** fora do padrão (a §5.2 diz "repositórios fora do padrão"; a saída traz também `repositorios_fora`).
- M12: `for` de coleção e braço de `switch` expression **não** contam (não estão na lista); closure conta no método que a contém; só declarações com corpo entram.
- M6: referências inexistentes contadas por token **distinto** por categoria; (c2)/(c3) só em arquivos `data/`; citados × alterados usa só `plan.md` e arquivos `lib/**.dart` do diff.
- M14: dedup = conjunto de identificadores igual ou subconjunto; verbos de prescrição ampliados (`add`, `keep`, `goes through`, `placed in`…).
- M15: unidade de divergência definida em `m15_consistencia.py` (simétrica por subpasta/papel; por classe nas convenções C2/C3).
- M8: como o lcov só lista arquivos importados por algum teste, o módulo injeta na cópia um teste que importa todo o domínio (senão arquivos sem teste somem do denominador).

## 5. Rascunhos de desvio

(nenhum até aqui)

## 6. Pendências / dependem do Wagner

(nenhuma até aqui)
