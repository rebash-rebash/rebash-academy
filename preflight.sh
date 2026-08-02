#!/usr/bin/env bash
set -euo pipefail
set -E
readonly E_OK=0 E_USAGE=1 E_MISSING=2 E_CHECK=3
LOG_FILE="${LOG_FILE:-./preflight.log}"
WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/rebash-preflight.XXXXXX")"
log() { local level=$1; shift; local msg="[$(date -Is)] ${level}: $*"; printf '%s\n' "$msg" >&2; printf '%s\n' "$msg" >>"${LOG_FILE}"; }
on_err() { local ec=$?; log ERROR "command failed (exit ${ec}) near line ${BASH_LINENO[0]}"; exit "${ec}"; }
on_exit() { local ec=$?; rm -rf "${WORKDIR}"; log INFO "cleanup done; final_exit=${ec}"; return 0; }
trap on_err ERR; trap on_exit EXIT
require_cmd() { command -v "$1" >/dev/null 2>&1 || { log ERROR "missing: $1"; exit "${E_MISSING}"; }; }
main() {
  local mode=ok
  case "${1:-}" in "" ) ;; --fail) mode=fail ;; -h|--help) exit "${E_OK}" ;; *) exit "${E_USAGE}" ;; esac
  : >"${LOG_FILE}"; log INFO "starting mode=${mode}"; require_cmd date
  printf 'host=lab\n' >"${WORKDIR}/host.txt"
  if [[ "${mode}" == "fail" ]]; then log ERROR "intentional check failure"; exit "${E_CHECK}"; fi
  log INFO "all checks passed"; printf 'RESULT=ok\n'; exit "${E_OK}"
}
main "$@"
