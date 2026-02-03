from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3] 

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30

    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()
