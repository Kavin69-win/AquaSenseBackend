from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from groq import AsyncGroq  # Native Groq Async SDK
from datetime import date

from app.db.models import SensorReading, Device, Crop, WeatherCache, User
from app.api.deps import get_db 
from app.core.config import settings

# --- 1. Groq Client Handshake ---
# Using the GROQ_API_KEY from your updated config.py
client = AsyncGroq(
    api_key=settings.GROQ_API_KEY.get_secret_value()
)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    device_id: str

@router.post("/")
async def chat_with_bot(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 1. FETCH LATEST SENSOR DATA
        sensor_query = (
            select(SensorReading)
            .where(SensorReading.device_id == request.device_id)
            .order_by(desc(SensorReading.timestamp))
        )
        sensor_result = await db.execute(sensor_query)
        latest_reading = sensor_result.scalars().first()
        
        # 2. FETCH DEVICE & OWNER DATA
        device_query = select(Device).where(Device.device_id == request.device_id)
        device_result = await db.execute(device_query)
        device_record = device_result.scalars().first()
        
        if not device_record:
            raise HTTPException(status_code=404, detail="Device not found")

        user_query = select(User).where(User.id == device_record.user_id)
        user_result = await db.execute(user_query)
        user_record = user_result.scalars().first()

        # 3. CONSTRUCT CROP CONTEXT
        crop_context = "No specific crop data available."
        if user_record and user_record.current_crop_id:
            crop_query = select(Crop).where(Crop.id == user_record.current_crop_id)
            crop_result = await db.execute(crop_query)
            crop_record = crop_result.scalars().first()
            
            if crop_record:
                sowing = user_record.sowing_date
                try:
                    days_old = (date.today() - sowing).days if sowing else "Unknown"
                except Exception:
                    days_old = "Unknown"
                
                crop_context = (
                    f"Crop: {crop_record.name}, "
                    f"Age: {days_old} days, "
                    f"Location: Punjab"
                )

        # 4. FETCH LATEST WEATHER CACHE
        weather_query = select(WeatherCache).order_by(desc(WeatherCache.updated_at))
        weather_result = await db.execute(weather_query)
        weather_record = weather_result.scalars().first()

        # 5. PACKAGE LIVE SENSOR DATA
        live_stats = "N/A"
        if latest_reading:
            weather_info = (
                f"Temp: {weather_record.temperature}°C, Rain: {weather_record.precipitation_probability}%" 
                if weather_record else "No weather data"
            )
            live_stats = (
                f"Moisture: {latest_reading.soil_moisture * 100}%, "
                f"Air Temp: {latest_reading.temperature}°C, "
                f"Humidity: {latest_reading.humidity}%. "
                f"Forecast: {weather_info}"
            )

        # 6. GET AI RESPONSE via Groq
        system_instruction = (
            "You are AquaBot, an expert AI agronomist for Punjab farmers. "
            f"Farm Context: {crop_context}. "
            f"Current Data: {live_stats}. "
            "Tone: Practical, concise, and professional. Provide irrigation advice based on these specific numbers."
        )

        # Using Llama 3.3 70B for high-quality agronomy logic
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_instruction,
                },
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        return {"response": chat_completion.choices[0].message.content}

    except Exception as e:
        print(f"❌ CHATBOT ERROR: {e}")
        raise HTTPException(status_code=500, detail="AquaBot is temporarily unavailable. Check server logs.")