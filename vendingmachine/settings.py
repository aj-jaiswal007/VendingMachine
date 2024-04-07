from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_name: str
    database_user: str
    database_password: str
    database_host: str = "localhost"
    database_port: int = 5432


@lru_cache
def get_settings():
    return Settings()  # type: ignore
