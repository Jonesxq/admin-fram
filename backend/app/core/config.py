from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Open Admin API"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite+pysqlite:///:memory:"
    jwt_secret_key: str = "test-secret"
    jwt_expire_minutes: int = 120
    initial_admin_password: str = ""
    allow_default_admin_password: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
