from __future__ import annotations

from pydantic.alias_generators import to_camel
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UI_",
        alias_generator=to_camel,
    )

    backend_path: str = "/backend/"
    login_path: str = "/login/"
    public_paths: list[str] = [
        "/login/",
        "/logout/",
    ]
    redirect_after_login_path: str = "/"


settings = Settings()
