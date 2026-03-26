# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS backend-builder

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /build/backend

COPY src/backend/pyproject.toml src/backend/uv.lock ./
RUN uv sync --frozen --no-dev


FROM python:3.14-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src/backend
ENV PATH=/opt/venv/bin:${PATH}

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=backend-builder /opt/venv /opt/venv
COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations
COPY src/backend /app/src/backend
COPY --chmod=755 docker/entrypoints/backend.sh /usr/local/bin/backend-entrypoint.sh
COPY --chmod=755 docker/runs/backend.sh /usr/local/bin/backend-run.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/api/v1/system/health')"

USER app

ENTRYPOINT ["/usr/local/bin/backend-entrypoint.sh"]
CMD ["/usr/local/bin/backend-run.sh"]


FROM node:22-alpine AS frontend-builder

WORKDIR /build/frontend

RUN corepack enable

COPY src/frontend/package.json src/frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY src/frontend /build/frontend
RUN pnpm build


FROM nginxinc/nginx-unprivileged:1.27-alpine AS frontend

COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --chmod=755 docker/entrypoints/frontend.sh /usr/local/bin/frontend-entrypoint.sh
COPY --chmod=755 docker/runs/frontend.sh /usr/local/bin/frontend-run.sh
COPY --from=frontend-builder /build/frontend/dist /usr/share/nginx/html

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:8080/

ENTRYPOINT ["/usr/local/bin/frontend-entrypoint.sh"]
CMD ["/usr/local/bin/frontend-run.sh"]
