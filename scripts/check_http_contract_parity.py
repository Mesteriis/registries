from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from generate_frontend_openapi_client import GENERATED_API_PATH, render_generated_api


ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = ROOT / "src" / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from core.bootstrap.app import create_app


SPEC_PATH = ROOT / "specs" / "openapi" / "platform.openapi.yaml"
FRONTEND_SHARED_API_INDEX_PATH = ROOT / "src" / "frontend" / "shared" / "api" / "index.ts"
FRONTEND_ENTITY_CLIENT_PATH = ROOT / "src" / "frontend" / "entities" / "system" / "api" / "get-system-health.ts"
FRONTEND_ENTITY_MODEL_PATH = ROOT / "src" / "frontend" / "entities" / "system" / "model" / "system-health.ts"


def load_spec() -> dict[str, Any]:
    return yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))


def load_runtime_openapi() -> dict[str, Any]:
    return create_app().openapi()


def extract_ref_name(ref: str) -> str:
    return ref.rsplit("/", maxsplit=1)[-1]


def normalize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    if "$ref" in schema:
        return {"$ref": extract_ref_name(schema["$ref"])}

    if "anyOf" in schema:
        return {
            "anyOf": tuple(sorted((normalize_schema(item) for item in schema["anyOf"]), key=_sort_key)),
        }

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        return {
            "anyOf": tuple(sorted(({"type": item} for item in schema_type), key=_sort_key)),
        }

    normalized: dict[str, Any] = {}
    if schema_type is not None:
        normalized["type"] = schema_type
    if "const" in schema:
        normalized["const"] = schema["const"]
    if "enum" in schema:
        normalized["enum"] = tuple(schema["enum"])
    if "required" in schema:
        normalized["required"] = tuple(schema["required"])
    if "properties" in schema:
        normalized["properties"] = {
            name: normalize_schema(property_schema)
            for name, property_schema in schema["properties"].items()
        }
    if "items" in schema:
        normalized["items"] = normalize_schema(schema["items"])
    if "additionalProperties" in schema:
        normalized["additionalProperties"] = schema["additionalProperties"]
    return normalized


def _sort_key(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def response_schema_name(operation: dict[str, Any], status_code: str) -> str | None:
    schema = (
        operation.get("responses", {})
        .get(status_code, {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )
    if not isinstance(schema, dict) or "$ref" not in schema:
        return None
    return extract_ref_name(schema["$ref"])


def collect_referenced_schemas(schema_name: str, components: dict[str, Any]) -> set[str]:
    pending = [schema_name]
    seen: set[str] = set()

    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)

        component = components[current]
        for ref_name in find_refs(component):
            pending.append(ref_name)

    return seen


def find_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "$ref" and isinstance(item, str):
                refs.add(extract_ref_name(item))
            else:
                refs.update(find_refs(item))
    elif isinstance(value, list):
        for item in value:
            refs.update(find_refs(item))
    return refs


def validate_backend_against_spec(
    spec_openapi: dict[str, Any],
    runtime_openapi: dict[str, Any],
    errors: list[str],
) -> None:
    spec_title = spec_openapi.get("info", {}).get("title")
    runtime_title = runtime_openapi.get("info", {}).get("title")
    if spec_title != runtime_title:
        errors.append(
            f"OpenAPI title drift detected: spec has {spec_title!r} while runtime has {runtime_title!r}"
        )

    spec_paths = spec_openapi.get("paths", {})
    runtime_paths = runtime_openapi.get("paths", {})

    for path_name, spec_path_item in spec_paths.items():
        runtime_path_item = runtime_paths.get(path_name)
        if runtime_path_item is None:
            errors.append(f"runtime OpenAPI is missing spec path: {path_name}")
            continue

        for method_name, spec_operation in spec_path_item.items():
            runtime_operation = runtime_path_item.get(method_name)
            if runtime_operation is None:
                errors.append(f"runtime OpenAPI is missing {method_name.upper()} {path_name}")
                continue

            for status_code in spec_operation.get("responses", {}):
                spec_schema_name = response_schema_name(spec_operation, status_code)
                runtime_schema_name = response_schema_name(runtime_operation, status_code)
                if spec_schema_name != runtime_schema_name:
                    errors.append(
                        f"response schema drift for {method_name.upper()} {path_name} {status_code}: "
                        f"spec={spec_schema_name!r}, runtime={runtime_schema_name!r}"
                    )

    spec_components = spec_openapi.get("components", {}).get("schemas", {})
    runtime_components = runtime_openapi.get("components", {}).get("schemas", {})

    referenced_schema_names: set[str] = set()
    for path_item in spec_paths.values():
        for operation in path_item.values():
            for status_code in operation.get("responses", {}):
                schema_name = response_schema_name(operation, status_code)
                if schema_name is not None:
                    referenced_schema_names.update(collect_referenced_schemas(schema_name, spec_components))

    for schema_name in sorted(referenced_schema_names):
        spec_schema = spec_components.get(schema_name)
        runtime_schema = runtime_components.get(schema_name)
        if spec_schema is None or runtime_schema is None:
            errors.append(f"missing schema in spec/runtime parity set: {schema_name}")
            continue

        if normalize_schema(spec_schema) != normalize_schema(runtime_schema):
            errors.append(
                f"schema drift detected for {schema_name}: "
                f"spec={normalize_schema(spec_schema)!r}, runtime={normalize_schema(runtime_schema)!r}"
            )


def derive_health_contract(spec_openapi: dict[str, Any]) -> tuple[str, str, dict[str, Any], dict[str, Any]]:
    for path_name, path_item in spec_openapi.get("paths", {}).items():
        if not path_name.endswith("/health"):
            continue
        operation = path_item.get("get")
        if operation is None:
            continue
        schema_name = response_schema_name(operation, "200")
        if schema_name is None:
            msg = f"spec health path {path_name} does not declare a JSON response schema"
            raise RuntimeError(msg)
        components = spec_openapi.get("components", {}).get("schemas", {})
        return path_name, schema_name, components[schema_name], components

    msg = "spec does not define a canonical GET /health path"
    raise RuntimeError(msg)


def validate_frontend_against_spec(spec_openapi: dict[str, Any], errors: list[str]) -> None:
    health_path, schema_name, _schema, _components = derive_health_contract(spec_openapi)
    generated_expected = render_generated_api(spec_openapi)
    generated_actual = GENERATED_API_PATH.read_text(encoding="utf-8") if GENERATED_API_PATH.is_file() else ""
    if generated_actual != generated_expected:
        errors.append(
            "generated frontend OpenAPI client is out of date with specs/openapi/platform.openapi.yaml; "
            "run scripts/generate_frontend_openapi_client.py"
        )

    shared_api_index_text = FRONTEND_SHARED_API_INDEX_PATH.read_text(encoding="utf-8")
    if 'export * from "@/shared/api/generated/platform-api";' not in shared_api_index_text:
        errors.append("shared/api index must re-export the generated OpenAPI client")

    entity_client_text = FRONTEND_ENTITY_CLIENT_PATH.read_text(encoding="utf-8")
    if "readHealth(httpClient)" not in entity_client_text:
        errors.append("entities/system/api/get-system-health.ts must delegate to generated readHealth(httpClient)")
    if "appConfig.systemHealthPath" in entity_client_text:
        errors.append("entities/system/api/get-system-health.ts must not keep a handwritten health path binding")

    entity_model_text = FRONTEND_ENTITY_MODEL_PATH.read_text(encoding="utf-8")
    if 'export type { DependencyProbe, ReadinessProbe } from "@/shared/api";' not in entity_model_text:
        errors.append("entities/system/model/system-health.ts must re-export generated contract types from shared/api")
    if 'export type SystemHealthStatus = ReadinessProbe["status"];' not in entity_model_text:
        errors.append("entities/system/model/system-health.ts must derive SystemHealthStatus from the generated ReadinessProbe type")

    if f'readHealth: "{health_path}"' not in generated_actual:
        errors.append(
            f"generated platformApiPaths.readHealth must match spec path {health_path!r}"
        )
    if f"export function readHealth(client: HttpClient): Promise<ApiResponse<{schema_name}>>" not in generated_actual:
        errors.append(
            f"generated readHealth function must return ApiResponse<{schema_name}>"
        )




def main() -> int:
    errors: list[str] = []
    spec_openapi = load_spec()
    runtime_openapi = load_runtime_openapi()

    validate_backend_against_spec(spec_openapi, runtime_openapi, errors)
    validate_frontend_against_spec(spec_openapi, errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    print("HTTP contract parity validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
