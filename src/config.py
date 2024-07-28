from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str
    APP_NAME: str
    ADMIN_EMAIL: str
    ITEMS_PER_USER: int
    SECRET_SALT: str
    ALGORITHM: str
    TOKEN_EXP: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()