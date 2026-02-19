from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from app.api import deps
from app.db import models
from app.schemas.sensor import CropSelection 
from app.services.irrigation import calculate_universal_duration
# Import your new logic engine
from app.services import logic_engine 

router = APIRouter()

# ==========================================
# 1. Pydantic Schemas
# ==========================================

class SensorData(BaseModel):
    device_id: str = Field(..., example="AS-BC:DD:C2:11")
    moisture: float = Field(..., description="Soil moisture level (0.0 to 1.0)")
    temperature: Optional[float] = Field(None, example=28.5)
    humidity: Optional[float] = Field(None, example=65.0)

class PumpCommand(BaseModel):
    device_id: str = Field(..., example="device_001")
    command: str = Field(..., description="Must be exactly 'ON' or 'OFF'")
    duration_minutes: int = Field(0)

class HardwareRegistration(BaseModel):
    device_id: str
    user_id: int

class SoilUpdate(BaseModel):
    device_id: str
    soil_type: str # e.g., "Sandy", "Clay", "Loamy"

# ==========================================
# 2. API Routes
# ==========================================

@router.post("/record", status_code=status.HTTP_201_CREATED)
async def record_sensor_data(data: SensorData, db: AsyncSession = Depends(deps.get_db)):
    """
    Ingests data and RUNS LIVE AI LOGIC to update the threshold 
    based on the latest database state.
    """
    # 1. Verify Device
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == data.device_id))
    device = device_stmt.scalars().first()
    
    if not device:
        raise HTTPException(status_code=403, detail="Hardware not registered.")

    # 2. Get the User and their specific settings from DB
    user_stmt = await db.execute(select(models.User).where(models.User.id == device.user_id))
    user = user_stmt.scalars().first()

    # 3. LIVE AI CALCULATION
    # Every time the ESP32 pings, we check the DB for the current crop/soil and ask the AI
    current_threshold = 0.25 # Default fallback
    
    if user:
        # Fetch Crop Name for the AI
        crop_name = "General Crop"
        if user.current_crop_id:
            crop_stmt = await db.execute(select(models.Crop).where(models.Crop.id == user.current_crop_id))
            crop = crop_stmt.scalars().first()
            crop_name = crop.name if crop else "General Crop"

        # Calculate Age from Database Sowing Date
        from datetime import date
        days_old = (date.today() - user.sowing_date).days if user.sowing_date else 30

        # RUN THE INTERNAL AI (Logic Engine)
        # This takes the info DIRECTLY from the database you just updated via frontend
        ai_data = await logic_engine.calculate_soil_threshold(
            crop_name=crop_name,
            soil_type=user.soil_type or "Loamy",
            growth_stage=f"{days_old} days old"
        )
        current_threshold = ai_data.get("threshold", 0.25)
        
        # Sync the database with this new calculated threshold
        user.dynamic_threshold = current_threshold

    # 4. Save the actual sensor reading
    new_reading = models.SensorReading(
        device_id=data.device_id,
        user_id=device.user_id,
        soil_moisture=data.moisture,
        temperature=data.temperature,
        humidity=data.humidity,
        timestamp=datetime.now()
    )
    db.add(new_reading)
    await db.commit()
    
    # 5. Send the AI-calculated threshold back to ESP32
    return {
        "status": "success", 
        "threshold": current_threshold, 
        "device_mode": "AUTOMATED" if device.is_automated else "MANUAL"
    }

@router.put("/update-soil-ai")
async def update_soil_and_recalculate_threshold(req: SoilUpdate, db: AsyncSession = Depends(deps.get_db)):
    """
    AI INTEGRATION STEP: 
    Takes frontend soil choice, runs Logic AI, and updates the database.
    """
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == req.device_id))
    device = device_stmt.scalars().first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    user_stmt = await db.execute(select(models.User).where(models.User.id == device.user_id))
    user = user_stmt.scalars().first()

    crop_name = "General Crop"
    if user.current_crop_id:
        crop_stmt = await db.execute(select(models.Crop).where(models.Crop.id == user.current_crop_id))
        crop = crop_stmt.scalars().first()
        crop_name = crop.name

    # CALL THE INTERNAL AI ENGINE
    ai_data = await logic_engine.calculate_soil_threshold(
        crop_name=crop_name,
        soil_type=req.soil_type,
        growth_stage="Vegetative" # Simplified for demo
    )

    # Update User Table with AI Results
    user.soil_type = req.soil_type
    user.dynamic_threshold = ai_data.get("threshold", 0.25)
    
    await db.commit()
    
    return {
        "status": "success", 
        "new_threshold": user.dynamic_threshold,
        "ai_reasoning": ai_data.get("reason", "Optimized for soil type.")
    }

# --- Rest of your routes (pump-control, register-hardware, etc.) remain unchanged ---
# [Ensure the rest of your provided routes are pasted here]