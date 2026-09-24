# Estados avaliados na M9 (fidelidade visual)

**Destino:** `cerne-avaliacao/holdout/estados-m9.md` · **Tarefa:** `C-020` · **Versão:** 23/09/2026
**Fonte:** catálogo de estados do próprio protótipo (`Cerne - Prototipo Final.html`, SHA-256 `61032a92…185d2fff`; lista "frameGroups" com 32 itens) menos o estado de extensão (P10).
**Uso:** M9 — cor e tipografia (mecanismo D, sobre screenshot e árvore de widgets) e espaçamento (mecanismo J), só nos screenshots da tag `final`; score 0–3 por estado em `estados_m9.csv`. Hardcodes (mecanismo D) valem para o código inteiro, em toda tag.

## Regras de captura

- **Dispositivo:** o modelo da P11, com as dimensões do frame do protótipo (390 × 844); mesma versão de iOS nos dois ciclos.
- **Referência:** para cada estado, o frame do protótipo é capturado abrindo o HTML **original** (congelado, `holdout/referencia/Cerne - Prototipo Final.html`) e escolhendo o item do catálogo pelo `id` da tabela; captura no mesmo tamanho lógico.
- **Condições do app:** as do `cenarios.md` (seção 0), inclusive proxy e contas. Estados transitórios (streaming, processando) são congelados pelo proxy, que segura a resposta pelo tempo da captura; estados de erro são provocados como indicado.
- **Estado inalcançável** no app (a tela não existe ou o caminho não leva a ela): score 0, com a justificativa registrada — ausência de um estado previsto é falta de fidelidade.
- **Conteúdo diferente** (textos do usuário, datas, quantidades): não é critério; só cor, tipografia e espaçamento.

## Os 31 estados

Fora: `planos` — "Tela 5 — Planos de Ação" (extensão, não construída, P10).

| # | `id` no catálogo | Estado | Conta | Caminho no app até o estado |
|---|---|---|---|---|
| 1 | `splash` | Tela 0 — Splash | — | Abrir o app a frio; captura no primeiro quadro estável |
| 2 | `bio` | Tela 0.1 — Biometria | A | Com sessão salva e app bloqueado, abrir o app |
| 3 | `login` | Tela 0.1a — Entrar / criar conta | — | Primeira abertura sem sessão (ou "usar e-mail e senha" na Biometria), modo Entrar |
| 4 | `pinInicial` | Tela 0.1b — PIN inicial | A | Na Biometria, "Usar PIN" |
| 5 | `pinErro` | Tela 0.1c — PIN após falha | A | Na Biometria, simular rosto não reconhecido |
| 6 | `home` | Tela 1 — Home / Chat | A | ☰ → "CONVERSAS" → "Conversa sobre o dia no trabalho" (padrão, sem overlay) |
| 7 | `t2texto` | Tela 2 — Texto | A | Home → "+" → "Texto" |
| 8 | `t2audio_recording` | Tela 2 — Áudio — Gravando | A | "+" → "Áudio" → iniciar gravação |
| 9 | `t2audio_processing` | Tela 2 — Áudio — Processando | A | Parar a gravação; captura durante "Transcrevendo..." |
| 10 | `t2audio_transcribed` | Tela 2 — Áudio — Transcrito | A | Fim da transcrição do fixture de áudio |
| 11 | `t2audio_error` | Tela 2 — Áudio — Erro | A | Gravação de silêncio (mesmo gatilho do H02-1) |
| 12 | `t2foto_idle` | Tela 2 — Foto — Captura | A | "+" → "Foto" |
| 13 | `t2foto_processing` | Tela 2 — Foto — Processando OCR | A | "Galeria" → `ocr_fixture_01.png`; proxy segura `media-ocr` |
| 14 | `t2foto_recognized` | Tela 2 — Foto — Reconhecido | A | Fim do OCR do fixture legível |
| 15 | `t2foto_error` | Tela 2 — Foto — Erro | A | "Galeria" → `ocr_fixture_ilegivel.png` |
| 16 | `menu` | Tela 3 — Menu lateral | A | Home → ☰ |
| 17 | `sessao` | Tela 1 — Sessão expirada | A | Home; proxy forja `401 AUTH_EXPIRED` na próxima chamada (como no H07-1) |
| 18 | `registros` | Tela 4 — Meus Registros | A | ☰ → "Meus Registros" |
| 19 | `vazio` | Tela 4 — Estado vazio | C | ☰ → "Meus Registros" |
| 20 | `filtro` | Tela 4 — Sheet de filtro | A | "Meus Registros" → funil |
| 21 | `filtrosAtivos` | Tela 4 — Filtros ativos | A | Funil → "TIPO DE ENTRADA: áudio" → "Aplicar" |
| 22 | `exp_pending` | Tela 4 — Exportar — Pendente | A | Ícone de download → pedir exportação; proxy segura a primeira `export-status-get` |
| 23 | `exp_processing` | Tela 4 — Exportar — Processando | A | Idem; proxy devolve o status `processing` |
| 24 | `exp_done` | Tela 4 — Exportar — Concluído | A | Aguardar `done` com narrativa |
| 25 | `exp_error` | Tela 4 — Exportar — Erro | A | Exportação com `X-Test-Fault: ai_timeout` (como no H05-2) |
| 26 | `exp_empty` | Tela 4 — Exportar — Período vazio | C | Ícone de download → pedir exportação |
| 27 | `config` | Tela 6 — Configurações (mais de 30 entradas) | A | ☰ → "Configurações" |
| 28 | `dashZero` | Tela 6 — Dashboard zero entradas | C | ☰ → "Configurações" |
| 29 | `dashUma` | Tela 6 — Dashboard uma entrada | B | ☰ → "Configurações" |
| 30 | `dashNarrativeError` | Tela 6 — Narrativa indisponível | A | "Configurações" com `X-Test-Fault: ai_timeout` em `dashboard-narrative-get` |
| 31 | `excluir` | Tela 6 — Confirmar exclusão | A | "Configurações" → "Apagar conta" (sem confirmar) |

**Conferência:** 32 itens do catálogo − 1 de extensão = 31. As variações internas da Home (streaming, insight, falha, bookmark, offline) não são itens próprios do catálogo; ficam fora da M9, que segue o catálogo.

**Ordem de captura:** estados que chamam IA na conta A (6, 17, 22–25, 27, 30) seguem a ordem do Bloco I de `cenarios.md`, antes de qualquer escrita na conta A; 7–15 depois, no Bloco III.
