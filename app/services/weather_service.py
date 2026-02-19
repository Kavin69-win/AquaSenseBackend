from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
# REMOVED: from datetime import timezone (We don't want timezone aware objects)
import httpx
from app.db import models

OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"

async def get_district_weather(district_id: int, lat: float, lon: float, db: AsyncSession):
    # 1. Check Cache
    # FIX: Use datetime.utcnow() which returns a "naive" timestamp (no timezone info)
    # This matches your PostgreSQL 'TIMESTAMP WITHOUT TIME ZONE' column.
    valid_after = datetime.utcnow() - timedelta(minutes=30)
    
    stmt = (
        select(models.WeatherCache)
        .where(
            models.WeatherCache.district_id == district_id,
            models.WeatherCache.last_updated > valid_after
        )
    )
    result = await db.execute(stmt)
    cached = result.scalars().first()

    if cached:
        return {
            "temp": cached.temp_celsius,
            "precip": cached.precipitation_probability,
            "is_raining": cached.is_raining
        }

    # 2. Fetch Live Data (If cache missed)
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "precipitation", "rain"],
        "hourly": "precipitation_probability",
        "forecast_days": 1
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OPENMETEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Parse API Response
            current = data.get("current", {})
            hourly = data.get("hourly", {})
            
            # Get max precip probability for the next 24h
            max_precip_prob = 0
            if "precipitation_probability" in hourly:
                max_precip_prob = max(hourly["precipitation_probability"][:24])

            new_weather_data = {
                "temp": current.get("temperature_2m", 25.0),
                "precip": max_precip_prob,
                "is_raining": current.get("rain", 0) > 0 or current.get("precipitation", 0) > 0
            }

            # 3. Update Cache
            # First, delete old entry if exists
            await db.execute(
                models.WeatherCache.__table__.delete().where(
                    models.WeatherCache.district_id == district_id
                )
            )
            
            # Create new entry
            # FIX: Use datetime.utcnow() here too
            cache_entry = models.WeatherCache(
                district_id=district_id,
                temp_celsius=new_weather_data["temp"],
                precipitation_probability=new_weather_data["precip"],
                is_raining=new_weather_data["is_raining"],
                last_updated=datetime.utcnow() 
            )
            db.add(cache_entry)
            await db.commit()
            
            return new_weather_data

        except Exception as e:
            print(f"Weather API Error: {e}")
            # Fallback if API fails
            return {"temp": 25.0, "precip": 0, "is_raining": False}