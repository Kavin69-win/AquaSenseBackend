from pydantic import BaseModel, Field

class WeatherData(BaseModel):
    """
    Normalized weather data structure.
    Independent of specific API providers (OpenMeteo/IMD).
    """
    # Location context
    district: str = Field(..., description="Target district in Punjab")
    
    # Core Metrics
    temp_celsius: float = Field(..., description="Current temperature")
    humidity_percent: float = Field(..., description="Current relative humidity")
    
    # Rainfall: mm (last 24h or forecast)
    rainfall_mm: float = Field(..., ge=0.0, description="Precipitation volume in mm")
    
    # Wind Speed: m/s (SI Unit) - often APIs give km/h, we must convert
    wind_speed_ms: float = Field(..., ge=0.0, description="Wind speed in meters per second")

    # Localized Summaries
    forecast_summary_en: str = Field(..., description="Short forecast summary in English")
    forecast_summary_hi: str = Field(..., description="Short forecast summary in Hindi")