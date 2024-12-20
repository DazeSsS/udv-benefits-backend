from datetime import timedelta
from pydantic import root_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str 
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    DB_HOST: str

    BALANCE_DEFAULT: int
    TIMEZONE: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_LIFETIME_MINUTES: int = 15
    REFRESH_LIFETIME_DAYS: int = 30
    PUBLIC_API: bool
    AUTH_URL: str
    USERS_FILE_DIR: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_STORAGE_BUCKET_NAME: str
    AWS_ENDPOINT_URL: str

    SMTP_HOST: str
    SMTP_USER: str
    SMTP_PORT: int
    SMTP_PASSWORD: str

    TEST_MODE: bool
    TEST_EMAILS: str

    LOCAL_ORIGIN: str
    MAIN_ORIGIN: str

    ACCESS_LIFETIME: timedelta | None = None
    REFRESH_LIFETIME: timedelta | None = None

    def __init__(self, **values):
        super().__init__(**values)
        self.ACCESS_LIFETIME = timedelta(minutes=self.ACCESS_LIFETIME_MINUTES)
        self.REFRESH_LIFETIME = timedelta(days=self.REFRESH_LIFETIME_DAYS)

    def get_db_url(self, in_docker=True):
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.DB_HOST if in_docker else self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    def get_sync_db_url(self, in_docker=True):
        return (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.DB_HOST if in_docker else self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
