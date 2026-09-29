#!/usr/bin/env -S deno run --allow-net --allow-env --allow-read
// scripts/db-truncate-and-seed.ts (C-015)
//
// "Reset" de dados para os ambientes hospedados (ciclo-a/ciclo-b), onde
// não existe `supabase db reset` contra projeto remoto (achado:
// cerne-backend/docs/roteiro_de_congelamento.md, Passo 7). O equivalente
// documentado ali é um TRUNCATE manual das tabelas de app + recarga do
// seed — feito aqui em Deno puro (biblioteca `postgres`), sem depender de
// `psql` (achado: o Mac não tem `psql` por padrão — mesmo motivo que fez
// o próprio cerne-backend evitar `psql` em `configure-worker.ts`).
//
// Nunca toca o schema `experiment` (worker_config, ai_replay_cache) —
// só as tabelas de app listadas no roteiro.
//
// Uso:
//   deno run --allow-net --allow-env --allow-read scripts/db-truncate-and-seed.ts --seed <caminho/para/seed.sql>
//
// Variável de ambiente:
//   SUPABASE_DB_URL (obrigatório — connection string do ciclo-a/ciclo-b)

import postgres from "npm:postgres";

const DB_URL = Deno.env.get("SUPABASE_DB_URL");
if (!DB_URL) {
  console.error("Falta a variável de ambiente SUPABASE_DB_URL.");
  Deno.exit(1);
}

const seedFlagIndex = Deno.args.indexOf("--seed");
const seedPath = seedFlagIndex >= 0 ? Deno.args[seedFlagIndex + 1] : undefined;
if (!seedPath) {
  console.error("Uso: --seed <caminho/para/seed.sql>");
  Deno.exit(1);
}

const sql = postgres(DB_URL, { max: 1 });

try {
  console.log(
    "Truncando entries, chat_sessions, chat_messages, insights, export_jobs...",
  );
  await sql.unsafe(
    "truncate table entries, chat_sessions, chat_messages, insights, export_jobs cascade;",
  );

  console.log(`Recarregando seed de ${seedPath}...`);
  await sql.file(seedPath);

  console.log("OK.");
} finally {
  await sql.end();
}
