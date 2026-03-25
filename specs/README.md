# Specs

`specs/` is the source of truth for contract-first development.

Rules:

- OpenAPI documents live in `specs/openapi/` and use `*.openapi.yaml|yml|json`
- AsyncAPI documents live in `specs/asyncapi/` and use `*.asyncapi.yaml|yml|json`
- JSON Schema documents live in `specs/jsonschema/` and use `*.schema.json`
- Generated clients, SDKs and DTOs are derived artifacts and must not replace the source contracts in `specs/`
