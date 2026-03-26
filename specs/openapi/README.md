# OpenAPI

Store canonical HTTP API contracts here using:

- `*.openapi.yaml`
- `*.openapi.yml`
- `*.openapi.json`

Current canonical backend/frontend reference contract:

- [platform.openapi.yaml](./platform.openapi.yaml)

The health reference slice must stay aligned across:

- this OpenAPI document;
- backend FastAPI routes and response models;
- frontend typed client contracts and tests.
