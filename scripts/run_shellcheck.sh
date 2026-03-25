#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

shellcheck \
  "$repo_root"/docker/entrypoints/*.sh \
  "$repo_root"/docker/runs/*.sh \
  "$repo_root"/scripts/*.sh
