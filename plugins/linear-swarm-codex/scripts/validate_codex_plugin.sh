#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${PLUGIN_ROOT}/../.." && pwd)"
SCRATCH_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/linear-swarm-codex-validate.XXXXXX")"

trap 'rm -rf "$SCRATCH_ROOT"' EXIT

require_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    printf 'Error: missing file: %s\n' "$path" >&2
    exit 1
  fi
}

require_executable() {
  local path="$1"
  if [ ! -x "$path" ]; then
    printf 'Error: expected executable file: %s\n' "$path" >&2
    exit 1
  fi
}

require_file "${PLUGIN_ROOT}/.codex-plugin/plugin.json"
require_file "${PLUGIN_ROOT}/README.md"
require_file "${PLUGIN_ROOT}/bin/swarm-codex"
require_file "${PLUGIN_ROOT}/skills/linear-swarm-codex/SKILL.md"
require_file "${PLUGIN_ROOT}/scripts/swarm_codex.py"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/linear-issue"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/linear-comment"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/sandbox-worker"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/swarm-phase7"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/runtime/package.json"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/runtime/package-lock.json"
require_file "${REPO_ROOT}/plugins/_shared/linear-swarm/runtime/sandbox_worker.mjs"
require_file "${REPO_ROOT}/.agents/plugins/marketplace.json"
require_executable "${PLUGIN_ROOT}/bin/swarm-codex"
require_executable "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/linear-issue"
require_executable "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/linear-comment"
require_executable "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/sandbox-worker"
require_executable "${REPO_ROOT}/plugins/_shared/linear-swarm/bin/swarm-phase7"

python3 - <<'PY' "${PLUGIN_ROOT}/.codex-plugin/plugin.json" "${REPO_ROOT}/.agents/plugins/marketplace.json"
import json
import sys

for path in sys.argv[1:]:
    with open(path, "r", encoding="utf-8") as handle:
        json.load(handle)
PY

env PYTHONPYCACHEPREFIX="${SCRATCH_ROOT}/pycache" python3 -m py_compile "${PLUGIN_ROOT}/scripts/swarm_codex.py"
bash -n "${PLUGIN_ROOT}/bin/swarm-codex"
node --check "${REPO_ROOT}/plugins/_shared/linear-swarm/runtime/sandbox_worker.mjs"

printf 'linear-swarm-codex manifest, entrypoint, and shared-runtime dependencies look valid.\n'
