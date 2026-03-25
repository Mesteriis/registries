#!/bin/sh
set -eu

host="${REGISTRIES_API_HOST:-0.0.0.0}"
port="${REGISTRIES_API_PORT:-8000}"

exec uvicorn main:app --host "$host" --port "$port"
