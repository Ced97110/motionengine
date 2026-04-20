"""Application settings loaded from environment."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["dev", "staging", "prod"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.local", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Environment = "dev"
    log_level: str = "INFO"

    database_url: str = Field(
        default="postgresql+asyncpg://motion:motion_dev@localhost:5432/motion",
        description="SQLAlchemy URL; asyncpg driver in prod, sync psycopg for Alembic.",
    )

    clerk_secret_key: str = "sk_test_unset"
    clerk_jwks_url: str = ""
    clerk_issuer: str = ""
    clerk_authorized_parties: str = ""
    clerk_webhook_secret: str = ""

    @property
    def clerk_authorized_parties_list(self) -> list[str]:
        return [p.strip() for p in self.clerk_authorized_parties.split(",") if p.strip()]

    anthropic_api_key: str = "unset"

    redis_url: str = ""
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket: str = ""

    @property
    def is_prod(self) -> bool:
        return self.environment == "prod"

    @property
    def sync_database_url(self) -> str:
        """Alembic runs synchronously; swap driver for migrations."""
        return self.database_url.replace("+asyncpg", "+psycopg")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
