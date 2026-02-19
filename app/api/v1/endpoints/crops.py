from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.api import deps
from app.db import models

router = APIRouter()

@router.get("")
async def list_crops(
    category: Optional[str] = Query(None, description="Filter by category (e.g., Cereal, Fruit)"),
    season: Optional[str] = Query(None, description="Filter by season (e.g., Rabi, Kharif)"),
    db: AsyncSession = Depends(deps.get_db)
):
    # Base query
    stmt = select(models.Crop)
    
    # Dynamic Filtering
    if category:
        stmt = stmt.where(models.Crop.category == category)
    if season:
        # Using 'ilike' for case-insensitive matching
        stmt = stmt.where(models.Crop.season.ilike(f"%{season}%"))
        
    result = await db.execute(stmt)
    crops = result.scalars().all()
    
    return {
        "total": len(crops),
        "crops": [
            {
                "id": c.id,
                "name": c.name,
                "category": c.category,
                "season": c.season,
                "preferred_soils": c.soil_types.split("|")
            } for c in crops
        ]
    }