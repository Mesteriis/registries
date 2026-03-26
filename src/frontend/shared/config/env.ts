import {
  isNonEmptyString,
  trimTrailingSlash,
} from "@/shared/lib";

export interface AppObservabilityConfig {
  enabled: boolean;
  environment: string;
  release: string;
  serviceName: string;
  sentryEnabled: boolean;
  glitchtipDsn: string;
  tracingEnabled: boolean;
  otlpEndpoint: string;
  webVitalsEnabled: boolean;
  traceSampleRate: number;
  uiTelemetryEnabled: boolean;
  routerTelemetryEnabled: boolean;
  requestCorrelationEnabled: boolean;
}

export interface AppConfig {
  appName: string;
  apiBaseUrl: string;
  observability: AppObservabilityConfig;
}

function readApiBaseUrl(): string {
  const configuredBaseUrl = trimTrailingSlash(readStringEnv("VITE_API_BASE_URL", ""));
  const runtimeOrigin = globalThis.location?.origin;

  if (isNonEmptyString(configuredBaseUrl)) {
    return configuredBaseUrl;
  }

  if (isNonEmptyString(runtimeOrigin)) {
    return trimTrailingSlash(runtimeOrigin);
  }

  return "http://localhost:5173";
}

function readStringEnv(name: keyof ImportMetaEnv, fallback: string): string {
  const rawValue = import.meta.env[name];

  if (!isNonEmptyString(rawValue)) {
    return fallback;
  }

  return rawValue.trim();
}

function readBooleanEnv(name: keyof ImportMetaEnv, fallback: boolean): boolean {
  const rawValue = import.meta.env[name];

  if (!isNonEmptyString(rawValue)) {
    return fallback;
  }

  const normalizedValue = rawValue.trim().toLowerCase();

  if (["1", "true", "yes", "on"].includes(normalizedValue)) {
    return true;
  }

  if (["0", "false", "no", "off"].includes(normalizedValue)) {
    return false;
  }

  return fallback;
}

function readNumberEnv(
  name: keyof ImportMetaEnv,
  fallback: number,
  min: number,
  max: number,
): number {
  const rawValue = import.meta.env[name];

  if (!isNonEmptyString(rawValue)) {
    return fallback;
  }

  const parsedValue = Number(rawValue);
  if (!Number.isFinite(parsedValue)) {
    return fallback;
  }

  return Math.min(max, Math.max(min, parsedValue));
}

export const appConfig: AppConfig = Object.freeze({
  appName: readStringEnv("VITE_APP_NAME", "Fullstack Template"),
  apiBaseUrl: readApiBaseUrl(),
  observability: Object.freeze({
    enabled: readBooleanEnv("VITE_OBSERVABILITY_ENABLED", false),
    environment: readStringEnv("VITE_OBSERVABILITY_ENVIRONMENT", import.meta.env.MODE),
    release: readStringEnv("VITE_OBSERVABILITY_RELEASE", "frontend-local"),
    serviceName: readStringEnv("VITE_OBSERVABILITY_SERVICE_NAME", "fullstack-template-frontend"),
    sentryEnabled: readBooleanEnv("VITE_OBSERVABILITY_SENTRY_ENABLED", false),
    glitchtipDsn: readStringEnv("VITE_OBSERVABILITY_GLITCHTIP_DSN", ""),
    tracingEnabled: readBooleanEnv("VITE_OBSERVABILITY_TRACING_ENABLED", false),
    otlpEndpoint: trimTrailingSlash(readStringEnv("VITE_OBSERVABILITY_OTLP_ENDPOINT", "")),
    webVitalsEnabled: readBooleanEnv("VITE_OBSERVABILITY_WEB_VITALS_ENABLED", false),
    traceSampleRate: readNumberEnv("VITE_OBSERVABILITY_TRACE_SAMPLE_RATE", 0.1, 0, 1),
    uiTelemetryEnabled: readBooleanEnv("VITE_OBSERVABILITY_UI_TELEMETRY_ENABLED", false),
    routerTelemetryEnabled: readBooleanEnv("VITE_OBSERVABILITY_ROUTER_TELEMETRY_ENABLED", true),
    requestCorrelationEnabled: readBooleanEnv(
      "VITE_OBSERVABILITY_REQUEST_CORRELATION_ENABLED",
      true,
    ),
  }),
});
