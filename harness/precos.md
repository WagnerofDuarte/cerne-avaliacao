# Tabela de preços congelada da M3

**Destino:** `cerne-avaliacao/harness/precos.md` · **Tarefa:** `C-023`
**Data da consulta:** 24/09/2026
**Fonte:** Claude Platform Docs, página "Pricing" — `https://platform.claude.com/docs/en/about-claude/pricing` (tabela "Model pricing").

Valores em USD por milhão de tokens (MTok), API de primeira parte, roteamento global (sem o multiplicador 1,1× de `inference_geo: "us"`), sem Batch API.

| Modelo | Uso no experimento | Input | Output | Escrita de cache 5 min | Escrita de cache 1 h | Leitura de cache (hit) |
|---|---|---|---|---|---|---|
| `claude-sonnet-5` | Agente e subagentes (P1, P1c) | 2,00 | 10,00 | 2,50 | 4,00 | 0,20 |
| `claude-haiku-4-5-20251001` | Tarefas de fundo do Claude Code (P1c) | 1,00 | 5,00 | 1,25 | 2,00 | 0,10 |

**Regras de cálculo (M3):**
1. Custo da sessão = Σ (tokens da categoria × preço da categoria) ÷ 10⁶, por modelo, somando transcript principal e subagentes.
2. Se o transcript separar a escrita de cache em 5 min e 1 h, cada parte usa o seu preço. Se não separar, toda escrita de cache usa o preço de 5 min, e isso é registrado como aproximação.
3. O valor é calculado **sempre** por esta tabela, nunca pelo custo estimado pela ferramenta, e independe da forma de cobrança (assinatura, P13).
4. A tabela não muda durante os ciclos, mesmo que os preços públicos mudem. Uma mudança pública de preço é anotada aqui, sem recalcular.

**Nota:** o preço do Sonnet 5 de US$ 2/US$ 10 foi lançado como introdutório até 31/08/2026; a página oficial consultada o mantém como preço vigente.
