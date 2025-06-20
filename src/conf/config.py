from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql://username:password@localhost:5432/contacts_db"

    debug: bool = True

    postgres_db: str = "contacts_db"
    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432


settings = Settings()
