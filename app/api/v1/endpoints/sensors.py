from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List

from app.api import deps
from app.db import models
from app.schemas.sensor import CropSelection 
from app.services.irrigation import calculate_universal_duration
# Points to your Groq-powered logic engine
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
    soil_type: str 

class CropSelectionUpdate(BaseModel):
    device_id: str
    crop_name: str 
    sowing_date: Optional[date] = None

# ==========================================
# 2. API Routes
# ==========================================

@router.post("/register-hardware")
async def register_hardware(req: HardwareRegistration, db: AsyncSession = Depends(deps.get_db)):
    """Registers a new physical ESP32 to a user account."""
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == req.device_id))
    if device_stmt.scalars().first():
        raise HTTPException(status_code=400, detail="Device already registered.")
    
    new_device = models.Device(device_id=req.device_id, user_id=req.user_id, is_automated=True)
    db.add(new_device)
    await db.commit()
    return {"status": "success", "message": f"Device {req.device_id} registered."}

@router.post("/record", status_code=status.HTTP_201_CREATED)
async def record_sensor_data(data: SensorData, db: AsyncSession = Depends(deps.get_db)):
    """Ingests data from ESP32 and returns the AI-CALCULATED dynamic threshold."""
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == data.device_id))
    device = device_stmt.scalars().first()
    
    #if not device:
       #raise HTTPException(status_code=403, detail="Hardware not registered.")

    current_threshold = 0.25 
    
    user_stmt = await db.execute(select(models.User).where(models.User.id == device.user_id))
    user = user_stmt.scalars().first()

    if user:
        # Uses the dynamic_threshold calculated by the Logic AI
        current_threshold = user.dynamic_threshold

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
    
    return {
        "status": "success", 
        "threshold": current_threshold, 
        "device_mode": "AUTOMATED" if device.is_automated else "MANUAL"
    }

@router.put("/select-crop")
async def select_crop_for_device(req: CropSelection, db: AsyncSession = Depends(deps.get_db)):
    """Farmer selects a crop, AI recalculates the new threshold, and updates DB."""
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == req.device_id))
    device = device_stmt.scalars().first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    user_stmt = await db.execute(select(models.User).where(models.User.id == device.user_id))
    user = user_stmt.scalars().first()

    crop_stmt = await db.execute(select(models.Crop).where(models.Crop.id == req.crop_id))
    crop = crop_stmt.scalars().first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found.")

    # Call the new Groq-based logic
    ai_data = await logic_engine.calculate_soil_threshold(
        crop_name=crop.name,
        soil_type=user.soil_type or "Loamy",
        growth_stage="Sowing Stage"
    )

    user.current_crop_id = req.crop_id
    user.sowing_date = date.today()
    user.dynamic_threshold = ai_data.get("threshold", 0.25)
    await db.commit()

    return {"status": "success", "new_threshold": user.dynamic_threshold}

@router.put("/update-soil-ai")
async def update_soil_and_recalculate_threshold(req: SoilUpdate, db: AsyncSession = Depends(deps.get_db)):
    """Takes frontend soil choice, runs Logic AI, and updates the database."""
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
        crop_name = crop.name if crop else "General Crop"

    ai_data = await logic_engine.calculate_soil_threshold(
        crop_name=crop_name,
        soil_type=req.soil_type,
        growth_stage="Vegetative" 
    )

    user.soil_type = req.soil_type
    user.dynamic_threshold = ai_data.get("threshold", 0.25)
    await db.commit()
    
    return {
        "status": "success", 
        "new_threshold": user.dynamic_threshold,
        "ai_reasoning": ai_data.get("reason", "Optimized for soil type.")
    }

@router.post("/pump-control")
async def manual_pump_control(req: PumpCommand, db: AsyncSession = Depends(deps.get_db)):
    # 1. Get Device and Owner
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == req.device_id))
    device = device_stmt.scalars().first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    user_stmt = await db.execute(select(models.User).where(models.User.id == device.user_id))
    user = user_stmt.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # 2. Get the Crop Object needed for your formula
    crop = None
    if user.current_crop_id:
        crop_stmt = await db.execute(select(models.Crop).where(models.Crop.id == user.current_crop_id))
        crop = crop_stmt.scalars().first()

    # 3. RUN THE FORMULA
    duration = req.duration_minutes
    if duration == 0:
        if crop:
            try:
                # Pass the exact objects your formula expects!
                duration = calculate_universal_duration(user=user, crop=crop)
            except Exception as e:
                print(f"Formula Error: {e}")
                duration = 15 # Fallback if math fails
        else:
            # If farmer hasn't selected a crop yet, default to 15
            duration = 15

    return {
        "status": "success",
        "command": req.command,
        "calculated_duration": duration,
        "details": f"Calculated for crop: {crop.name if crop else 'None'}, soil: {user.soil_type or 'None'}"
    }

@router.put("/toggle-automation/{device_id}")
async def toggle_automation(device_id: str, is_automated: bool, db: AsyncSession = Depends(deps.get_db)):
    """Switch between AI-Driven and Manual modes."""
    device_stmt = await db.execute(select(models.Device).where(models.Device.device_id == device_id))
    device = device_stmt.scalars().first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    device.is_automated = is_automated
    await db.commit()
    return {"device_id": device_id, "is_automated": is_automated}