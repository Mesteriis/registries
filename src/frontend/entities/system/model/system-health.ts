import type { ReadinessProbe } from "@/shared/api";

export type { DependencyProbe, ReadinessProbe } from "@/shared/api";

export type SystemHealthStatus = ReadinessProbe["status"];
