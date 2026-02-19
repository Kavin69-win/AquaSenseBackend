from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AquaSense"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"
    
    # --- GROQ CONFIGURATION ---
    GROQ_API_KEY: SecretStr = SecretStr("gsk_placeholder")
    
    SECRET_KEY: str = "kavin_sharma_aquasense_2026"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()