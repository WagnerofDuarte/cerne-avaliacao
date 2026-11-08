#!/usr/bin/env bash
# Postgres LOCAL descartavel para testar as asserções SQL (nunca o banco hospedado).
# Uso: pg_local.sh up|down [porta]. Roda como o usuario `postgres` do sistema (o servidor recusa root).
set -euo pipefail
ACAO="${1:?up|down}"; PORTA="${2:-54329}"; DIR=/tmp/holdout-pg
BIN=$(ls -d /usr/lib/postgresql/*/bin | tail -1)
case "$ACAO" in
  up)
    rm -rf "$DIR"; mkdir -p "$DIR"; chown postgres "$DIR"
    su postgres -c "$BIN/initdb -D $DIR/data -A trust -U postgres >/dev/null"
    su postgres -c "$BIN/pg_ctl -D $DIR/data -o '-p $PORTA -k $DIR -c listen_addresses=127.0.0.1' -l $DIR/log -w start >/dev/null"
    echo "postgres://postgres@127.0.0.1:$PORTA/postgres" ;;
  down)
    su postgres -c "$BIN/pg_ctl -D $DIR/data -m fast stop >/dev/null" || true; rm -rf "$DIR" ;;
esac
