from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.api import deps
from app.db import models

# Setup logging to see the "real" error in your terminal
logger = logging.getLogger("uvicorn.error")
router = APIRouter()

class UserCreate(BaseModel):
    full_name: str
    phone_number: str 
    village_id: int
    role: str = "farmer"
    crop_id: Optional[int] = None
    device_id: Optional[str] = None
    water_source: Optional[str] = "tubewell"
    preferred_language: Optional[str] = "en"
    land_size_value: Optional[float] = 1.0
    land_size_unit: Optional[str] = "acre"

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_farmer(user_in: UserCreate, db: AsyncSession = Depends(deps.get_db)):
    try:
        # 1. Prevent 'UniqueViolationError' by checking for existing phone
        existing_user = await db.execute(
            select(models.User).where(models.User.phone_number == user_in.phone_number)
        )
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Phone number already registered.")

        # 2. Convert Land Units
        unit_multipliers = {"acre": 1.0, "killa": 1.0, "hectare": 2.471, "kanal": 0.125}
        multiplier = unit_multipliers.get(user_in.land_size_unit.lower().strip(), 1.0)
        final_acres = round(user_in.land_size_value * multiplier, 4)

        # 3. Create User (Database will handle the ID automatically)
        new_user = models.User(
            full_name=user_in.full_name,
            phone_number=user_in.phone_number,
            village_id=user_in.village_id,
            current_crop_id=user_in.crop_id,
            field_size_acres=final_acres,
            water_source=user_in.water_source
        )
        db.add(new_user)
        await db.flush() 

        # 4. Create Device with correct columns
        if user_in.device_id:
            new_device = models.Device(
                device_id=user_in.device_id,
                user_id=new_user.id,
                status="Online",  # Using 'Online' to match your setup script
                is_automated=False
            )
            # Remove any other fields like is_active or crop_id here
            db.add(new_device)
        
        await db.commit()
        return {"status": "success", "user_id": new_user.id}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))