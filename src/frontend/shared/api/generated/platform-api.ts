// AUTO-GENERATED FROM specs/openapi/platform.openapi.yaml.
// DO NOT EDIT MANUALLY.

import type { HttpClient } from "@/shared/api/http-client";
import type { ApiResponse } from "@/shared/api/types";

export interface LivenessProbe {
  status: "ok";
  service: string;
}

export interface DependencyProbe {
  name: string;
  status: "ok" | "error";
  detail?: string | null;
}

export interface ReadinessProbe {
  status: "ok" | "error";
  service: string;
  checks: readonly DependencyProbe[];
}

export const platformApiPaths = Object.freeze({
  readLiveness: "/api/v1/system/livez",
  readReadiness: "/api/v1/system/readyz",
  readHealth: "/api/v1/system/health",
});

export function readLiveness(client: HttpClient): Promise<ApiResponse<LivenessProbe>> {
  return client.requestJson<LivenessProbe>(platformApiPaths.readLiveness);
}

export function readReadiness(client: HttpClient): Promise<ApiResponse<ReadinessProbe>> {
  return client.requestJson<ReadinessProbe>(platformApiPaths.readReadiness);
}

export function readHealth(client: HttpClient): Promise<ApiResponse<ReadinessProbe>> {
  return client.requestJson<ReadinessProbe>(platformApiPaths.readHealth);
}
