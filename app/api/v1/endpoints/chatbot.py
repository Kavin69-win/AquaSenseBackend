from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.models import SensorReading, Device, Crop, WeatherCache, User
from app.api.deps import get_db 
from app.services.chatbot import ask_aquabot

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
        
        # 2. FETCH DEVICE & OWNER (USER) DATA
        # We need the User to get the sowing_date and current_crop_id
        device_query = select(Device).where(Device.device_id == request.device_id)
        device_result = await db.execute(device_query)
        device_record = device_result.scalars().first()
        
        if not device_record:
            raise HTTPException(status_code=404, detail="Device not found")

        # Get User details
        user_query = select(User).where(User.id == device_record.user_id)
        user_result = await db.execute(user_query)
        user_record = user_result.scalars().first()

        # 3. CONSTRUCT CROP CONTEXT
        crop_context = None
        if user_record and user_record.current_crop_id:
            crop_query = select(Crop).where(Crop.id == user_record.current_crop_id)
            crop_result = await db.execute(crop_query)
            crop_record = crop_result.scalars().first()
            
            if crop_record:
                crop_context = {
                    "crop_name": crop_record.name,
                    "sowing_date": user_record.sowing_date  # Critical for age calculation
                }

        # 4. FETCH LATEST WEATHER CACHE
        weather_query = select(WeatherCache).order_by(desc(WeatherCache.updated_at))
        weather_result = await db.execute(weather_query)
        weather_record = weather_result.scalars().first()

        # 5. PACKAGE LIVE SENSOR DATA
        live_data = None
        if latest_reading:
            live_data = {
                "soil_moisture": latest_reading.soil_moisture,
                "temperature_celsius": latest_reading.temperature,
                "humidity_percent": latest_reading.humidity,
                "weather": {
                    "temp": weather_record.temperature if weather_record else "N/A",
                    "rain_chance": weather_record.precipitation_probability if weather_record else 0
                }
            }

        # 6. GET AI RESPONSE (Passing both live_data and crop_context)
        bot_reply = ask_aquabot(
            message=request.message, 
            device_id=request.device_id, 
            live_data=live_data,
            crop_context=crop_context
        )
        
        return {"response": bot_reply}

    except Exception as e:
        print(f"❌ CHATBOT ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))