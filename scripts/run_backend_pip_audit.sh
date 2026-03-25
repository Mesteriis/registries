#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
backend_root="$repo_root/src/backend"

tmp_requirements="$(mktemp)"
cleanup() {
  rm -f "$tmp_requirements"
}
trap cleanup EXIT

uv export --project "$backend_root" --no-dev --format requirements-txt --no-hashes > "$tmp_requirements"
uv run --project "$backend_root" --group dev pip-audit --no-deps --disable-pip -r "$tmp_requirements"
