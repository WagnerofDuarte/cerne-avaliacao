# Plano: completar as métricas M6 a M15 ainda hoje (08/11/2026)

**Objetivo.** Chegar às 23h59 com a monografia contendo o máximo de métricas de produto e diferenciais coletadas, cada uma com o método realmente usado, e com o que não coube declarado. **Meta honesta:** completar todas as partes que não dependem do aparelho (iPhone) e do avaliador externo; as partes que dependem de execução no aparelho (hold-out de caixa-preta) não cabem hoje e ganham um substituto declarado, ou ficam "não avaliadas".

**Regras que não mudam** (regra 8 e `GATE-H02`): nenhuma métrica de produto é calculada sobre os repositórios finais antes de o harness ser congelado (hashes registrados e tag `harness-v1.0`, do pesquisador). Nenhum limiar, regra de contagem ou rubrica muda depois de ver resultado. Tudo que mudar de método é registrado como desvio **antes** de rodar.

---

## 1. Ponto de partida

| Item | Estado |
|---|---|
| M1 a M5, M4, análise pareada | Prontos (monografia, seção 4.4 e 4.8) |
| Harness (branch `harness`) | 11 módulos estáticos + CLI Dart da M12 + avaliador + 4 skills, testados **só no repositório de calibração**; Maestro/mitmproxy/SQL prontos mas nunca rodaram em aparelho |
| Repositórios finais | `cerne-ciclo-a` e `cerne-ciclo-b` clonados aqui, com todas as tags (as 4 que faltavam no B acabaram de ser buscadas) |
| Ferramentas | `claude -p` (modo sem tela) funciona aqui e devolve o **ID exato do modelo** e o custo (`modelUsage`); Flutter 3.47.9/Dart 3.13.7 foram instalados pela sessão do harness em outro container, e a rede libera `storage.googleapis.com` e `pub.dev` |
| Tamanho dos apps (tag `final`) | A: 167 arquivos em `lib/`, 80 arquivos de teste. B: 132 em `lib/`, 96 de teste |
| Sem aparelho | Não há iPhone, simulador nem Maestro aqui; o app não compila para simulador (`whisper_ggml`, D de 03/11) |

---

## 2. O que muda no método (desvios a registrar antes de rodar)

| Nº (a registrar) | Mudança | Por quê | Efeito/ameaça |
|---|---|---|---|
| **D-099** | **Avaliador LLM: de `gpt-5.5-2026-04-23` (OpenAI) para um modelo Claude diferente do gerador**, chamado por `claude -p --model <ID>` em diretório neutro, sem ferramentas, com os **mesmos prompts e schemas congelados** de `harness/juiz/`. Modelo: `claude-opus-5-5` (decisão do pesquisador em 08/11: **somente** Opus 5.5; o agente dos ciclos foi `claude-sonnet-5`) | Não há chave da OpenAI no ambiente e o prazo não comporta obtê-la; o próprio documento de métricas (§6) já prevê o fallback: "manter um avaliador Claude, ampliar a amostra humana e registrar a ameaça como não mitigada" | **Viés de autopreferência não mitigado por família** (mesmo fornecedor do gerador). Mitigações: modelo ≠ do gerador, anonimização, 3 execuções, cegamento do rótulo do ciclo, e rotular os resultados J como **exploratórios** até a validação humana (§6 do documento de métricas, regra do κ). Se houver chave OpenAI depois, repetir os itens como checagem cruzada |
| **D-100** | **Hold-out de caixa-preta não é executado hoje.** M10 (15 cenários), M11 (28 cenários) e a parte por imagem da M9 (cor por pixel, espaçamento ±4dp) ficam fora, com substitutos (ver §3) | Maestro não roda em iPhone físico e o app não compila no simulador; o plano B (checklist manual) leva 2 a 2,5 h por ciclo, mais mitmproxy, reset do ambiente e esperas reais | M11 e M10-cenários ficam sem medida independente; declarado como limitação central |
| **D-101** | **Congelamento parcial (`GATE-H02`)**: congela-se só o que será usado hoje (`harness/estatico/`, `harness/m12/`, `harness/m9/` (hardcodes), `harness/avaliador/`, `harness/juiz/`, `harness/regras.md`, `harness/precos.md`). `holdout/` não é congelado nem usado | Menos itens para conferir antes da tag | Hash do conjunto congelado é registrado; o resto fica para a Parte IV completa |
| **D-102** | **M9 estático**: cor primária e tipografia comparadas por **tokens** (`design_tokens.dart` × tokens do protótipo), não por pixel nem por árvore de widgets; espaçamento ±4dp **não avaliado** | Sem aparelho, não há screenshots | M9 vira "disciplina de tokens", não "fidelidade renderizada" (construto mais fraco, declarado) |
| **D-103** | **M11 substituto**: (a) critérios estruturais do RF07 e RF10 pelo script da M7 (como previsto) e (b) registro da **P6** de cada unidade (verificação manual do pesquisador no fechamento: critérios atendidos), reportado como **M11-P6**, dado não cego, no momento da entrega | A P6 já existe nos dois ciclos e cobre os critérios de aceite | Executor = pesquisador, sem cegamento, na entrega (não na tag `final`); rotular assim |
| **D-104** (se necessário) | **M8b por amostra**: se a mutação completa passar de 45 min por ciclo, usar amostra de mutantes com semente fixa (registrada) ou declarar "não avaliada" | O módulo foi validado com 17 mutantes e 10 testes; o tamanho real é desconhecido | Poder menor; ou ausente |

Os números D-099 a D-104 são provisórios. O texto de cada desvio sai deste quadro.

---

## 3. Plano por métrica

Legenda de prioridade: **P0** estático e barato (sem aparelho, sem juiz); **P1** exige executar `flutter test`; **P2** juiz Claude; **P3** exige aparelho. Tempo = estimativa de relógio, com tarefas em paralelo.

| Métrica | Como o protocolo previa | O que faremos hoje | Prio. | Quem | Tempo | Se falhar |
|---|---|---|---|---|---|---|
| **M6-D** (tarefas concluídas, citados×alterados, inexistentes) | Script sobre `tasks.md`/`plan.md` (A) e stories + `mapa-stories.csv` (B) | Rodar por unidade, com os formatos reais; ajustar **parâmetros** (caminhos, nomes), nunca a regra, **antes** do congelamento | P0 | Eu | 30 min | Reportar só as categorias que o formato real permitir; declarar |
| **M6-J** (divergências não documentadas) | gpt-5.5, 3 execuções, voto | Claude Opus 5.5, 22 itens (11 unidades × 2 ciclos; RF02 do B = 0) × 3 execuções, voto majoritário; **exploratório** | P2 | Eu | 40 min | Sem maioria → fila de validação humana |
| **M7** (violações de camada) | Script Python do harness | Todas as tags dos dois ciclos (trajetória por RF) | P0 | Eu | 15 min | — |
| **M8** (cobertura do domínio) | `flutter test --coverage` na tag `final` | Instalar Flutter/Dart aqui, `pub get`, rodar nas duas tags `final` | P1 | Eu | 40 min | Se o `pub get` falhar por versão, reportar cobertura "não obtida" e a causa |
| **M8b** (mutação) | Módulo próprio, só na `final` | Rodar nas duas `final` com teto de 45 min por ciclo (D-104) | P1 | Eu | 90 min (paralelo) | Amostra ou "não avaliada" |
| **M9-hardcodes** | Script estático, toda tag | Todas as tags | P0 | Eu | 15 min | — |
| **M9-cor/tipografia** | Pixel e árvore de widgets | Tokens × protótipo (D-102) | P0 | Eu | 20 min | — |
| **M9-espaçamento** | Juiz com visão sobre screenshots | **Não avaliada** (sem screenshots) | P3 | — | — | Declarar |
| **M10-assinaturas** (padrão `Either`) | Script estático | Todas as tags | P0 | Eu | 10 min | — |
| **M10-cenários** (15 falhas) | mitmproxy + Maestro | **Não avaliada hoje** (D-100) | P3 | — | — | Declarar; checklist manual fica como trabalho futuro |
| **M11** (critérios de aceite) | Hold-out na `final` | Estrutural RF07/RF10 (script) + **M11-P6** (D-103); **sem** hold-out | P0 | Eu | 40 min para extrair a P6 do registro | Declarar construto reduzido |
| **M12** (complexidade) | CLI Dart | Rodar nas duas `final` (e nas tags, se sobrar tempo) | P0 | Eu | 20 min | — |
| **M13** (regressão) | `flutter test` da suíte do agente em cada tag de unidade | 11 tags × 2 ciclos = 22 execuções; IDs de testes aprovados por tag; taxa com e sem apagados | P1 | Eu | 60–90 min (paralelo) | Reportar as tags que rodaram e declarar as que não |
| **M14** (fidelidade de handoff) | 10 decisões por critério pré-registrado; checks D + juiz J | Extrair as 10 decisões por ciclo aplicando o critério congelado (`C-022`), checks estáticos onde houver, juiz Claude nas demais (20 itens × 3), **exploratório** | P0+P2 | Eu (+ você confere a lista das 20 decisões, 10 min) | 50 min | Só a parte D |
| **M15** (consistência) | Script, 4 convenções, referência RF01 | Todas as features das duas `final` | P0 | Eu | 15 min | — |
| **Validação do juiz (κ)** | ≥20 itens por métrica, cego, você classifica | Validação humana só da **M14** (20 decisões, cerca de 1 h), "se couber"; M6-J sem validação humana hoje | P2 | Você (opcional) | 60 min | Resultados J ficam exploratórios (regra do documento de métricas) |
| D16 (log auxiliar) | Juiz sobre 54 correções | **Fora de hoje** (não é métrica numerada) | — | — | — | — |

### O que isso entrega

- **Completas (método do protocolo, com a ressalva de tooling):** M6-D, M7, M8, M9-hardcodes, M10-assinaturas, M12, M13, M15 e a parte D da M14.
- **Completas com método alterado e rótulo "exploratório":** M6-J e M14-J (juiz Claude).
- **Com construto reduzido:** M9 (tokens), M11 (estrutural + P6), M8b (se couber).
- **Não avaliadas (declaradas):** M9-espaçamento, M10-cenários e M11 de caixa-preta.

---

## 4. Desenho do juiz Claude (D-099)

1. **Entrada.** Para cada item, `harness/avaliador/` monta o texto exato da rubrica congelada (`harness/juiz/m6-aderencia.md`, `m14-handoff.md`) + o material **anonimizado** (rótulo `X`/`Y` aleatório; diretórios e termos da metodologia trocados conforme `anonimizacao.txt`, que a sessão do harness escreveu de memória e que preciso **conferir contra a instalação real** antes de congelar).
2. **Chamada.** `cd /tmp/juiz && claude -p "<entrada>" --model claude-opus-5-5 --output-format json --max-turns 1`, sem ferramentas, sem `CLAUDE.md`, sem skills nem conectores (diretório neutro e `--setting-sources` vazio), em paralelo (8 a 10 por vez). Cada resposta fornece `modelUsage` com o **ID canônico do modelo** e o custo, gravados em `julgamentos.jsonl` junto com data, parâmetros e hash do prompt.
3. **Validação do schema.** Resposta fora do schema = execução inválida, repetida uma vez; se falhar de novo, o item vai para a fila humana.
4. **Voto.** 3 execuções por item, maioria; sem maioria → fila humana.
5. **Sem segundo juiz** (decisão do pesquisador). A estabilidade é medida só pela concordância entre as 3 execuções do mesmo modelo. A validação humana (M14, 20 decisões) fica **opcional**, "se couber".
6. **Rótulo.** Todo resultado J sai como **exploratório** (κ humano pendente), ao lado do resultado D da mesma métrica. Nenhuma troca de modelo ou rubrica depois de ver resultado.
7. **Ameaça a declarar:** autopreferência (mesmo fornecedor do gerador), além do viés próprio do avaliador e da dependência de um fornecedor.
8. **Custo estimado:** cada chamada tem cerca de US$ 0,09 só de contexto base mais a entrada; cerca de 130 a 200 chamadas ⇒ ordem de US$ 20 a 60 a preço de lista. Sai da sua assinatura.

---

## 5. Sequência de hoje (horário de Brasília) e pontos de corte

| Hora | Passo | Quem | Corte |
|---|---|---|---|
| 18h00–18h30 | Decisões do §6; desvios D-099 a D-104 escritos em `docs/desvios.md`; mesclar a branch `harness` na `cicloA` (ou copiar só o escopo de D-101); instalar Flutter/Dart; buscar tags | Eu (+ você decide) | — |
| 18h30–19h00 | **Conferência de formato, sem rodar métrica**: caminhos de `plan.md`, `tasks.md`, `_bmad-output`, `mapa-stories.csv`, `anonimizacao.txt` | Eu | Se algo exigir mudar **regra** (não parâmetro), a métrica sai |
| 19h00 | **Congelamento**: hashes do escopo de D-101 em `docs/hashes-congelamento.md`; você cria a tag `harness-v1.0` (eu passo os comandos ou executo se você autorizar) | Você + eu | **Sem tag, nada de produto roda** (volto ao texto atual) |
| 19h00–19h45 | P0 em todas as tags: M6-D, M7, M9-hardcodes/tokens, M10-assinaturas, M11-estrutural, M12, M15 | Eu | — |
| 19h00–21h00 | P1 em segundo plano: M13 (22 execuções), M8 e M8b (`final`) | Eu | **21h00**: o que não terminou é declarado "não avaliado" |
| 19h45–20h45 | P2: seleção das 10 decisões da M14 por ciclo (você confere a lista em 10 min), M6-J e M14-J, segundo juiz | Eu | **20h45**: itens pendentes ficam "sem resultado J" |
| 21h00 | **Congelar os dados**: gerar `dados/produto/*.csv` e `docs/resultados-produto.md` | Eu | — |
| 21h00–22h15 | Escrever na monografia: 4.5, 4.6, 4.7, ajuste de 5.1 a 5.3, 6.2/6.3 se mudar, 7.1, 7.3, Resumo/Abstract, Apêndice F, Quadro 19 | Eu | **22h15**: texto final |
| 22h15–23h45 | Sua revisão | Você | — |

**Regra de parada.** Se às 19h00 a tag não existir, ou às 21h00 menos de 6 das 14 linhas de métrica estiverem computadas, **abandono a coleta** e a monografia fica como está (já é entregável). Nenhuma meia coleta entra no texto sem declaração.

---

## 6. O que preciso de você

1. **Aprovar o plano e os desvios** D-099 a D-104 (ou cortar algum).
2. ~~Escolher o modelo do juiz~~ **Decidido: `claude-opus-5-5`, sem segundo juiz.**
3. ~~Chave da OpenAI~~ **Decidido: não será usada hoje.**
4. **Autorizar a tag `harness-v1.0`** por volta das 19h, depois de eu mostrar os hashes e explicar o que ela faz. Você disse que não sabe fazer: **eu executo e narro cada passo; você só diz "pode criar" no chat.**
5. **Conferir a lista de 10 decisões da M14 por ciclo** (cerca de 10 min, às 19h45).
6. **"Sim, se couber" (decidido):** classificar às cegas as 20 decisões da M14 (cerca de 1 h), entre 20h30 e 21h30, numa planilha que eu preparo sem o voto do juiz. Se atrasar, vale o corte das 21h30 e a M14-J fica exploratória.
7. **Opcional e pouco provável hoje:** executar no iPhone uma amostra do checklist manual (um cenário por RF + 3 falhas, cerca de 45 min por ciclo mais a preparação do mitmproxy). Só vale se você quiser trocar a sua revisão por isso; eu desaconselho.

---

## 7. Riscos

| Risco | Probabilidade | Resposta |
|---|---|---|
| Versão do Flutter/Dart diferente da usada no Mac quebra `pub get` ou `flutter test` em tags antigas | Média | Reportar o que rodou; M13 por tag disponível |
| M8b muito lento | Alta | Teto de 45 min e amostra com semente fixa (D-104) |
| Formato real do BMAD/`mapa-stories.csv` exige mudar a regra do M6/M4 | Média | A parte afetada sai (declarada) |
| Autopreferência do juiz Claude | Certa | Declarada; resultados J exploratórios; checagem cruzada com segundo modelo |
| Chamadas `claude -p` limitadas por quota da assinatura | Média | Reduzir paralelismo; priorizar M14-J |
| Tempo | Alta | Pontos de corte do §5; texto final às 22h15 |
| Cegamento: o pesquisador e o guia já conhecem o mapeamento A/B | Certa | O cegamento vale para o **juiz** (anonimização), não para os humanos; declarar |

---

## 8. Depois de hoje (pós-entrega, já previsto no plano original)

Hold-out completo (Maestro/mitmproxy/SQL ou checklist manual no iPhone), M9 por imagem, M10-cenários, validação humana do juiz com κ, repetição dos itens J no `gpt-5.5-2026-04-23`, D16.
