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

## 4. Status por item

(atualizado a cada commit)

## 5. Rascunhos de desvio

(nenhum até aqui)

## 6. Pendências / dependem do Wagner

(nenhuma até aqui)
