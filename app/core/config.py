from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./cityflow_dev.db"
    frontend_origin: str = "http://localhost:3000"
    provider_mode: str = "mock"  # mock | live | hybrid
    auth_mode: str = "mock"  # mock | provider
    auth_enabled: bool = False

    tomtom_api_key: str | None = None
    tomtom_base_url: str = "https://api.tomtom.com"
    open_meteo_base_url: str = "https://api.open-meteo.com/v1"
    open_meteo_aqi_base_url: str = "https://air-quality-api.open-meteo.com/v1"

    # Delhi NCR is the only supported operating region.
    delhi_lat_min: float = 28.20
    delhi_lat_max: float = 29.00
    delhi_lon_min: float = 76.80
    delhi_lon_max: float = 77.60

    request_timeout_seconds: float = 12.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @field_validator("provider_mode")
    @classmethod
    def valid_provider_mode(cls, value: str) -> str:
        value = value.lower().strip()
        if value not in {"mock", "live", "hybrid"}:
            raise ValueError("PROVIDER_MODE must be mock, live, or hybrid")
        return value

    @field_validator("auth_mode")
    @classmethod
    def valid_auth_mode(cls, value: str) -> str:
        value = value.lower().strip()
        if value not in {"mock", "provider"}:
            raise ValueError("AUTH_MODE must be mock or provider")
        return value

    @property
    def frontend_origins(self) -> list[str]:
        return [item.strip() for item in self.frontend_origin.split(",") if item.strip()]

    @property
    def has_tomtom(self) -> bool:
        return bool(self.tomtom_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
