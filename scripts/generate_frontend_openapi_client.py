from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "specs" / "openapi" / "platform.openapi.yaml"
GENERATED_API_PATH = ROOT / "src" / "frontend" / "shared" / "api" / "generated" / "platform-api.ts"


def load_spec() -> dict[str, Any]:
    return yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))


def extract_ref_name(ref: str) -> str:
    return ref.rsplit("/", maxsplit=1)[-1]


def render_typescript_type(schema: dict[str, Any]) -> str:
    if "$ref" in schema:
        return extract_ref_name(schema["$ref"])

    if "const" in schema:
        return json.dumps(schema["const"])

    if "enum" in schema:
        return " | ".join(json.dumps(value) for value in schema["enum"])

    if "anyOf" in schema:
        return " | ".join(render_typescript_type(item) for item in schema["anyOf"])

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        return " | ".join(render_typescript_type({"type": item}) for item in schema_type)
    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "null":
        return "null"
    if schema_type == "array":
        return f"readonly {render_typescript_type(schema['items'])}[]"
    if schema_type == "object":
        return "Record<string, unknown>"

    msg = f"unsupported schema in frontend generator: {schema!r}"
    raise RuntimeError(msg)


def render_component(name: str, schema: dict[str, Any]) -> list[str]:
    schema_type = schema.get("type")
    if schema_type != "object":
        return [f"export type {name} = {render_typescript_type(schema)};", ""]

    required_fields = set(schema.get("required", ()))
    lines = [f"export interface {name} {{"]
    for property_name, property_schema in schema.get("properties", {}).items():
        optional_marker = "" if property_name in required_fields else "?"
        lines.append(f"  {property_name}{optional_marker}: {render_typescript_type(property_schema)};")
    lines.append("}")
    lines.append("")
    return lines


def render_operation_function(path_name: str, method_name: str, operation: dict[str, Any]) -> list[str]:
    operation_id = operation["operationId"]
    response_schema = (
        operation.get("responses", {})
        .get("200", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )
    if not isinstance(response_schema, dict) or "$ref" not in response_schema:
        msg = f"{method_name.upper()} {path_name} is missing a 200 JSON response schema"
        raise RuntimeError(msg)

    response_type = extract_ref_name(response_schema["$ref"])
    return [
        f"export function {operation_id}(client: HttpClient): Promise<ApiResponse<{response_type}>> {{",
        f'  return client.requestJson<{response_type}>(platformApiPaths.{operation_id});',
        "}",
        "",
    ]


def render_generated_api(spec: dict[str, Any]) -> str:
    lines = [
        "// AUTO-GENERATED FROM specs/openapi/platform.openapi.yaml.",
        "// DO NOT EDIT MANUALLY.",
        "",
        'import type { HttpClient } from "@/shared/api/http-client";',
        'import type { ApiResponse } from "@/shared/api/types";',
        "",
    ]

    components = spec.get("components", {}).get("schemas", {})
    for component_name, component_schema in components.items():
        lines.extend(render_component(component_name, component_schema))

    lines.extend(
        [
            "export const platformApiPaths = Object.freeze({",
        ]
    )
    for path_name, path_item in spec.get("paths", {}).items():
        for method_name, operation in path_item.items():
            _ = method_name
            lines.append(f'  {operation["operationId"]}: "{path_name}",')
    lines.extend(
        [
            "});",
            "",
        ]
    )

    for path_name, path_item in spec.get("paths", {}).items():
        for method_name, operation in path_item.items():
            lines.extend(render_operation_function(path_name, method_name, operation))

    return "\n".join(lines).rstrip() + "\n"


def write_generated_api(content: str) -> None:
    GENERATED_API_PATH.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_API_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate frontend OpenAPI client/types from specs.")
    parser.add_argument("--check", action="store_true", help="Fail if the generated file is out of date.")
    args = parser.parse_args()

    rendered = render_generated_api(load_spec())
    current = GENERATED_API_PATH.read_text(encoding="utf-8") if GENERATED_API_PATH.is_file() else ""

    if args.check:
        if current != rendered:
            print(
                "Generated frontend OpenAPI client is out of date. "
                "Run `uv run --project src/backend python scripts/generate_frontend_openapi_client.py`."
            )
            return 1
        print("Frontend OpenAPI client generation is up to date.")
        return 0

    write_generated_api(rendered)
    print(f"Generated frontend OpenAPI client: {GENERATED_API_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
