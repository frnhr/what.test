from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="UI_")

    backend_path: str = "/backend/"
    login_path: str = "/login/"
    public_paths: list[str] = [
        "/login/",
        "/logout/",
    ]


settings = Settings()
