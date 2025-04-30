# app/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="forbid"  # запрещаем «лишние» поля
    )

    # Параметры подключения к Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str  # например: postgresql://user:pass@host:port/dbname

    # Настройки безопасности и JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: float = 30
    REFRESH_TOKEN_EXPIRE_DAYS: float = 7
    ALGORITHM: str = "HS256"


settings = Settings()
