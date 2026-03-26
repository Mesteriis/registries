import { type ApiResponse, httpClient, readHealth, type ReadinessProbe } from "@/shared/api";

export function getSystemHealth(): Promise<ApiResponse<ReadinessProbe>> {
  return readHealth(httpClient);
}
