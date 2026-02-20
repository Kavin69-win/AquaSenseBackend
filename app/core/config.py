from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    PROJECT_NAME: str = "AquaSense"
    DATABASE_URL: str
    GROQ_API_KEY: SecretStr
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()