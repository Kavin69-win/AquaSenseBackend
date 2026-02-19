from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    """
    AquaSense Configuration Engine.
    Implements Level 280 Safe-Fallback logic to prevent ValidationErrors.
    """
    
    # --- PROJECT INFO ---
    PROJECT_NAME: str = "AquaSense"
    API_V1_STR: str = "/api/v1"
    
    # --- DATABASE CONFIGURATION ---
    # We provide your specific credentials as a default value.
    # If a .env file is found, it will override this value.
    DATABASE_URL: str = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"
    
    # --- SECURITY ---
    SECRET_KEY: str = "kavin_sharma_aquasense_2026"
    
    # --- IOT SETTINGS ---
    # Threshold for management allowed depletion
    MOISTURE_MAD_THRESHOLD: float = 0.5
    # Change threshold for flagging sensor anomalies (30%)
    MOISTURE_DELTA_ANOMALY: float = 0.3

    # --- SETTINGS CONFIGURATION ---
    model_config = SettingsConfigDict(
        # Look for the .env file but don't crash if it's missing
        env_file=".env",
        env_file_encoding="utf-8",
        # Ignore extra variables in the .env file to prevent validation crashes
        extra="ignore",
        case_sensitive=True
    )

# Initialize the settings object
settings = Settings()