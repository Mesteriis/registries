.PHONY: backend-sync frontend-install check lint test build docker-build install-hooks

backend-sync:
	cd src/backend && uv sync --group dev

frontend-install:
	cd src/frontend && pnpm install --frozen-lockfile

check:
	python3 scripts/check_adrs.py
	python3 scripts/check_repo_structure.py
	python3 scripts/check_backend_architecture.py
	python3 scripts/check_specs.py

lint:
	python3 scripts/run_backend_lint.py
	python3 scripts/run_backend_deptry.py
	python3 scripts/run_frontend_lint.py
	./scripts/run_shellcheck.sh
	./scripts/run_hadolint.sh

test:
	python3 scripts/run_backend_tests.py
	python3 scripts/run_frontend_tests.py

build:
	python3 scripts/run_backend_types.py
	python3 scripts/run_backend_import_boundaries.py
	python3 scripts/run_frontend_types.py
	python3 scripts/run_frontend_build.py

docker-build:
	docker build -f docker/Dockerfile --target backend -t registries-backend:local .
	docker build -f docker/Dockerfile --target frontend -t registries-frontend:local .

install-hooks:
	cd src/backend && uv run pre-commit install --install-hooks && uv run pre-commit install --hook-type pre-push --install-hooks
