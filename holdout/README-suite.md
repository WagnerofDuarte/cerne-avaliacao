# Suíte hold-out automatizada (H-005) — como as peças se ligam

Peças novas (nada de `cenarios.md`, `rnf09.md`, `estados-m9.md`, `referencia/` ou `fixtures/` foi editado):

| Peça | Onde | Testado em |
|---|---|---|
| Fluxos Maestro (25 cenários C-018 + 15 falhas C-019 + 31 estados C-020) | `holdout/maestro/*.yaml` (gerados por `holdout/maestro/gerar.py`) | **só revisão por leitura** (`holdout/maestro/verificar.py`): cobertura, sintaxe e textos contra o protótipo |
| Manifesto cenário → fluxo, cenário do proxy e asserções SQL | `holdout/suite.json` | `test_verificar.py` |
| Addon do mitmproxy + API de controle | `holdout/proxy/cerne_holdout.py`, `cenarios.py` | 14 testes contra backend **falso** (mitmdump real) |
| Asserções SQL (Deno + `npm:postgres`, só leitura) | `holdout/sql/asserts.ts` | Postgres **local** com schema sintético |
| Textos do instrumento | `holdout/fixtures/*.json` (já tinham `rnf09_mensagem_1..3`) | — |

**Como roda na Parte IV (V-002)** — passos por cenário (o executor da Parte IV os orquestra; este repositório não traz o orquestrador):
1. `TEST_FAULT_KEY=<do operador> mitmdump -s holdout/proxy/cerne_holdout.py` (porta de controle 8099).
2. `maestro test -e APP_ID=<bundle> -e SENHA_A=... -e PROXY_CONTROL=http://127.0.0.1:8099 -e CICLO_ANON=X holdout/maestro/<ID>.yaml` — os fluxos armam/desarmam o proxy e checam contagens (`/check`).
3. As asserções SQL de cada cenário (`suite.json` → `sql`) rodam depois: `DATABASE_URL=... deno run --allow-net --allow-env holdout/sql/asserts.ts <comando> --flag valor`.

**Suposições a conferir antes do `GATE-H02`** (backend e pacote de entrada não estão neste checkout): nomes das funções (`x-cerne-function` ou `/functions/v1/<fn>`), formato do SSE (`event: token`), corpo do 401 forjado, chave do campo da narrativa/status, esquema de tabelas SQL, posições dos ícones (medidas no protótipo, ±4 px), `pressKey: Home` e esperas reais por `extendedWaitUntil optional` no iOS físico.
