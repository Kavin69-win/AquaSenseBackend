from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.api import deps
from app.db import models

router = APIRouter()

@router.get("")
async def list_villages(db: AsyncSession = Depends(deps.get_db)):
    """
    Returns a list of all villages currently in the AquaSense database.
    """
    # Fetch villages and join with district info
    stmt = select(models.Village)
    result = await db.execute(stmt)
    villages = result.scalars().all()
    
    return {
        "total": len(villages),
        "villages": [
            {
                "id": v.id,
                "name": v.name,
                "district_id": v.district_id,
                "soil_type": v.soil_type
            } for v in villages
        ]
    }

@router.get("/districts")
async def list_districts(db: AsyncSession = Depends(deps.get_db)):
    """
    Returns a list of all districts (e.g., Hoshiarpur, Bathinda, Mansa).
    """
    stmt = select(models.District)
    result = await db.execute(stmt)
    districts = result.scalars().all()
    
    return {
        "districts": [
            {"id": d.id, "name": d.name} for d in districts
        ]
    }