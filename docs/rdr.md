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
