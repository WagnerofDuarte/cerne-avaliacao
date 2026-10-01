#!/usr/bin/env bash
# Funções compartilhadas pelos scripts auxiliares do C-017
# (iniciar-ciclo, instalar-metodologia, concluir-rf, rf-incompleto).
# Nunca executado direto — sempre "source"ado.

REPO_ROOT_AVALIACAO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ciclo_dir() {
  local ciclo="$1"
  if [[ "$ciclo" == "a" ]]; then
    : "${CERNE_CICLO_A_DIR:?Defina CERNE_CICLO_A_DIR apontando para o clone local de cerne-ciclo-a}"
    echo "$CERNE_CICLO_A_DIR"
  elif [[ "$ciclo" == "b" ]]; then
    : "${CERNE_CICLO_B_DIR:?Defina CERNE_CICLO_B_DIR apontando para o clone local de cerne-ciclo-b}"
    echo "$CERNE_CICLO_B_DIR"
  else
    echo "Ciclo inválido: '$ciclo' (use a ou b)" >&2
    exit 1
  fi
}

tag_prefix() {
  local ciclo="$1"
  if [[ "$ciclo" == "a" ]]; then echo "cicloA"; else echo "cicloB"; fi
}

now_iso() {
  date -u +"%Y-%m-%dT%H:%M:%S.000Z"
}

registrar_tag() {
  local ciclo="$1" tag="$2" tipo="$3" id_rf="$4" commit="$5"
  python3 "$REPO_ROOT_AVALIACAO/scripts/registrar_tag.py" \
    --ciclo "$ciclo" --tag "$tag" --tipo "$tipo" --id-rf "$id_rf" \
    --commit "$commit" --data "$(now_iso)"
}

validar_id_rf() {
  local id_rf="$1"
  case "$id_rf" in
    F000|RF01|RF02|RF03|RF04|RF05|RF06|RF07|RF08|RF09|RF10) return 0 ;;
    *)
      echo "ID inválido: '$id_rf' (use F000 ou RF01..RF10)" >&2
      return 1
      ;;
  esac
}
