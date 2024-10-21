from pydantic_settings import BaseSettings, SettingsConfigDict

import sys

class Settings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str 
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DB_HOST: str
    COINS_DEFAULT: int
    TIMEZONE: str

    model_config = SettingsConfigDict(env_file='.env')

    def get_db_url(self, in_docker=True):
        return (
            f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.DB_HOST if in_docker else self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )


settings = Settings()
