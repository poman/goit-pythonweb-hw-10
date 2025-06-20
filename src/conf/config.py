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

    # JWT settings
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Email settings
    mail_username: str = "example@meta.ua"
    mail_password: str = "secretPassword"
    mail_from: str = "example@meta.ua"
    mail_port: int = 587
    mail_server: str = "smtp.meta.ua"

    # Cloudinary settings
    cloudinary_name: str = "your_cloud_name"
    cloudinary_api_key: str = "your_api_key"
    cloudinary_api_secret: str = "your_api_secret"


settings = Settings()
