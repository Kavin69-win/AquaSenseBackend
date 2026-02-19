import httpx
import logging
from app.schemas.weather import WeatherData
from app.core.geo_data import DISTRICT_COORDINATES

logger = logging.getLogger("aquasense.weather")

class OpenMeteoProvider:
    """
    Production-grade Weather Adapter.
    Fetches real-time climate data based on Punjab district coordinates.
    """
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    async def get_district_weather(self, district: str) -> WeatherData:
        # Retrieve coordinates for the specific district
        coords = DISTRICT_COORDINATES.get(district)
        
        if not coords:
            logger.warning(f"Coordinates missing for {district}. Defaulting to Ludhiana.")
            coords = DISTRICT_COORDINATES["Ludhiana"]
        
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            # Added wind_speed_10m to satisfy your schema requirement
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
            "daily": ["precipitation_sum"],
            "timezone": "auto",
            "forecast_days": 1
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()

            # Extract wind speed (API gives km/h, Schema wants m/s)
            wind_kph = data["current"].get("wind_speed_10m", 0.0)
            wind_ms = wind_kph * 0.27778  # Conversion factor

            return WeatherData(
                district=district,  # REQUIRED by your schema
                temp_celsius=data["current"]["temperature_2m"],
                humidity_percent=data["current"]["relative_humidity_2m"],
                rainfall_mm=data["daily"]["precipitation_sum"][0],
                wind_speed_ms=round(wind_ms, 2), # REQUIRED by your schema
                forecast_summary_en=f"Live conditions for {district}",
                forecast_summary_hi=f"{district} के लिए लाइव मौसम"
            )

        except (httpx.HTTPError, KeyError, IndexError) as e:
            logger.error(f"Weather API Error: {str(e)}")
            # Fallback must ALSO match the schema structure perfectly
            return WeatherData(
                district=district,
                temp_celsius=25.0,
                humidity_percent=50.0,
                rainfall_mm=0.0,
                wind_speed_ms=2.5,
                forecast_summary_en="Weather service unavailable (Fallback)",
                forecast_summary_hi="मौसम सेवा अनुपलब्ध है"
            )

# Singleton Export
weather_service = OpenMeteoProvider()