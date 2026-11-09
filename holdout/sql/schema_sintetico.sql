-- Schema SINTETICO para testar as asserções SQL (H-005) num Postgres local.
-- SUPOSICAO: nomes de tabelas/colunas abaixo seguem o que cenarios.md/rnf09.md descrevem
-- (entries.source/content/embedding/chat_message_id; experiment.fault_injection_log). Conferir contra o
-- esquema real do cerne-backend (nao esta neste checkout) antes do GATE-H02.
create schema if not exists auth;
create schema if not exists experiment;
create table if not exists auth.users (id uuid primary key default gen_random_uuid(), email text unique not null);
create table if not exists chat_sessions (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id), title text not null);
create table if not exists chat_messages (id uuid primary key default gen_random_uuid(), session_id uuid not null references chat_sessions(id),
  user_id uuid not null, role text not null check (role in ('user','assistant')), content text not null, created_at timestamptz not null default now());
create table if not exists entries (id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id),
  source text not null check (source in ('manual','audio','photo','chat')), content text not null default '', embedding text,
  chat_message_id uuid references chat_messages(id), created_at timestamptz not null default now());
create table if not exists experiment.fault_injection_log (id bigserial primary key, function_name text not null, fault text not null, created_at timestamptz not null default now());
