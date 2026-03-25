from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"
BACKEND_PATHS = ("api", "apps", "core", "runtime", "tests")
ALLOWED_STD_LOGGING_IMPORTS = {
    BACKEND_ROOT / "core" / "observability" / "logging.py",
}
ALLOWED_STRUCTLOG_IMPORTS = {
    BACKEND_ROOT / "core" / "observability" / "logging.py",
}
ALLOWED_SENTRY_IMPORTS = {
    BACKEND_ROOT / "core" / "observability" / "error_tracking.py",
}
ALLOWED_OTEL_INSTRUMENTATION_IMPORTS = {
    BACKEND_ROOT / "core" / "observability" / "tracing.py",
}


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def validate_import(node: ast.AST, path: Path, errors: list[str]) -> None:
    if isinstance(node, ast.Import):
        for alias in node.names:
            name = alias.name
            if name == "logging" and path not in ALLOWED_STD_LOGGING_IMPORTS:
                errors.append(
                    f"{relative_path(path)} imports stdlib logging; use core.observability.get_logger instead"
                )
            if name == "structlog" and path not in ALLOWED_STRUCTLOG_IMPORTS:
                errors.append(
                    f"{relative_path(path)} imports structlog directly; use core.observability.get_logger instead"
                )
            if name == "sentry_sdk" and path not in ALLOWED_SENTRY_IMPORTS:
                errors.append(
                    f"{relative_path(path)} imports sentry_sdk directly; error tracking must stay centralized in core/observability/error_tracking.py"
                )
            if name.startswith("opentelemetry.instrumentation") and path not in ALLOWED_OTEL_INSTRUMENTATION_IMPORTS:
                errors.append(
                    f"{relative_path(path)} imports OpenTelemetry instrumentors directly; tracing setup must stay centralized in core/observability/tracing.py"
                )
        return

    if not isinstance(node, ast.ImportFrom) or node.module is None:
        return

    module = node.module
    if module == "logging" and path not in ALLOWED_STD_LOGGING_IMPORTS:
        errors.append(
            f"{relative_path(path)} imports from stdlib logging; use core.observability.get_logger instead"
        )
    if module == "structlog" and path not in ALLOWED_STRUCTLOG_IMPORTS:
        errors.append(
            f"{relative_path(path)} imports from structlog directly; use core.observability.get_logger instead"
        )
    if module.startswith("sentry_sdk") and path not in ALLOWED_SENTRY_IMPORTS:
        errors.append(
            f"{relative_path(path)} imports sentry_sdk directly; error tracking must stay centralized in core/observability/error_tracking.py"
        )
    if module.startswith("opentelemetry.instrumentation") and path not in ALLOWED_OTEL_INSTRUMENTATION_IMPORTS:
        errors.append(
            f"{relative_path(path)} imports OpenTelemetry instrumentors directly; tracing setup must stay centralized in core/observability/tracing.py"
        )


def validate_calls(tree: ast.AST, path: Path, errors: list[str]) -> None:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name) and node.func.id in {"print", "pprint"}:
            errors.append(
                f"{relative_path(path)} uses {node.func.id}() at line {node.lineno}; backend runtime code must use structured logging only"
            )

        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "logging"
            and node.func.attr == "getLogger"
            and path not in ALLOWED_STD_LOGGING_IMPORTS
        ):
            errors.append(
                f"{relative_path(path)} calls logging.getLogger() at line {node.lineno}; use core.observability.get_logger instead"
            )

        if (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "sentry_sdk"
            and node.func.attr == "init"
            and path not in ALLOWED_SENTRY_IMPORTS
        ):
            errors.append(
                f"{relative_path(path)} calls sentry_sdk.init() at line {node.lineno}; sentry bootstrap must stay centralized in core/observability/error_tracking.py"
            )


def validate_file(path: Path, errors: list[str]) -> None:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        validate_import(node, path, errors)
    validate_calls(tree, path, errors)


def main() -> int:
    errors: list[str] = []

    for rel_path in BACKEND_PATHS:
        for path in sorted((BACKEND_ROOT / rel_path).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            validate_file(path, errors)

    main_path = BACKEND_ROOT / "main.py"
    if main_path.is_file():
        validate_file(main_path, errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Backend observability validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
