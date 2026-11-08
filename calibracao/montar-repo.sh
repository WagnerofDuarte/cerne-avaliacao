#!/usr/bin/env bash
# Monta, FORA do repositorio de avaliacao, um repositorio git real com as tags v1 e v2
# a partir dos snapshots calibracao/v1 e calibracao/v2. Uso: montar-repo.sh <destino-vazio>
set -euo pipefail
DEST="${1:?uso: montar-repo.sh <destino>}"
AQUI="$(cd "$(dirname "$0")" && pwd)"
[ -e "$DEST" ] && [ -n "$(ls -A "$DEST" 2>/dev/null || true)" ] && { echo "destino nao vazio: $DEST" >&2; exit 2; }
mkdir -p "$DEST" && cd "$DEST"
git init -q -b main
git config user.email calibracao@example.invalid && git config user.name calibracao
for v in v1 v2; do
  find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  cp -a "$AQUI/$v/." .
  git add -A && git commit -q -m "calibracao $v" && git tag "$v"
done
echo "repositorio de calibracao montado em $DEST (tags: $(git tag | tr '\n' ' '))"
