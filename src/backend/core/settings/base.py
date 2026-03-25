from functools import lru_cache

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = "Registries API"
    version: str = "0.1.0"
    environment: str = "local"


class ApiSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    prefix: str = "/api"

    @field_validator("prefix")
    @classmethod
    def normalize_prefix(cls, value: str) -> str:
        return value if value.startswith("/") else f"/{value}"


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    postgres_dsn: str = "postgresql+asyncpg://registries:registries@localhost:5432/registries"
    redis_url: str = "redis://localhost:6379/0"


class BrokerSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    taskiq_queue_name: str = "registries:taskiq"
    taskiq_consumer_group_name: str = "registries:backend"


class ObservabilitySettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool = True
    logs_enabled: bool = True
    log_level: str = "INFO"
    traces_enabled: bool = False
    otlp_endpoint: str = ""
    otlp_headers: str = ""
    metrics_enabled: bool = True
    metrics_path: str = "/metrics"
    request_id_header: str = "X-Request-ID"
    correlation_id_header: str = "X-Correlation-ID"
    sentry_enabled: bool = False
    glitchtip_dsn: str = ""
    trace_sample_rate: float = 0.1
    profile_sample_rate: float = 0.0
    instrument_sqlalchemy: bool = True
    instrument_redis: bool = True
    instrument_httpx: bool = False
    service_name: str | None = None
    service_version: str | None = None
    environment: str | None = None

    @field_validator("metrics_path")
    @classmethod
    def normalize_metrics_path(cls, value: str) -> str:
        return value if value.startswith("/") else f"/{value}"

    @field_validator("request_id_header", "correlation_id_header")
    @classmethod
    def normalize_context_header(cls, value: str) -> str:
        header_name = value.strip()
        if not header_name:
            msg = "observability context header names must not be empty"
            raise ValueError(msg)
        return header_name

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("trace_sample_rate", "profile_sample_rate")
    @classmethod
    def validate_sample_rate(cls, value: float) -> float:
        if not 0.0 <= value <= 1.0:
            msg = "observability sample rates must be between 0.0 and 1.0"
            raise ValueError(msg)
        return value


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REGISTRIES_",
        env_nested_delimiter="__",
        extra="ignore",
        nested_model_default_partial_update=True,
    )

    app: AppSettings = Field(default_factory=AppSettings)
    api: ApiSettings = Field(default_factory=ApiSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    broker: BrokerSettings = Field(default_factory=BrokerSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)

    @property
    def observability_service_name(self) -> str:
        return self.observability.service_name or self.app.name

    @property
    def observability_service_version(self) -> str:
        return self.observability.service_version or self.app.version

    @property
    def observability_environment(self) -> str:
        return self.observability.environment or self.app.environment


@lru_cache
def get_settings() -> Settings:
    return Settings()
