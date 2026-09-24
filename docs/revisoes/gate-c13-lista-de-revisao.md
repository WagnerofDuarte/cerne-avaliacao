# GATE-C13 — Lista de revisão do pacote de entrada

**Destino:** `cerne-avaliacao/docs/revisoes/gate-c13-lista-de-revisao.md`
**Data:** 23/09/2026
**Objeto:** `cerne-avaliacao/entrada/` (vira `docs/input/` nos repositórios dos ciclos).
**Fontes usadas:** `ux/Requisitos_e_Fluxo_de_Telas_TCC.md` reconciliado (SHA-256 `a62d8439…3db0`, idêntico no `ux.zip` e no handoff); `ux/Cerne - Prototipo Final.html` (SHA-256 `61032a92…185d2fff`, confere com o congelamento do backend); `cerne-backend-handoff-main` (commit `fa998d9e`); `doc-prototipo.md` do projeto.

Duas perguntas para cada arquivo: (1) isto favorece uma metodologia ou revela o que será medido? (2) a tradução acrescenta, omite ou muda algum requisito, critério ou texto de interface? Compare lado a lado com a fonte.

## 1. Arquivos do pacote

| Arquivo | Fonte | O que conferir |
|---|---|---|
| `requirements.md` | Requisitos reconciliados | Itens 2.1–2.6 abaixo |
| `prototype/cerne-prototype.html` | HTML congelado | Uma única linha mudada (item 2.7) |
| `prototype/prototype-extract.md` | `doc-prototipo.md` §1, §2, §4, §6, §7 | Itens 2.8–2.10 |
| `backend/README.md` | Handoff `README.md` | Tabela contrato → função idêntica (23 linhas) |
| `backend/api/openapi.yaml` | Handoff `api/openapi.yaml` | Item 2.11 |
| `backend/error-taxonomy.md` | Handoff `taxonomia_erros.md` | 13 códigos, HTTP e `retryable` idênticos |
| `backend/export-screen-states.md` | Handoff `mapa_estados_tela.md` | Status traduzidos para os valores do contrato (item 2.12) |
| `backend/sync-badge.md` | Handoff `selo_sincronizacao.md` | 3 estados idênticos |
| `backend/known-bugs.md` | Handoff `bugs_conhecidos.md` | Tabela vazia |
| `backend/fixtures/` | Handoff `fixtures/` | Item 2.13 |
| `cerne-avaliacao/prompts/` (14, **fora do pacote**, R27) | P8, P9, P11, P12, requisitos | Item 2.14 |

**Fora do pacote, por decisão:** credenciais; `roteiro_de_validacao.md`; `testes_contrato/`; `politica_defeito_D16.md`; `fixtures/textos.json`.

## 2. Pontos que pedem a sua decisão ou conferência

### Requisitos (`requirements.md`)
2.1 **Removido por neutralidade:** parágrafo "Contexto"; linhas "Estressa"; toda a §8 (métricas); §13 (congelamento do protótipo); a justificativa "para manter os dois ciclos comparáveis" do RF03; a frase "Backend único, compartilhado pelos dois ciclos (Spec Kit e BMAD-METHOD), construído com RIPER"; as anotações de histórico "Correção em 10/09/2026" — **o conteúdo que elas corrigiam foi mantido**, só a narrativa da correção saiu.

2.2 **RNF06–RNF09 sem o "como medimos":** saíram os nomes de ferramenta (`clean_architecture_kit`, `import_linter`, `very_good_coverage`) e a rubrica de 3 pontos do RNF08 com a **tolerância de ±4 dp**. Ficaram as metas. O RNF09 manteve "testes com `mocktail`" e "15 de 15 cenários", porque são requisito de desenvolvimento (e o `mocktail` é stack fixa, P8). **Confira se a retirada da tolerância de ±4 dp está de acordo.**

2.3 **§9 (stack) e §10 (parâmetros):** saíram a coluna "Onde foi decidido", as linhas de lint, cobertura e complexidade (substituídas por remissão a RNF06/RNF07), a linha "Limiar de complexidade ciclomática >10" e a linha "Decisões de plano checadas (8–10)". **Complexidade:** o plano mandava trocar pela "regra de qualidade correspondente", mas não há requisito de produto correspondente — o limiar só existia como métrica. Eu retirei. **Decida se entra como regra ("métodos com complexidade ≤ 10") ou fica fora.**

2.4 **Contradições internas da fonte, mantidas com nota de precedência:** a §8 (modelo de dados) traz `sync_status` em `entries` e "tags criadas manualmente pelo usuário"; a semântica do selo (D9) diz que não existe `sync_status`, e a §6.2 diz que tags vêm só do seed. A própria fonte diz que os nomes da §8 são sugestão e que o `openapi.yaml` é a fonte de verdade; acrescentei uma nota que repete essa precedência. **Alternativa:** tirar as duas linhas contraditórias.

2.5 **Códigos de erro:** a §11 lista 10 códigos "mínimos"; o backend tem 13 (lista fechada). Mantive os 10 e acrescentei remissão à taxonomia completa.

2.6 **Acrescentado:** §12 (ordem de entrega, P9, com o escopo da F000) e §13 (restrições técnicas, P8, com a convenção de pastas). Telas 5 e 6 e a §2 dizem "não implementado" (P10); a fonte dizia que a Tela 5 "existe visualmente para completude da demo".

### Protótipo
2.7 **HTML derivado:** única mudança — "Referência visual travada para o TCC de Wagner Duarte (Spec Kit vs. BMAD-METHOD) · frame 390×844 · grid 4dp" → "Referência visual travada · frame 390×844 · grid 4dp". Busquei "TCC", "Spec Kit", "BMAD", "Wagner" no template e nos 24 recursos do bundle (7 comprimidos, descomprimidos para a busca): nenhuma outra ocorrência. Restam anotações neutras, como "Ground truth para design_tokens.dart — RNF08" e rótulos "RF04 · …". O original fica em `cerne-avaliacao` para a M9. **O hash do derivado é calculado no terminal**, sobre o arquivo versionado, e registrado no `protocolo.md`.

2.8 **Extrato — omitido do `doc-prototipo.md`:** os parágrafos "Por que existe", porque usam uma **numeração antiga de RF/RNF** que não bate com os requisitos (ex.: chamam a memória do chat de "RF07" e a exclusão de conta de "RF08/RNF05"); a §3 (biblioteca de componentes) e a §5 (fluxos ponta a ponta), fora do escopo do `C-006`; o item 4 da §7 (personas, extensão); e os tempos simulados do protótipo (1,4 s de processamento, 0,7 s/2,2 s da exportação, 3 caracteres a cada 30 ms). **Decida se a §3 (componentes) deve entrar** — ela ajuda a fidelidade visual e não revela nada.

2.8b **Extrato — tokens refeitos a partir do HTML (24/09/2026):** o HTML tem um painel "Design Tokens" marcado como *ground truth* para o `design_tokens.dart`, com nomes e valores que o `doc-prototipo.md` não traz (`colorOnAccent #241C0D`, `colorWarningSync`, `colorInfoOffline`, escala tipográfica com tamanho/entrelinha). A seção 3 do extrato agora segue o painel; as duas cores que só aparecem em telas (balão do usuário, texto de chip) ficam listadas à parte. A seção 2 ganhou o catálogo oficial dos 32 estados. Confira contra o painel do HTML.

2.9 **Extrato — acrescentado:** linha de precedência ("o protótipo define aparência e estados; regras de comportamento estão nos requisitos") — o protótipo insere o insight "a cada 5 mensagens", e o RF08 diz "5 mensagens OU 2 min"; nota no "Sheet de filtro" de que o backend não filtra por categoria (RF06).

2.10 **Dimensões para a P11:** frame 390×844. Candidatos a simulador: iPhone 16e ou iPhone 14 (escolha final no `GATE-C15`).

### Backend
2.11 **`openapi.yaml`:** traduzidos os 29 textos distintos em português (72 campos `summary`/`description`/`title`; o título "Cerne Backend API" não mudou); saíram o comentário "GERADO por…", os IDs internos (T-026, D-01, D12, D15, "mesma impressão digital de cache") e a menção a "dev/ciclo-a/ciclo-b". **Verificação feita:** com os campos de texto removidos, o YAML traduzido e o original são idênticos (comparação por script). A formatação do arquivo mudou (serialização), o conteúdo do contrato não.

2.12 **`export-screen-states.md`:** os status em português da fonte ("pendente", "dados_prontos", "concluída", "pulada"…) foram escritos com os valores reais do contrato (`pending`, `data_ready`, `done`, `skipped`…), conferidos no `openapi.yaml`.

2.13 **Fixtures:** entram as 3 mídias, a transcrição esperada e os 3 textos semeados (sem a regra de aceite, GATE e T-024). O texto da transcrição menciona medicação e psiquiatra — é dado de teste do backend, entregue igual aos dois ciclos.

### Prompts
2.14 **Alocação no P-RF09:** a Tela 6 inteira (dashboard, edição de nome, "Sair", "Apagar conta" com confirmação, RNF05) ficou na unidade RF09, porque o RNF05 não tem unidade própria e a Tela 6 "conecta a RF09, RNF05". **Confirme.** Dependências declaradas: RF06 depende de RF07; RF05 de RF07; RF09 de F000 e RF01.

## 3. Registro (preencher)
- Decididos em 23/09/2026 (R27): prompts fora de `docs/input/`; item 2.3 — limiar de complexidade **fora**; item 2.14 — Tela 6 inteira no RF09 **confirmada**.
- Decididos em 23/09/2026 (R28): item 2.2 — tolerância de ±4 dp **fora**; item 2.4 — tradução fiel da §8 **mantida**, com a nota de precedência do contrato; item 2.8 — biblioteca de componentes **incluída** (`prototype-extract.md`, seção 6).
- Pendente: a revisão lado a lado e os hashes.
- Observações por arquivo:
- Hashes (terminal): `sha256sum` de cada arquivo e do pacote inteiro (`find entrada -type f | sort | xargs sha256sum | sha256sum`), registrados no `protocolo.md`.
