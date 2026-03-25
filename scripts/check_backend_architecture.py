from __future__ import annotations

import ast
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"
BACKEND_DIRS = ("api", "apps", "core", "runtime")
BACKEND_IMPORT_PREFIXES = tuple(f"{name}." for name in BACKEND_DIRS)
CONTEXT_LAYERS = {"api", "application", "contracts", "domain", "infrastructure"}
ALLOWED_SAME_CONTEXT_IMPORTS: dict[str, set[str]] = {
    "api": {"api", "application", "contracts", "domain"},
    "application": {"application", "contracts", "domain"},
    "contracts": {"contracts"},
    "domain": {"domain"},
    "infrastructure": {"application", "contracts", "domain", "infrastructure"},
}


def module_parts_for(path: Path) -> list[str]:
    return list(path.relative_to(BACKEND_ROOT).with_suffix("").parts)


def parse_imported_modules(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        if node.module is None:
            return []
        return [node.module]
    return []


def validate_context_imports(parts: list[str], imported: str, errors: list[str], path: Path) -> None:
    if len(parts) < 4 or parts[0] != "apps":
        return

    context_name = parts[1]
    layer_name = parts[2]

    if layer_name not in CONTEXT_LAYERS or not imported.startswith("apps."):
        return

    imported_parts = imported.split(".")
    if len(imported_parts) < 3:
        errors.append(f"{path.relative_to(ROOT)} imports incomplete app module '{imported}'")
        return

    imported_context = imported_parts[1]
    imported_layer = imported_parts[2]

    if imported_context == context_name:
        allowed = ALLOWED_SAME_CONTEXT_IMPORTS[layer_name]
        if imported_layer not in allowed:
            errors.append(
                f"{path.relative_to(ROOT)} violates same-context layer rule: "
                f"{layer_name} -> {imported_layer} via '{imported}'"
            )
        return

    if imported_layer != "contracts":
        errors.append(
            f"{path.relative_to(ROOT)} imports internal module of another context via '{imported}'; "
            "only contracts are allowed cross-context"
        )


def validate_core_imports(parts: list[str], imported: str, errors: list[str], path: Path) -> None:
    if len(parts) < 2 or parts[0] != "core":
        return

    is_bootstrap = len(parts) >= 2 and parts[1] == "bootstrap"
    if is_bootstrap:
        return

    if imported == "api" or imported == "runtime" or imported == "apps":
        errors.append(
            f"{path.relative_to(ROOT)} uses forbidden dependency from core module via '{imported}'"
        )
        return

    if imported.startswith(("api.", "runtime.", "apps.")):
        errors.append(
            f"{path.relative_to(ROOT)} uses forbidden dependency from core module via '{imported}'"
        )


def validate_runtime_imports(parts: list[str], imported: str, errors: list[str], path: Path) -> None:
    if len(parts) < 2 or parts[0] != "runtime":
        return

    if imported == "api" or imported.startswith("api."):
        errors.append(f"{path.relative_to(ROOT)} must not import API layer via '{imported}'")


def is_backend_import(imported: str) -> bool:
    return imported in BACKEND_DIRS or imported.startswith(BACKEND_IMPORT_PREFIXES)


def validate_file(path: Path, errors: list[str]) -> None:
    parts = module_parts_for(path)
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    for node in ast.walk(tree):
        for imported in parse_imported_modules(node):
            if not is_backend_import(imported):
                continue
            validate_context_imports(parts, imported, errors, path)
            validate_core_imports(parts, imported, errors, path)
            validate_runtime_imports(parts, imported, errors, path)


def main() -> int:
    errors: list[str] = []

    for backend_dir in BACKEND_DIRS:
        for path in sorted((BACKEND_ROOT / backend_dir).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            validate_file(path, errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("Backend architecture validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
