# GATE-C01 — Roteiro de revisão do `Metricas_e_Skills_Ciclos.md`

**Destino no repositório:** `cerne-avaliacao/docs/revisoes/gate-c01-roteiro-revisao.md`
**Data:** 22/09/2026
**Objeto da revisão:** o arquivo `Metricas_e_Skills_Ciclos.md` que está no conhecimento do projeto.

---

## 0. Antes de começar: o documento não é a v0

O `plano-ciclos.md` foi escrito contra uma **v0** do documento de métricas (cabeçalho do plano; Fase 0; `GATE-C01`; `GATE-C02` item 8; `GATE-C03` itens 1–2; `C-016`). O arquivo do projeto é a **revisão v2 (22/09/2026)**, que já traz:

- fundamentação bibliográfica por métrica (§5), mapeamento em Macedo (§5.6), plano de análise (§14) e referências (§15);
- o prefixo `PROCESSO:` e o arquivo `revisoes_processo.csv`, que já **resolvem** a pendência #4 (§5.1 M5; §9 regra 7);
- campos novos no prefixo de intervenção: causa (`ctx`/`chk`/`inc`/`prd`/`amb`/`out`) e nível `N1`/`N2` (§9 regra 2);
- segmentação por fase `ESPEC`/`IMPL`/`VALID` e o arquivo `segmentos.csv` (§5.1 M2, M3);
- a M8b (mutation score) como opcional;
- **11 pendências** na §13 — não 7. A #8 da v2 (M8b) colide em número com o item 8 do `GATE-C02` do plano (tags da hold-out).

**Decidido (R1-Q1, 22/09/2026): a v2 é a base da v1.0.**

Consequência para a revisão: parte do que o plano chama de "mudança sobre a v0" a v2 já fez, às vezes de outro jeito. Este roteiro separa as três situações.

**Legenda**
- `[x]` resolvido · `[~]` regra definida, caso concreto depende de GATE posterior · `[→]` adiado, com dono no plano · `[ ]` nos itens 🔁 e ✅: lista de aplicação do `C-001` (não é problema em aberto).
- 🔁 **PLAN** — trecho que o `plano-ciclos.md` altera (e onde).
- ⚠️ **DIV** — divergência entre o plano e a v2. Pela regra de precedência do plano, a fonte (v2) prevalece até você decidir.
- ❓ **LAC** — lacuna: nem a v2 nem o plano resolvem.
- ✅ — sem alteração prevista; revisar só o mérito.

---

## 1. Os seis pontos que você pediu, localizados

| # | Mudança do plano | Onde o plano muda | Trechos da v2 atingidos |
|---|---|---|---|
| 1 | ID `PLAN` | `GATE-C03` item 2; B2/B3; `C-016` | §4.1 (lista de IDs); §8 `sessoes.csv` (`id_rf`); §3.3 (falta a tag `plan-done`); §14 (pareamento por RF) |
| 2 | Série M5b | `GATE-C02` item 4; P5b; `GATE-C11`; `C-016` | §5.1 M5 (bloco "Revisão humana exigida pelo processo"); §8 (`n_processo`, `revisoes_processo.csv`); §9 regra 7; §10; §11; §13 #4 |
| 3 | JSONL como fonte primária | `GATE-C03` item 1 | §4.1 "O que faz"; §5.1 M3 "Operacionalização"; §8 "Dados brutos" (exportação OTel) |
| 4 | Skill de usuário, não de projeto | `C-011`; `C-016` | §2 P1; §3.1 (linha do app); §4.1 "Local"; §12 linha 2 |
| 5 | Convenção de tags | `C-017`; P7; `GATE-B03` | §3.3 inteira; §5.1 M1(b) e M2 (tempo de calendário); §9 regra 5 |
| 6 | Hold-out só na tag `final` | `GATE-C02` item 12 (era 8); `V-002` | §3.2 (fluxo); §4.2; §5.2 M8 (último ajuste), M10, M11, M13; §7; §8 `rf.csv`; §12 (linha "validação circular"); §14 (pareamento de M11 e M13) |

---

## 2. Roteiro seção a seção

### Cabeçalho
- [ ] 🔁 **PLAN** — "Status: rascunho" e "Revisão: v2" viram v1.0 no `C-001`.
- [x] ❓ **LAC** — *Resolvido (R1-Q3).* Numeração: a v2 passa a v1.0. Decidir como o cabeçalho registra isso (sugestão: "v1.0, congelada, derivada da revisão v2 de 22/09/2026") para a banca não ler "v1.0" como anterior à "v2".

### §2 Princípios
- [ ] 🔁 **PLAN** — P1 diz "Dentro do projeto do app existe apenas uma skill". Com a skill de usuário (`C-016`), **nenhuma** skill do instrumento fica no repositório do ciclo; ela fica em `cfg-ciclo-a`/`cfg-ciclo-b`.
- [ ] 🔁 **PLAN** — P5 (harness construído durante o Ciclo A): o plano acrescenta o repositório de calibração como único alvo de teste do harness (`GATE-C03` item 6; `H-001`) e proíbe rodar medição no código de ciclo antes da Parte IV (regra 8).
- [ ] 🔁 **PLAN** — Falta um princípio de **cegamento do pesquisador** (regra 8 do plano; `GATE-C03` item 7). Hoje ele não aparece na v2.

### §3 Arquitetura
- [ ] 🔁 **PLAN** — §3.1: a linha dos repositórios de ciclo passa a "nenhum conteúdo do instrumento"; acrescentar uma linha para os diretórios de configuração `cfg-ciclo-a`/`cfg-ciclo-b` (`C-011`).
- [ ] 🔁 **PLAN** — §3.2: o fluxo mostra `/avaliar-rf` logo após cada tag. No plano, toda avaliação acontece na Parte IV (`V-001`), e a hold-out roda só na `final` (item 12 do `GATE-C02`, aceito em R4).
- [ ] 🔁 **PLAN** — §3.3: `baseline` muda de sentido ("após `specify init`" → "pacote copiado, antes da instalação"); entram `instalado` e `rfNN-incompleto` (P7).
- [x] ⚠️ **DIV (interna ao plano)** — *Resolvido (R1-Q3): `plan-done` entra na convenção.* O `GATE-B03` cria a tag `cicloB/plan-done`, mas a convenção do `C-017` não a lista. Decidir se ela entra na §3.3.
- [→] ❓ **LAC** — *Adiado com dono: `GATE-C10`.* A §3.3 define `setup-done` do BMAD como "agentes/templates". Depende do `GATE-C10` (P-SETUP no contexto de projeto ou na arquitetura).

### §4 Skills
- [ ] 🔁 **PLAN** — §4.1 "Local": skill de usuário (`C-016`).
- [ ] 🔁 **PLAN** — §4.1 "Invocação": acrescentar `PLAN`.
- [ ] 🔁 **PLAN** — §4.1 "O que faz": JSONL primário; OTel opcional; copia o JSONL para `dados/<ciclo>/brutos/`; exibe só a confirmação e a faixa do timebox (`GATE-C03` item 7; `C-016`).
- [x] ⚠️ **DIV** — *Resolvido (R2-Q4 e R3-Q7): o `C-016` grava os dois.* §4.1 "O que faz" não menciona `segmentos.csv` nem `revisoes_processo.csv`, que a própria v2 cria (§8). O `C-016` do plano também não os menciona. Hoje nenhum dos dois documentos diz quem grava esses arquivos.
- [x] ❓ **LAC** — *Resolvido (R4-Q12): soma principal + subagentes.* **Transcripts de subagentes.** Se o Claude Code grava subagentes em arquivos JSONL separados do transcript principal (verificar na versão travada), um script que lê só o arquivo da sessão **subconta tokens justamente onde há mais delegação** — é o confundimento de topologia da M3. Isso afeta o item 1 (fonte primária) e o item 4 (cópia dos brutos) do `GATE-C03`.
- [ ] 🔁 **PLAN** — §4.2: "Após a tag `rfNN-done`" vira "na Parte IV, sobre as tags" (regra 8); build a partir da tag com `.env` injetado (`V-002` passo 0).
- [x] ❓ **LAC** — *Resolvido (R6-Q17): o mapa é insumo da `/julgar-rf` do B.* §4.3 (`/julgar-rf`) no Ciclo B: "architecture/stories correspondentes" pressupõe o `mapa-stories.csv` do `GATE-B03`, que a v2 não cita.
- [ ] 🔁 **PLAN** — §4.4: acrescentar a linha de planejamento global (`PLAN`) e a série M5b.
- [ ] ✅ §4.5.

### §5.1 Métricas de processo
**M1**
- [x] 🔁 **PLAN** — *Confirmado (R5-Q15).* O plano soma à M1 o tempo de instalação cronometrado fora de sessão (`instalar-metodologia`, `tipo_sessao = instalacao`, `C-017`).
- [x] ❓ **LAC** — *Resolvido (R5-Q15): M1 = instalação + sessões `SETUP`, componentes e calendário lado a lado.* A v2 define M1(a) como "tempo em sessão". A instalação não é sessão. Decidir se ela entra em M1(a), em M1(b) ou numa terceira medida.
- [~] ❓ **LAC** — *Regra definida (R5-Q15): a definição da M1 declara a assimetria; o caso concreto depende do `GATE-C10`.* Assimetria de setup no BMAD se o `P-SETUP` for para a arquitetura (`GATE-C10`): precisa de uma frase na definição.

**M2**
- [ ] 🔁 **PLAN** — Linha de planejamento global `PLAN` (`GATE-C03` item 2).
- [x] ⚠️ **DIV** — *Resolvido (R3-Q7): mantida; tabela no `C-004`.* Segmentação por fase e `segmentos.csv` (v2) não aparecem no plano: nem no `C-016`, nem no `GATE-C10`, nem na Fase 7. A tabela comando/persona → fase é a pendência #9 da v2 e não tem dono no plano.
- [x] ❓ **LAC** — *Resolvido (R3-Q9).* **Timebox (P7) censura a M2**: um RF encerrado em 8 h tem tempo verdadeiro desconhecido (≥ 8 h). A §14 precisa de regra para RF incompleto no pareamento.

**M3**
- [ ] 🔁 **PLAN** — OTel primário → JSONL primário.
- [ ] ✅ `config_raciocinio` (coerente com P1b do plano).
- [x] ❓ **LAC** — *Resolvido (R4-Q12).* Subagentes: ver §4.1 acima.

**M4**
- [x] ⚠️ **DIV** — *Resolvido (R6-Q18): dono é o `C-022`.* A v2 diz "lista de tipos contáveis congelada no protocolo", mas nenhuma tarefa do plano produz essa lista.
- [x] ❓ **LAC** — *Resolvido (R6-Q18): no B, lida em `plan-done` e `final`, regra no `C-022`.* No BMAD, os artefatos nascem nas sessões `PLAN`. Contar "na tag de cada RF" dá zero incremental por RF no B. Registrar que a M4 do B se lê em `plan-done` e `final`.

**M5**
- [x] ⚠️ **DIV (principal)** — *Resolvido (R2-Q4): prefixo `PROCESSO:`; M5b = `n_processo`.* A v2 marca as respostas à metodologia com `PROCESSO:` (§9 regra 7) e as grava em `revisoes_processo.csv`. O plano as trata como **mensagens neutras, sem prefixo** (P5b) e as conta como M5b "conforme a regra do `GATE-C11`" (`C-016`). Sem prefixo, o script não tem como distinguir uma resposta à metodologia de uma mensagem livre. Os dois desenhos só convivem se M5b = contagem das linhas `PROCESSO:` (que a v2 já grava em `n_processo`).
- [x] ⚠️ **DIV** — *Resolvido (R2-Q5): `PROCESSO` = resposta a pausa prevista pela metodologia.* A v2 inclui "aprovação de plano" entre os gatilhos `PROCESSO`; o plano classifica "sim", "pode seguir" como confirmação neutra (P5b). É preciso dizer onde termina uma e começa a outra.
- [x] ⚠️ **DIV** — *Resolvido (R2-Q6): formato completo da v2.* Formato do prefixo: v2 §9 regra 2 exige causa (e severidade ou nível, conforme o tipo). O plano (regra 7; `C-016`) só fala em `INTERVENÇÃO [tipo]` e `INTERVENÇÃO [correção|Sn]`.
- [~] ❓ **LAC** — *Dono definido: `C-004` (R2-Q5). Menus do BMAD ficam para o `GATE-C10`/`C11`.* Lista de gatilhos `PROCESSO` por framework: a v2 exige congelar (§11), o plano não tem tarefa para isso. No BMAD, conferir na versão travada os menus que os workflows apresentam a cada passo (continuar / elicitação avançada etc.) e decidir a resposta padrão e se conta como `PROCESSO` ou neutra.

**M6**
- [x] ❓ **LAC** — *Resolvido (R6-Q17): checkboxes das stories da unidade, via `mapa-stories.csv`.* `M6_tasks` ("% de itens marcados no `tasks.md`") não tem equivalente definido para o BMAD.
- [x] ⚠️ **DIV** — *Resolvido (R6-Q18): dono é o `C-022`.* As regex de referências inexistentes (pendência #10 da v2) e o hash da Especificação Técnica usada como referência não aparecem no plano (a Fase 7 não os cita).

### §5.2 Métricas de produto
**M7**
- [ ] 🔁 **PLAN** — Pendência #1: ⭐ script próprio do harness (`GATE-C02` item 1). Mapa de camadas vem da convenção de pastas (P8).
- [x] ❓ **LAC** — *Resolvido (R6-Q16): só na M11; a M7 fica com o RNF06.* As regras estruturais do RF07 ("nenhum BLoC importa outro") e do RF10 são aplicadas pelo script da M7 (plano) **e** contadas na M11 (v2, §5.2 M11). Decidir onde contam, para não contar duas vezes.

**M8**
- [x] ⚠️ **DIV** — *Resolvido (R4-Q11): só na `final`, condicionada à calibração até 06/11.* M8b (pendência #8 da v2) estava ausente do plano.
- [x] ⚠️ **DIV** — *Resolvido (R4-Q10): parágrafo reescrito no `C-001`.* O último ajuste da M8 diz que "a evidência de qualidade funcional vem da M11 e da M13, **ambas medidas pela suíte hold-out**". Se a hold-out rodar só na `final`, a M13 deixa de ser medida por ela, e o argumento contra a validação circular perde metade da base. Se o item 8 for aceito, este parágrafo e a linha correspondente da §12 precisam mudar.

**M9**
- [ ] 🔁 **PLAN** — Pendência #7 fecha pela P10 (estados de extensão fora) e P11 (dispositivo).
- [ ] ✅ Mecanismos D/J.

**M10**
- [x] 🔁 **PLAN** — *Confirmado (R4-Q10); `C-002` ajustado.* Com hold-out só na `final`, `M10_cenarios` passa de métrica por RF a métrica por ciclo. Ajustar `rf.csv`.

**M11**
- [x] 🔁 **PLAN** — *Confirmado (R4-Q10); mudança de construto declarada no `C-001`.* Com hold-out só na `final`, a M11 por RF mede "o RF funciona no app final", não "funcionava quando foi entregue". Declarar essa mudança de construto.

**M12**
- [ ] 🔁 **PLAN** — Pendência #2: ⭐ script próprio sobre o `package:analyzer` (`GATE-C02` item 2).

**M13**
- [x] 🔁 **PLAN** — *Confirmado (R4-Q10).* Hold-out só na `final` → M13 só com a suíte do agente, tag a tag. Observação: isso **volta** à definição original da §8.2 dos requisitos ("roda a suíte completa do RNF07 a cada RF"); foi a v2 que acrescentou a hold-out na M13.
- [x] ⚠️ **DIV** — *Resolvido (R1-Q3).* O `C-002` mandava "acrescentar `M13_apagados`", mas a coluna já existe na v2 (§8).

### §5.3 Métricas diferenciais
- [→] ❓ **LAC** — *Adiado com dono: `C-022`.* M14: no Spec Kit há um `plan.md` por unidade (11); no BMAD, uma arquitetura global. O critério de seleção (`C-022`) precisa dizer de qual artefato saem as 8–10 decisões em cada ciclo.
- [ ] ✅ M15.

### §5.4 D16 e §6 Avaliador
- [x] ⚠️ **DIV** — *Resolvido (R5-Q13): outra família, com visão.* Família do avaliador: a v2 (§6) recomenda **outra família** (Taghavi & Bhavani; Baltes et al.). O ⭐ do plano (`GATE-C02` item 6) é "um modelo Claude diferente do usado nos ciclos". Observação: o avaliador da M9 precisa de visão.
- [x] ⚠️ **DIV** — *Resolvido (R5-Q14): regra da v2 + rótulo "exploratória".* κ abaixo do limiar: a v2 (§5.4, §6) diz "J reportado com ressalva, humano ao lado" (e, na D16, humano como primário). O ⭐ do plano diz "métrica vira exploratória e a amostra humana vira o dado principal". São regras parecidas, mas não iguais; só uma pode ser congelada.

### §7 Suíte hold-out
- [x] 🔁 **PLAN** — *Confirmado (R4-Q10).* Execução só na `final` (item 12); estratégia de cache `record` no ciclo-a → importação no ciclo-b → `replay_strict` (`GATE-C19`; `V-002`).
- [ ] ✅ O corte do stream SSE do RF04 continua necessário: é critério de aceite do RF04, então entra no `C-018` (M11), não no `C-019` (M10).

### §8 Dados
- [ ] 🔁 **PLAN** — `id_rf` aceita `PLAN`; coluna `tipo_sessao`; `tags.csv` (`C-017`); `mapa-stories.csv` (`GATE-B03`); `brutos/`; OTel passa a opcional.
- [x] ⚠️ **DIV** — *Resolvido (R2-Q4).* `n_processo` (v2) e "série M5b" (plano) são o mesmo dado com dois nomes.

### §9 Regras operacionais
- [x] ⚠️ **DIV** — *Resolvido (R2).* Regra 2 (campos do prefixo) e regra 7 (`PROCESSO:`) × regra 7 e P5b do plano. Ver M5.
- [x] ❓ **LAC** — *Resolvido (R7-Q20): só no `protocolo.md`; a §9 remete.* Regras novas do plano (sintoma, nunca solução; RDR; não editar artefatos; timebox): decidir se entram aqui ou só no `protocolo.md`, com remissão.

### §10 Resíduo manual
- [ ] 🔁 **PLAN** — Acrescentar: consultar e atualizar o RDR (`GATE-C11`), mapear stories (`GATE-B03`), acompanhar a faixa do timebox.

### §11 Cronograma do instrumento
- [x] ⚠️ **DIV** — *Resolvido: gatilhos e fases no `C-004` (R2, R3); regex da M6 e tipos da M4 no `C-022` (R6); M8b decidida (R4); zeros do Wilcoxon por Pratt (R7).* Itens que a v2 manda congelar e que não têm tarefa no plano: lista de gatilhos `PROCESSO`; tabela comando/persona → fase; regex da M6 e hash da Especificação Técnica; lista de tipos contáveis da M4; decisão sobre a M8b; regra de diferenças nulas do Wilcoxon (§14).

### §12 Ameaças
- [ ] 🔁 **PLAN** — Acrescentar as do plano: spike do `whisper_ggml` (`GATE-C16`); assimetria de setup do BMAD (`GATE-C10`); modelo de subagentes não travável (P1c); aprendizado prévio (`GATE-X02`); hold-out só na `final`; exibição de números pela coleta, se você optar por vê-los (`GATE-C03` item 7).
- [x] ❓ **LAC** — *Resolvido (R3-Q9); entra também como ameaça na §12 da v1.0.* Censura pela timebox (ver M2).

### §13 Pendências
- [x] ⚠️ **DIV** — *Resolvido (R1-Q2): lista unificada, 12 itens.* Reconciliar as 11 da v2 com os 8 itens do `GATE-C02` (o título do GATE diz "7") e os 7 do `GATE-C03`.

### §14 Plano de análise
- [x] ❓ **LAC (grave)** — *Resolvido (R3-Q8): par principal só em `IMPL` + `VALID`; `ESPEC` no nível do ciclo.* **Pareamento por RF com `PLAN` fora.** No Spec Kit, o tempo e os tokens de especificação de cada RF estão dentro do RF; no BMAD, estão nas sessões `PLAN`, fora do par. Comparar M2/M3 por RF assim compara "especificação + implementação" (A) com "só implementação" (B). Opções para pré-registrar: parear só a fase `IMPL` (exige a segmentação da v2); ratear o `PLAN` entre os RFs; ou reportar as duas leituras.
- [x] ❓ **LAC** — *Resolvido (R3-Q9).* RF incompleto no pareamento (censura).
- [ ] ✅ §15.

---

## 3. Registro das respostas

| Rodada | Pergunta | Decisão | Data | Onde foi aplicado |
|---|---|---|---|---|
| R1 | Q1 — Base da v1.0 | Revisão v2 do arquivo do projeto | 22/09/2026 | `plano-ciclos.md`: cabeçalho, Fase 0, `GATE-C01`, `GATE-C02` item 12, `GATE-C03` itens 1–2, `C-016` ("v0" → "v2") |
| R1 | Q2 — Escopo do `GATE-C02` | Unificar: pendências #1–#11 da v2 + tags da hold-out como #12, na numeração da v2 | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` (título, itens 8–12, critério) |
| R1 | Q3 — Correções editoriais | As quatro aprovadas: cabeçalho "v1.0 derivada da v2"; `plan-done` na convenção; título do `GATE-C02` e `C-002` sem `M13_apagados`; `C-000` com `.gitignore`, `evidencias/`, `brutos/`, `segredos/` | 22/09/2026 | `plano-ciclos.md`: `GATE-C02`, `C-000`, `C-002`, `C-017`. Cabeçalho da v1.0 aplicado no `C-001` |
| R2 | Q4 — Marcação das respostas à metodologia | Prefixo `PROCESSO:` (v2, §9 regra 7); M5b = `n_processo`, detalhe em `revisoes_processo.csv` | 22/09/2026 | `plano-ciclos.md`: regra 7, `GATE-C02` item 4, P5b, `GATE-C11` (passo 0), `C-016`, `GATE-C21`, bloco A passo 3 |
| R2 | Q5 — Fronteira `PROCESSO` × neutra | `PROCESSO` = resposta a pausa prevista pela metodologia (lista de gatilhos congelada); neutra = confirmação a pausa espontânea do agente | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 4, P5b, bloco A passo 6, `C-004` (dono da lista) |
| R2 | Q6 — Formato do prefixo | Completo da v2: `tipo\|Sn\|N1-N2\|causa` | 22/09/2026 | `plano-ciclos.md`: regra 7, P5, `C-016`, blocos A e B (verificação), `GATE-B03`, `GATE-B04` |
| R3 | Q7 — Segmentação por fase | Mantida; tabela comando/workflow → fase congelada no `C-004`; `C-016` grava `segmentos.csv` | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 9, `C-004`, `C-016` |
| R3 | Q8 — Pareamento com `PLAN` fora | Par principal por RF só em `IMPL` + `VALID`; `ESPEC` comparada no nível do ciclo (Σ `ESPEC` A × `PLAN` + `ESPEC` B) | 22/09/2026 | `plano-ciclos.md`: `C-001` (§14 da v1.0) |
| R3 | Q9 — Censura pela timebox | RF incompleto entra no par com o teto, marcado como censurado; sensibilidade sem os censurados | 22/09/2026 | `plano-ciclos.md`: P7, `C-001` (§14), `C-002` (`timebox_censurado`) |
| R4 | Q10 — Tags da hold-out | Só na `final`; M13 com a suíte do agente; parágrafo da M8 reescrito; ameaça nova na §12 | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 12, `C-002` |
| R4 | Q11 — M8b | Adotada só na `final`, se funcionar na calibração até 06/11; senão, ameaça declarada | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 8, `H-001` (mutante plantado), `H-002`, `GATE-H01`, `C-002` |
| R4 | Q12 — Subagentes | Soma principal + subagentes; todos copiados para `brutos/`; teste com transcript sintético com subagente | 22/09/2026 | `plano-ciclos.md`: `GATE-C03` itens 1 e 4, `C-016` (critério com 4 transcripts), `C-002` |
| R5 | Q13 — Família do avaliador | Outra família, com visão, via API de outro fornecedor (v2 §6); ID exato ainda em aberto | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 6 |
| R5 | Q14 — κ abaixo do limiar | Regra da v2 + rótulo "exploratória": J com ressalva e humano ao lado; D16 com humano primário; nada trocado após ver dados | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 6, `C-001` |
| R5 | Q15 — Instalação na M1 | M1 = instalação + sessões `SETUP`; componentes e calendário lado a lado; assimetria do BMAD declarada | 22/09/2026 | `plano-ciclos.md`: `C-017`, `C-001` |
| R6 | Q16 — RF07/RF10 na M7 ou na M11 | Só na M11; a M7 fica só com a regra do RNF06; mesmo script, duas saídas | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 1, `H-002` |
| R6 | Q17 — `M6_tasks` no BMAD | % de checkboxes marcados nas stories da unidade, via `mapa-stories.csv`; formato confirmado na versão travada | 22/09/2026 | `plano-ciclos.md`: `C-022`, `GATE-B03`, `H-002` |
| R6 | Q18 — Dono das regex da M6 e dos tipos da M4 | Ampliar o `C-022` (Fase 7) | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 10, `C-022` |
| R7 | Q19 — Opcionais da v2 | Nenhum adotado; estimativa prévia e estabilidade da M14 viram trabalho futuro | 22/09/2026 | `plano-ciclos.md`: `GATE-C02` item 11 |
| R7 | Q20 — Onde ficam as regras operacionais | Só no `protocolo.md` (seção "Regras operacionais"); a §9 da v1.0 fica com as regras de dados e remete | 22/09/2026 | `plano-ciclos.md`: `C-003`, `C-001` |
| R7 | Q21 — Zeros no Wilcoxon | Método de Pratt | 22/09/2026 | `plano-ciclos.md`: `C-001` (§14) |

## 4. Observações do Wagner

**Nenhuma** (22/09/2026). `GATE-C01` fechado.
