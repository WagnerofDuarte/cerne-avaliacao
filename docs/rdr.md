# Registro de Decisões de Resposta (RDR)

**Destino:** `cerne-avaliacao/docs/rdr.md`
**Regra:** `protocolo.md`, seção 3.4 (`GATE-C11`). Documento de protocolo: fica em `cerne-avaliacao` e **nunca** entra no repositório de um ciclo. Só as respostas, dadas no chat com `PROCESSO:`, chegam ao agente.

**Como usar**
1. Antes de responder a uma pausa prevista, procurar aqui uma pergunta equivalente.
2. Se houver, responder com **o mesmo texto** da coluna "Resposta".
3. Se não houver, responder só com o pacote de entrada ou, se ele não cobrir, decidir na hora e acrescentar uma linha.
4. Escolhas na elicitação avançada e no party mode (Ciclo B) também entram aqui, com o método escolhido e as melhorias aceitas e descartadas.

| # | Data | Ciclo | Unidade | Comando/skill | Pergunta (resumo) | Fonte (seção do pacote ou "decisão") | Resposta (texto exato, em inglês) |
|---|---|---|---|---|---|---|---|
| 1 | 11/10/2026 | A | F000 | `speckit-analyze` | Fim do relatório: oferta de sugerir edições concretas de remediação para os N problemas principais | decisão (sugestão de RDR do plano A, 5.3) | `PROCESSO: Yes.` |
| 2 | 11/10/2026 | A | F000 | `speckit-implement` | Algum checklist tem itens desmarcados: seguir com a implementação mesmo assim? (yes/no) | decisão (sugestão de RDR do plano A, 5.3) | `PROCESSO: yes` |
| 3 | 25/10/2026 | B | PLAN | `bmad-brainstorming` | Pergunta de descoberta: o que brainstormar e qual o objetivo (além do `P-GLOBAL`) | decisão (plano B, 5.5 regra 5: preferência) | `PROCESSO: Use your technical judgment, following the input package.` |
| 4 | 25/10/2026 | B | PLAN | `bmad-brainstorming` | O agente abriu o seletor de modo e técnicas no navegador e pediu o prompt colado de volta (ou "let's do it in chat") | decisão (plano B, 5.3: menu de conduzir; o seletor foi fechado sem uso) | `PROCESSO: Use your technical judgment, following the input package.` |
| 5 | 25/10/2026 | B | PLAN | `bmad-forge-idea` | De onde partir e qual ideia forjar (descoberta inicial) | decisão (sugestão de RDR do plano B, §9.2–9.5) | `PROCESSO: Start from the product input in docs/input/ (requirements.md, prototype/, backend/) and the earlier outputs in _bmad-output/.` |
| 6 | 25/10/2026 | B | PLAN | `bmad-forge-idea` | Painel, pergunta 1: "Which idea should this forge session pressure-test?" (F000 foundation choices / Something else about Cerne) | decisão (plano B, 5.5 regra 5: preferência) | `PROCESSO: Use your technical judgment, following the input package.` |
| 7 | 25/10/2026 | B | PLAN | `bmad-forge-idea` | Painel, pergunta 2: "What do you want out of this session?" (Make it better / Test whether it holds up / Clarify and understand) | decisão (plano B, 5.5 regra 5: preferência) | `PROCESSO: Use your technical judgment, following the input package.` |
| 8 | 25/10/2026 | B | PLAN | `bmad-forge-idea` | Interrogatório das personas (Winston × Priya): cache local, Hive ou drift, e se alguma tela calcula sobre o cache | decisão (plano B, 5.5 regra 5: preferência; `requirements.md` §13 deixa o cache livre) | `PROCESSO: Use your technical judgment, following the input package.` |
| 9 | 25/10/2026 | B | PLAN | `bmad-deep-recon` | Painel, pergunta 1: "What decision is this research meant to support, and do you have anything to work from already?" | decisão (plano B, 5.5 regra 5: preferência) | `PROCESSO: Use your technical judgment, following the input package.` |
| 10 | 25/10/2026 | B | PLAN | `bmad-deep-recon` | Painel, pergunta 2: "How should this research be produced?" (Run it here now / Draft a prompt for my own tool / Process a report I already have) | decisão (plano B, 5.3: modo da pesquisa; 5.5 regra 5) | Pretendido: `PROCESSO: Use your technical judgment, following the input package.` Enviado: `ROCESSO: Use your technical judgment, following the input package.` (D-039) |
| 11 | 25/10/2026 | B | PLAN | `bmad-deep-recon` | "Approve this plan to run native research now?" (Approve as-is / Trim / Bump effort / Cancel) | decisão (plano B, 5.5 regra 5: preferência) | `PROCESSO: Use your technical judgment, following the input package.` |
| 12 | 25/10/2026 | B | PLAN | `bmad-prfaq` | Perguntas de descoberta iniciais (escopo do PRFAQ, cliente, problema, stakes, conceito da solução, se é um TCC) | decisão (sugestão de RDR do plano B, §9.2–9.5; o pacote não define cliente nem problema) | `PROCESSO: Start from the product input in docs/input/ (requirements.md, prototype/, backend/) and the earlier outputs in _bmad-output/.` (mesmo texto da linha 5) |
| 13 | 25/10/2026 | B | PLAN | `bmad-prfaq` | O agente apresentou uma hipótese de cliente, problema, stakes e solução e perguntou se batia com o que o pesquisador tinha em mente e se o PRFAQ devia nomear a tensão da qualidade do texto gerado | decisão (plano B, 5.5 regra 5: preferência) | `PROCESSO: Use your technical judgment, following the input package.` |
| 14 | 25/10/2026 | B | PLAN | `bmad-product-brief` | Perguntas de descoberta iniciais: para que serve o brief, Coaching path × Fast path, e o que ficou de fora do PRFAQ | decisão (plano B, 5.3: Coaching × Fast = frase padrão; o pacote não cobre as outras) | `PROCESSO: Use your technical judgment, following the input package.` |
| 15 | 25/10/2026 | B | PLAN | `bmad-product-brief` | Rascunho pronto: finalizar (revisão de estrutura e prosa) ou ajustar antes (a persona marcada `[ASSUMPTION]` vale?) | decisão (plano B, 5.3: aprovação de seção; 5.5 regra 5) | `PROCESSO: Use your technical judgment, following the input package.` |
