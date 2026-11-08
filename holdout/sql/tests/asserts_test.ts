// Teste das asserções SQL contra um Postgres LOCAL com schema sintetico (nunca o banco hospedado).
// Uso: DATABASE_URL=$(holdout/sql/pg_local.sh up) deno test --allow-net --allow-env --allow-read holdout/sql/tests/
import postgres from "npm:postgres@3.4.5";
import { assert, assertEquals } from "jsr:@std/assert@1";
import { comandos } from "../asserts.ts";

const url = Deno.env.get("DATABASE_URL")!;
const sql = postgres(url, { max: 1, onnotice: () => {} });

Deno.test("asserções SQL contra Postgres local", async (t) => {
  await sql.unsafe("drop schema if exists experiment cascade; drop schema if exists auth cascade; drop table if exists entries, chat_messages, chat_sessions cascade");
  await sql.unsafe(await Deno.readTextFile(new URL("../schema_sintetico.sql", import.meta.url)));
  const [{ id: uid }] = await sql`insert into auth.users (email) values ('cenario-cheio@cerne.test') returning id`;
  await sql`insert into auth.users (email) values ('cenario-vazio@cerne.test')`;
  const [{ id: sid }] = await sql`insert into chat_sessions (user_id, title) values (${uid}, 'Conversa sobre o dia no trabalho') returning id`;
  const [{ id: mid }] = await sql`insert into chat_messages (session_id, user_id, role, content) values (${sid}, ${uid}, 'user', 'mensagem quinta') returning id`;
  await sql`insert into chat_messages (session_id, user_id, role, content) values (${sid}, ${uid}, 'assistant', 'resposta')`;
  const desde = new Date(Date.now() - 1000).toISOString();
  await sql`insert into entries (user_id, source, content, embedding) values (${uid}, 'manual', 'a', 'e'), (${uid}, 'audio', 'b', 'e'), (${uid}, 'photo', 'c', 'e')`;
  await sql`insert into entries (user_id, source, content, embedding, chat_message_id) values (${uid}, 'chat', 'd', 'e', ${mid})`;
  await sql`insert into experiment.fault_injection_log (function_name, fault) values ('entries-create', 'timeout')`;

  await t.step("contagem", async () => {
    assertEquals((await comandos.contagem(sql, { email: "cenario-cheio@cerne.test", igual: "4" })).ok, true);
    assertEquals((await comandos.contagem(sql, { email: "cenario-cheio@cerne.test", igual: "5" })).ok, false);
    assertEquals((await comandos.contagem(sql, { email: "cenario-vazio@cerne.test", igual: "0" })).ok, true);
  });
  await t.step("tres_modalidades: positivo e negativo", async () => {
    // a entrada de chat tambem e nova => 4 linhas => o criterio (exatamente 3) falha; restringindo por tempo com 'desde' futuro tambem falha
    assertEquals((await comandos.tres_modalidades(sql, { email: "cenario-cheio@cerne.test", desde })).ok, false);
    await sql`delete from entries where source = 'chat'`;
    assertEquals((await comandos.tres_modalidades(sql, { email: "cenario-cheio@cerne.test", desde })).ok, true);
    await sql`update entries set embedding = null where source = 'audio'`;
    assertEquals((await comandos.tres_modalidades(sql, { email: "cenario-cheio@cerne.test", desde })).ok, false);
    await sql`update entries set embedding = 'e' where source = 'audio'`;
    await sql`insert into entries (user_id, source, content, embedding, chat_message_id) values (${uid}, 'chat', 'd', 'e', ${mid})`;
  });
  await t.step("mensagens_usuario (H04-2: +1, nao +2)", async () => {
    const base = { email: "cenario-cheio@cerne.test", sessao: "Conversa sobre o dia no trabalho" };
    assertEquals((await comandos.mensagens_usuario(sql, { ...base, antes: "0" })).ok, true);
    assertEquals((await comandos.mensagens_usuario(sql, { ...base, antes: "1" })).ok, false);
  });
  await t.step("filtro_fonte_mes", async () => {
    const [{ id }] = await sql`select id::text from entries where source = 'audio'`;
    assertEquals((await comandos.filtro_fonte_mes(sql, { email: "cenario-cheio@cerne.test", fonte: "audio", ids_ui: id })).ok, true);
    assertEquals((await comandos.filtro_fonte_mes(sql, { email: "cenario-cheio@cerne.test", fonte: "audio", ids_ui: "" })).ok, false);
  });
  await t.step("idempotencia_chat", async () => {
    assertEquals((await comandos.idempotencia_chat(sql, { email: "cenario-cheio@cerne.test", mensagem: "mensagem quinta" })).ok, true);
    await sql`insert into entries (user_id, source, content, embedding, chat_message_id) values (${uid}, 'chat', 'dup', 'e', ${mid})`;
    assertEquals((await comandos.idempotencia_chat(sql, { email: "cenario-cheio@cerne.test", mensagem: "mensagem quinta" })).ok, false);
  });
  await t.step("log_falha", async () => {
    assertEquals((await comandos.log_falha(sql, { fn: "entries-create", fault: "timeout", desde })).ok, true);
    assertEquals((await comandos.log_falha(sql, { fn: "entries-create", fault: "offline", desde })).ok, false);
  });
  await sql.end();
});
