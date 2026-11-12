"""Central configuration.

Every setting comes from environment variables (or a .env file at the repo root).
Locally you use .env; on Render/GitHub Actions you set the same names in their
dashboards. The code never contains a secret.
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=REPO_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongodb_uri: str
    mongodb_db: str = "fraud_copilot"
    gemini_api_key: str = ""
    app_env: str = "dev"


@lru_cache
def get_settings() -> Settings:
    """Read settings once and reuse them (cheap, and easy to override in tests)."""
    return Settings()
