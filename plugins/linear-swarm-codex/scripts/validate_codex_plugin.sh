#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${PLUGIN_ROOT}/../.." && pwd)"

require_file() {
  local path="$1"
  if [ ! -f "$path" ]; then
    printf 'Error: missing file: %s\n' "$path" >&2
    exit 1
  fi
}

require_file "${PLUGIN_ROOT}/.codex-plugin/plugin.json"
require_file "${PLUGIN_ROOT}/README.md"
require_file "${PLUGIN_ROOT}/skills/linear-swarm-codex/SKILL.md"
require_file "${REPO_ROOT}/plugins/linear-swarm/bin/linear-issue"
require_file "${REPO_ROOT}/plugins/linear-swarm/bin/linear-comment"
require_file "${REPO_ROOT}/plugins/linear-swarm/bin/sandbox-worker"
require_file "${REPO_ROOT}/plugins/linear-swarm/bin/swarm-phase7"
require_file "${REPO_ROOT}/.agents/plugins/marketplace.json"

python3 - <<'PY' "${PLUGIN_ROOT}/.codex-plugin/plugin.json" "${REPO_ROOT}/.agents/plugins/marketplace.json"
import json
import sys

for path in sys.argv[1:]:
    with open(path, "r", encoding="utf-8") as handle:
        json.load(handle)
PY

printf 'linear-swarm-codex manifest and shared-runtime dependencies look valid.\n'
