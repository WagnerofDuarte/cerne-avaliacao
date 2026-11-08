// Asserções SQL da suite hold-out (H-005). Acesso a Postgres SO pela biblioteca `postgres` (npm:postgres, porsager),
// sem psql. A URL vem de DATABASE_URL (nunca de arquivo versionado). So leitura: nenhum INSERT/UPDATE/DELETE.
//
// Uso: DATABASE_URL=postgres://... deno run --allow-net --allow-env holdout/sql/asserts.ts <comando> [--flag valor ...]
// Saida: uma linha JSON {ok, cenario, ...}; codigo de saida 0 = ok, 1 = falhou, 2 = erro de uso.
//
// SUPOSICAO (a conferir contra o backend real): tabelas `entries`, `chat_messages`, `chat_sessions`, `auth.users`
// e `experiment.fault_injection_log`, como em holdout/sql/schema_sintetico.sql.
import postgres from "npm:postgres@3.4.5";

type Args = Record<string, string>;

function parse(argv: string[]): { cmd: string; a: Args } {
  const [cmd, ...rest] = argv;
  const a: Args = {};
  for (let i = 0; i < rest.length; i += 2) a[rest[i].replace(/^--/, "")] = rest[i + 1];
  return { cmd, a };
}

const need = (a: Args, ...ks: string[]) => {
  for (const k of ks) if (a[k] === undefined) throw new Error(`faltou --${k}`);
};

export type Sql = ReturnType<typeof postgres>;

async function userId(sql: Sql, email: string): Promise<string> {
  const r = await sql`select id from auth.users where email = ${email}`;
  if (r.length !== 1) throw new Error(`conta nao encontrada: ${email}`);
  return r[0].id;
}

export const comandos: Record<string, (sql: Sql, a: Args) => Promise<Record<string, unknown>>> = {
  // total de entradas da conta (H01-2, H06-3, H06-5, F01-F03 antes/depois)
  async contagem(sql, a) {
    need(a, "email");
    const uid = await userId(sql, a.email);
    const [{ n }] = await sql`select count(*)::int as n from entries where user_id = ${uid}`;
    const ok = a.igual === undefined ? true : n === Number(a.igual);
    return { ok, total: n, esperado: a.igual ?? null };
  },
  // H01-1: tres entradas novas (manual, audio, photo), mesmo conjunto de colunas preenchidas
  async tres_modalidades(sql, a) {
    need(a, "email", "desde");
    const uid = await userId(sql, a.email);
    const rows = await sql`select source, content, embedding, chat_message_id from entries
      where user_id = ${uid} and created_at >= ${a.desde} order by created_at`;
    const fontes = rows.map((r) => r.source).sort();
    const forma = rows.map((r) => `${r.content ? 1 : 0}${r.embedding ? 1 : 0}${r.chat_message_id ? 1 : 0}`);
    const ok = rows.length === 3 && JSON.stringify(fontes) === JSON.stringify(["audio", "manual", "photo"]) &&
      forma.every((f) => f === "110");
    return { ok, fontes, forma_content_embedding_chatmsg: forma };
  },
  // H04-2: a pergunta do usuario nao foi duplicada na retentativa (+1 mensagem `user` na sessao)
  async mensagens_usuario(sql, a) {
    need(a, "email", "sessao", "antes");
    const uid = await userId(sql, a.email);
    const [{ n }] = await sql`select count(*)::int as n from chat_messages m join chat_sessions s on s.id = m.session_id
      where s.user_id = ${uid} and s.title = ${a.sessao} and m.role = 'user'`;
    return { ok: n === Number(a.antes) + 1, total: n, esperado: Number(a.antes) + 1 };
  },
  // H06-4: ids do filtro (fonte + mes corrente) = os da UI (--ids-ui a,b,c)
  async filtro_fonte_mes(sql, a) {
    need(a, "email", "fonte", "ids_ui");
    const uid = await userId(sql, a.email);
    const rows = await sql`select id::text from entries where user_id = ${uid} and source = ${a.fonte}
      and date_trunc('month', created_at) = date_trunc('month', now()) order by id`;
    const sql_ids = rows.map((r) => r.id).sort();
    const ui = a.ids_ui.split(",").filter(Boolean).sort();
    return { ok: JSON.stringify(sql_ids) === JSON.stringify(ui), sql_ids, ui };
  },
  // H10-2: exatamente uma entrada source=chat por mensagem de chat salva duas vezes
  async idempotencia_chat(sql, a) {
    need(a, "email", "mensagem");
    const uid = await userId(sql, a.email);
    const r = await sql`select count(*)::int as n from entries e join chat_messages m on m.id = e.chat_message_id
      where e.user_id = ${uid} and e.source = 'chat' and m.content = ${a.mensagem}`;
    return { ok: r[0].n === 1, total: r[0].n };
  },
  // F01-F15 e demais: a injecao de falha foi de fato registrada no log do backend
  async log_falha(sql, a) {
    need(a, "fn", "fault", "desde");
    const [{ n }] = await sql`select count(*)::int as n from experiment.fault_injection_log
      where function_name = ${a.fn} and fault = ${a.fault} and created_at >= ${a.desde}`;
    return { ok: n >= 1, injecoes: n };
  },
};

if (import.meta.main) {
  const { cmd, a } = parse(Deno.args);
  const url = Deno.env.get("DATABASE_URL");
  if (!cmd || !(cmd in comandos) || !url) {
    console.error(JSON.stringify({ ok: false, erro: "uso: DATABASE_URL=... asserts.ts <" + Object.keys(comandos).join("|") + "> [--flag valor]" }));
    Deno.exit(2);
  }
  const sql = postgres(url, { max: 1, idle_timeout: 2 });
  try {
    const r = await comandos[cmd](sql, a);
    console.log(JSON.stringify({ cenario: cmd, ...r }));
    Deno.exit(r.ok ? 0 : 1);
  } catch (e) {
    console.error(JSON.stringify({ ok: false, erro: String(e) }));
    Deno.exit(2);
  } finally {
    await sql.end({ timeout: 1 });
  }
}
