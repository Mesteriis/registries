from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="REGISTRIES_",
        extra="ignore",
    )

    app_name: str = "Registries API"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    api_prefix: str = "/api"
    postgres_dsn: str = "postgresql+asyncpg://registries:registries@localhost:5432/registries"
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
