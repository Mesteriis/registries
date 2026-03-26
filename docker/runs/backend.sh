#!/bin/sh
set -eu

host="${FULLSTACK_TEMPLATE_API_HOST:-0.0.0.0}"
port="${FULLSTACK_TEMPLATE_API_PORT:-8000}"

exec uvicorn main:app --host "$host" --port "$port"
