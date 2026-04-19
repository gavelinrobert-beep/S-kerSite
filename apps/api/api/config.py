"""API configuration via pydantic-settings."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+asyncpg://sakersite:changeme_postgres@localhost:5432/sakersite"

    # JWT
    jwt_secret_key: str = "dev_secret_change_in_prod"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # S3 / MinIO
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "changeme_minio"
    s3_bucket: str = "sakersite-events"

    # Edge API key
    api_key_edge: str = "dev_edge_key"

    # Retention
    retention_days: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Logging
    log_level: str = "INFO"

    def model_post_init(self, __context: object) -> None:
        # Handle comma-separated CORS origins from env string
        if isinstance(self.cors_origins, str):
            object.__setattr__(
                self,
                "cors_origins",
                [o.strip() for o in self.cors_origins.split(",")],
            )


settings = Settings()
