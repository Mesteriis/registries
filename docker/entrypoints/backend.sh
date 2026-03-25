#!/bin/sh
set -eu

run_migrations="${RUN_DB_MIGRATIONS:-true}"

case "$run_migrations" in
  1|true|TRUE|True|yes|YES|on|ON)
    echo "Running database migrations"
    alembic -c /app/alembic.ini upgrade head
    ;;
  0|false|FALSE|False|no|NO|off|OFF)
    echo "Skipping database migrations"
    ;;
  *)
    echo "Unsupported RUN_DB_MIGRATIONS value: $run_migrations" >&2
    exit 1
    ;;
esac

exec "$@"
