from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

from app.api import deps
from app.db import models
from app.services import weather 

router = APIRouter()

# --- Bilingual Content Dictionary ---
TRANSLATIONS = {
    "en": {
        "decision_on": "START_PUMP",
        "decision_off": "KEEP_OFF",
        "decision_rain": "WAIT_FOR_RAIN",
        "action_on": "Turn on your {source} pump.",
        "action_auto": "Auto-Mode: Started your {source} pump.",
        "action_off": "Keep pump OFF.",
        "action_rain": "Keep pump OFF. Rain is expected soon.",
        "duration": "Run the pump for {minutes}.",
        "reason": "Your {crop} in {village} needs {threshold}% moisture. Current level is {current}%.",
        "weather_reason": "Moisture is low, but there is a {prob}% chance of rain in {village}.",
        "prompt": "Moisture is critically low. Do you want to turn on the pump for {minutes}?" 
    },
    "hi": {
        "decision_on": "पंप चालू करें",
        "decision_off": "पंप बंद रखें",
        "decision_rain": "बारिश का इंतज़ार करें",
        "action_on": "अपना {source} पंप चालू करें।",
        "action_auto": "ऑटो-मोड: आपका {source} पंप चालू कर दिया गया है।",
        "action_off": "पंप बंद रखें।",
        "action_rain": "पंप बंद रखें। जल्द ही बारिश होने की संभावना है।",
        "duration": "पंप को {minutes} के लिए चलाएं।",
        "reason": "{village} में आपकी {crop} की फसल को {threshold}% नमी की आवश्यकता है। वर्तमान स्तर {current}% है।",
        "weather_reason": "नमी कम है, लेकिन {village} में {prob}% बारिश होने की संभावना है।",
        "prompt": "नमी बहुत कम है। क्या आप {minutes} के लिए पंप चालू करना चाहते हैं?" 
    }
}

SOURCE_MAP = {
    "hi": {"tubewell": "ट्यूबवेल", "tank": "टैंक", "canal": "नहर", "tap": "नल"},
    "en": {"tubewell": "tubewell", "tank": "tank", "canal": "canal", "tap": "tap"}
}

@router.get("/daily")
async def get_irrigation_recommendation(
    x_user_id: Optional[int] = Header(None), 
    db: AsyncSession = Depends(deps.get_db)
):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="User ID header (X-User-ID) is missing.")

    # 1. Fetch Farmer
    stmt = select(models.User).where(models.User.id == x_user_id).options(selectinload(models.User.village))
    user = (await db.execute(stmt)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Farmer not registered.")

    lang = user.preferred_language if user.preferred_language in ["en", "hi"] else "en"
    t = TRANSLATIONS[lang]

    # 2. Get Device and Settings
    device = (await db.execute(select(models.Device).where(models.Device.user_id == user.id))).scalars().first()
    if not device:
        raise HTTPException(status_code=404, detail="No IoT device linked.")

    # 3. Get Latest Reading
    reading_stmt = select(models.SensorReading).where(models.SensorReading.device_id == device.device_id).order_by(models.SensorReading.timestamp.desc()).limit(1)
    latest_reading = (await db.execute(reading_stmt)).scalars().first()

    if not latest_reading:
        return {"farmer": user.full_name, "status": "WAITING_FOR_DATA"}

    # 4. Fetch Crop Threshold
    crop = None
    if user.current_crop_id:
        crop = (await db.execute(select(models.Crop).where(models.Crop.id == user.current_crop_id))).scalars().first()
    
    threshold = crop.moisture_threshold if (crop and crop.moisture_threshold) else 0.25

    # 5. Check Weather
    will_rain, rain_prob = weather.get_rain_forecast(user.village.name)

    # 6. Decision Engine
    moisture_pct = latest_reading.soil_moisture * 100
    needs_water = latest_reading.soil_moisture < threshold
    
    duration_text = f"0 { 'minutes' if lang == 'en' else 'मिनट' }"
    source_translated = SOURCE_MAP[lang].get(user.water_source.lower() if user.water_source else "tubewell", "tubewell")
    crop_display = crop.name if crop else ("Crop" if lang == 'en' else "फसल")
    
    requires_user_confirmation = False
    prompt_message = None

    if needs_water:
        if will_rain:
            decision = t["decision_rain"]
            action = t["action_rain"]
            reasoning = t["weather_reason"].format(village=user.village.name, prob=int(rain_prob*100))
        else:
            decision = t["decision_on"]
            
            # Runtime Calculation
            A = user.field_size_acres or 1.0
            Q = {"tubewell": 1500, "canal": 1000, "tank": 500, "tap": 50}.get(user.water_source.lower() if user.water_source else "tubewell", 500)
            T_calculated = (A * (threshold - latest_reading.soil_moisture) * 400000) / Q
            T_final = int(min(T_calculated, 240))
            duration_text = f"{T_final} { 'minutes' if lang == 'en' else 'मिनट' }"
            
            reasoning = t["reason"].format(crop=crop_display, village=user.village.name, threshold=int(threshold*100), current=f"{moisture_pct:.1f}")
            
            if device.is_automated:
                requires_user_confirmation = False 
                action = t["action_auto"].format(source=source_translated)
            else:
                requires_user_confirmation = True 
                action = t["action_on"].format(source=source_translated)
                prompt_message = t["prompt"].format(minutes=duration_text)
    else:
        decision = t["decision_off"]
        action = t["action_off"]
        reasoning = t["reason"].format(crop=crop_display, village=user.village.name, threshold=int(threshold*100), current=f"{moisture_pct:.1f}")

    return {
        "farmer": user.full_name,
        "village": user.village.name,
        "is_automated_mode": device.is_automated,
        "recommendation": {
            "decision": decision,
            "action": action,
            "duration": duration_text,
            "reasoning": reasoning,
            "requires_user_confirmation": requires_user_confirmation,
            "confirmation_prompt": prompt_message
        }
    }