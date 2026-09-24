# Regras concretas do harness (M4, M6, M14, M15)

**Destino:** `cerne-avaliacao/harness/regras.md` · **Tarefa:** `C-022` · **Versão:** v1.0 (24/09/2026)
Cada regra é implementada na trilha paralela e testada **só** no repositório de calibração (`H-001`), cujo gabarito tem casos para todas elas.

---

## 1. M14 — seleção das 8–10 decisões

**Artefatos-fonte (decidido em 24/09/2026):**
- **Ciclo A (Spec Kit):** `.specify/memory/constitution.md` e o `plan.md` da unidade F000 (`specs/<F000>/plan.md`), nessa ordem — as decisões globais que as unidades seguintes herdam.
- **Ciclo B (BMAD):** o documento de arquitetura produzido pelo `bmad-architecture`.

Os artefatos são lidos na tag `final`.

**Candidata a decisão:** cada item de lista ou frase de um parágrafo, nas seções de decisões técnicas do artefato, que cumpra **todas** as condições:
1. afirma uma escolha técnica (verbo de prescrição ou de fato: *use, must, should, will, is implemented with, lives in, never*, ou equivalentes);
2. contém ao menos um **identificador concreto**: nome de pacote (`` `[a-z0-9_]+` `` presente no pub.dev ou no `pubspec.yaml`), nome de classe ou padrão (`[A-Z][A-Za-z0-9]+` com sufixo `Bloc`, `Cubit`, `Repository`, `UseCase`, `Service`, `DataSource`, `Failure`, `Client`, `Store`), ou caminho (`lib/…`);
3. é consumida na implementação — refere-se a código de `lib/`, não a processo, documentação ou testes;
4. **não repete** uma restrição fixada no pacote de entrada (P8: `flutter_bloc`, Clean Architecture em três camadas, `fpdart`/`Either`, `mocktail`, `whisper_ggml`, `design_tokens.dart`, convenção de pastas, iOS) — essas são medidas por M7, M10 e M15, não por handoff.

"Seções de decisões técnicas": no `plan.md` do Spec Kit, as seções "Technical Context", "Project Structure" e outras de decisão técnica do template da versão travada; na constitution, os princípios; na arquitetura do BMAD, todas as seções, exceto introdução, glossário e changelog.

**Seleção:** as candidatas, na ordem em que aparecem (Ciclo A: constitution, depois `plan.md` da F000), deduplicadas; ficam as **10 primeiras**. Com menos de 8 candidatas, entram todas, e o número é registrado.

**Verificação:** parte D quando a decisão vira um check estático (ex.: "X nunca importa Y" → regra de import); parte J (rubrica `juiz/m14-handoff.md`) nas demais.

---

## 2. M15 — consistência de padrões entre features

**Referência (decidido em 24/09/2026):** a feature que implementa o **RF01** (a que contém o fluxo de criação de entradas), identificada na tag `rf01-done` pelo diretório `lib/features/<x>/` que recebeu os arquivos do RF01. O padrão de referência é extraído dela; as demais features, na tag `final`, são comparadas a ele.

| # | Convenção | Extração (por feature) | Divergência |
|---|---|---|---|
| C1 | Árvore de subpastas | Conjunto de subdiretórios de 1º nível dentro de `data/`, `domain/` e `presentation/` (ex.: `repositories`, `datasources`, `models`, `entities`, `usecases`, `bloc`, `pages`, `widgets`) | Subpasta presente na referência e ausente na feature, ou o contrário, para o mesmo tipo de conteúdo |
| C2 | Sufixo de repositório | Nome das classes abstratas `class\s+(\w+Repository)\b` em `domain/` e das implementações `class\s+(\w+)\s+implements\s+\w+Repository` em `data/`; padrão = relação entre os nomes (ex.: `XRepository` × `XRepositoryImpl`) | Feature cuja implementação não segue a relação de nomes da referência |
| C3 | Nome das falhas | Classes `class\s+(\w+)\s+extends\s+(\w*Failure)\b`; padrão = sufixo e classe-base | Falha com outro sufixo ou outra classe-base |
| C4 | BLoC, eventos e estados | Arquivos `*_bloc.dart`/`*_cubit.dart`, `*_event.dart`, `*_state.dart` e classes correspondentes (`\w+Bloc`, `\w+Event`, `\w+State`); padrão = esquema de nomes de arquivo e classe | Feature com esquema diferente (ex.: `bloc/` × `cubit/`, eventos num arquivo à parte × no mesmo arquivo) |

**Resultado:** por feature, convenções respeitadas (0–4); por ciclo, número total de divergências (`M15_divergencias`). Feature sem a camada correspondente (ex.: sem `data/`) conta divergência só na convenção afetada.

---

## 3. M6 — referências inexistentes (parte D)

**Onde procurar:** no plano da unidade (Ciclo A: `spec.md`, `plan.md`, `tasks.md`; Ciclo B: arquitetura e stories da unidade) e no diff da unidade.
**Referência externa:** o contrato entregue aos ciclos, `entrada/backend/api/openapi.yaml`, e a taxonomia `entrada/backend/error-taxonomy.md` — hash de cada um registrado no `protocolo.md` (`GATE-C13`).

| Categoria | Extração | Inexistente quando |
|---|---|---|
| (a) Arquivos | `lib/[A-Za-z0-9_/]+\.dart` | O caminho não existe na tag anterior e não é criado no diff da unidade |
| (b) Pacotes | `package:([a-z0-9_]+)/` no diff; `` `([a-z0-9_]+)` `` em frases do plano que contenham *package*, *dependency* ou *pub* | O pacote não está no `pubspec.yaml` da tag da unidade e não é o próprio app, `flutter` ou `dart:` |
| (c1) Rotas | `(GET\|POST\|PATCH\|DELETE)\s+/[A-Za-z0-9_/{}:\-]+` | A rota, com parâmetros normalizados (`:id` = `{id}`), não está entre os 23 caminhos do contrato |
| (c2) Funções | Strings `'([a-z]+(?:-[a-z]+)+)'` no diff usadas para montar URL | O nome não está entre as 23 funções da tabela do `backend/README.md` |
| (c3) Campos | Chaves de mapa JSON no diff — `\[['"]([A-Za-z_][A-Za-z0-9_]*)['"]\]` e `['"]([A-Za-z_][A-Za-z0-9_]*)['"]\s*:` em arquivos de `data/` | A chave não é propriedade de nenhum schema de `components.schemas` do contrato |
| (c4) Códigos de erro | `\b[A-Z]{3,}(?:_[A-Z]+)+\b` | O código não está entre os 13 da taxonomia |

**Colunas:** `M6_inexist_arq` (a), `M6_inexist_pkg` (b), `M6_inexist_backend` (c1–c4). Falsos positivos conhecidos são tratados por uma lista de exclusão congelada com o código (ex.: `REPLAY_MISS` não conta, porque é resposta de ambiente de teste).

---

## 4. M4 — tipos de artefato contáveis

Conta-se o número de **arquivos** por tipo; código, testes, configuração e arquivos gerados por build não contam.

| Ciclo A — Spec Kit | Onde |
|---|---|
| Constitution | `.specify/memory/constitution.md` |
| Especificação, plano, tarefas | `specs/<unidade>/spec.md`, `plan.md`, `tasks.md` |
| Pesquisa, modelo de dados, quickstart | `specs/<unidade>/research.md`, `data-model.md`, `quickstart.md` |
| Contratos | `specs/<unidade>/contracts/*` |
| Checklists | `specs/<unidade>/checklists/*` |
| Relatórios de análise e convergência, se gravados em arquivo | `specs/<unidade>/*` (tipo pelo nome) |

| Ciclo B — BMAD | Onde |
|---|---|
| Sessão de brainstorming, ideia forjada, pesquisa, PRFAQ, brief | diretório de saída do planejamento da versão travada |
| PRD e relatório de validação do PRD | idem |
| UX (`DESIGN.md`, `EXPERIENCE.md`) | idem |
| Arquitetura | idem |
| Épicos e stories | diretório de saída do planejamento e da implementação |
| `sprint-status.yaml`, relatórios de code review, retrospectivas | diretório de saída da implementação |

Os caminhos exatos do BMAD são confirmados na Fase 4 (instalação) e registrados aqui antes do congelamento, sem mudar os tipos. **Leitura:** Ciclo A, na tag de cada unidade e na `final`; Ciclo B, nas tags `plan-done` e `final`.

---

## 5. `M6_tasks` no Ciclo B

**Regra principal (decidida no `GATE-C01` R6):** % de checkboxes de tarefa marcados (`- [x]` ÷ `- [ ]` + `- [x]`) nos arquivos de story da unidade, atribuídos pelo `mapa-stories.csv`, na tag da unidade.

**Condição a verificar na Fase 4:** as notas da v6.11 dizem que acabou o ritual de marcar checkboxes de critérios de aceite após a implementação. Se os arquivos de story da versão travada não tiverem checkboxes de tarefa, vale a **regra alternativa (decidida em 24/09/2026, R30)**: % de stories da unidade com status `done` no `sprint-status.yaml`, declarada como granularidade mais grossa que a do Ciclo A. A escolha é feita por um teste mecânico sobre um arquivo de story de exemplo da versão instalada (existem linhas `- [ ]`/`- [x]` na seção de tarefas?), e registrada aqui.
