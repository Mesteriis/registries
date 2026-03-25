#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

trivy fs \
  --exit-code 1 \
  --no-progress \
  --scanners vuln,secret,misconfig \
  --skip-dirs "$repo_root/src/backend/.venv" \
  --skip-dirs "$repo_root/src/frontend/node_modules" \
  --skip-dirs "$repo_root/src/frontend/dist" \
  "$repo_root"
