#!/usr/bin/env bash
set -euo pipefail

# Lógica compartilhada por concluir-rf e rf-incompleto (C-017). Chamado
# como: _concluir_unidade.sh <a|b> <ID> <done|incompleto>

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=./_ciclo_common.sh
source "$HERE/_ciclo_common.sh"

CICLO="${1:?uso: _concluir_unidade.sh <a|b> <ID> <done|incompleto>}"
ID_RF="${2:?}"
TIPO="${3:?}"

[[ "$CICLO" == "a" || "$CICLO" == "b" ]] || { echo "Ciclo inválido: '$CICLO'" >&2; exit 1; }
validar_id_rf "$ID_RF"
case "$TIPO" in done|incompleto) ;; *) echo "Tipo inválido: '$TIPO'" >&2; exit 1 ;; esac

CICLO_DIR="$(ciclo_dir "$CICLO")"
PREFIX="$(tag_prefix "$CICLO")"
[[ -d "$CICLO_DIR/.git" ]] || { echo "Não é um repositório git: $CICLO_DIR" >&2; exit 1; }

cd "$CICLO_DIR"

CURRENT_BRANCH="$(git branch --show-current || true)"
if [[ -n "$CURRENT_BRANCH" && "$CURRENT_BRANCH" != "main" ]]; then
  echo "-- Branch atual '$CURRENT_BRANCH' != main; fazendo merge --"
  git checkout main
  git merge --no-ff "$CURRENT_BRANCH" -m "Merge $CURRENT_BRANCH into main ($ID_RF, $TIPO)"
else
  echo "-- Já em main (a metodologia fez o merge, ou nunca saiu dela) --"
fi

ID_LOWER="$(echo "$ID_RF" | tr '[:upper:]' '[:lower:]')"
TAG="$PREFIX/${ID_LOWER}-${TIPO}"
git tag "$TAG"
COMMIT_SHA="$(git rev-parse HEAD)"

registrar_tag "$CICLO" "$TAG" "$TIPO" "$ID_RF" "$COMMIT_SHA"

echo "== $ID_RF ($TIPO) concluído em $CICLO: tag $TAG em $COMMIT_SHA =="
