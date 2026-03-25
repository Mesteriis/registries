#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
trivy_version="${TRIVY_VERSION:-0.69.3}"
trivy_docker_image="${TRIVY_DOCKER_IMAGE:-aquasec/trivy:${trivy_version}}"
trivy_docker_fallback_image="${TRIVY_DOCKER_FALLBACK_IMAGE:-ghcr.io/aquasecurity/trivy:${trivy_version}}"

run_local_trivy() {
  trivy fs \
    --exit-code 1 \
    --no-progress \
    --scanners vuln,secret,misconfig \
    --skip-dirs "$repo_root/src/backend/.venv" \
    --skip-dirs "$repo_root/src/frontend/node_modules" \
    --skip-dirs "$repo_root/src/frontend/dist" \
    "$repo_root"
}

run_docker_trivy_with_image() {
  local image="$1"

  docker run --rm \
    -v "$repo_root:/workspace" \
    "$image" \
    fs \
    --exit-code 1 \
    --no-progress \
    --scanners vuln,secret,misconfig \
    --skip-dirs /workspace/src/backend/.venv \
    --skip-dirs /workspace/src/frontend/node_modules \
    --skip-dirs /workspace/src/frontend/dist \
    /workspace
}

if command -v trivy >/dev/null 2>&1; then
  run_local_trivy
  exit 0
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "error: neither trivy nor docker is available for repo-security scan" >&2
  exit 127
fi

if run_docker_trivy_with_image "$trivy_docker_image"; then
  exit 0
else
  status=$?
fi

if [[ "$status" -ne 125 || "$trivy_docker_image" == "$trivy_docker_fallback_image" ]]; then
  exit "$status"
fi

echo "warning: failed to start $trivy_docker_image, retrying with $trivy_docker_fallback_image" >&2
run_docker_trivy_with_image "$trivy_docker_fallback_image"
