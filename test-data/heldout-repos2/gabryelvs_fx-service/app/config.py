from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    redis_url: str = "redis://localhost:6379/0"
    frankfurter_base_url: str = "https://api.frankfurter.dev/v1"
    refresh_interval_seconds: int = 3600
    base_currency: str = "EUR"


settings = Settings()
