from datetime import datetime, timezone, timedelta, date
from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Punjab's Agricultural Seasons mapping
CROP_SEASONS = {
    "Wheat": [10, 11, 12, 1, 2, 3],
    "Paddy (Rice)": [5, 6, 7, 8],
    "Basmati rice": [6, 7, 8],
    "Maize (grain)": [6, 7, 8],
    "Barley": [10, 11, 12, 1],
    "Fodder maize": [3, 4, 5, 6, 7, 8],
    "Sorghum (Jowar) fodder": [5, 6, 7, 8],
    "Bajra (Pearl millet)": [6, 7, 8],
    "Oat fodder": [10, 11, 12],
    "Gram (Chickpea)": [10, 11],
    "Masur (Lentil)": [10, 11, 12],
    "Field pea (for grain)": [10, 11],
    "Moong (Green gram)": [3, 4, 5, 6, 7, 8],
    "Mash (Black gram)": [6, 7, 8],
    "Mustard": [10, 11],
    "Rapeseed": [10, 11],
    "Sunflower": [1, 2, 3, 8, 9, 10],
    "Groundnut (limited pockets)": [6, 7],
    "Linseed (minor)": [10, 11],
    "Cotton (American)": [4, 5],
    "Desi cotton (arboreum)": [4, 5],
    "Sugarcane": [2, 3, 4],
    "Sugar beet": [10, 11],
    "Fodder berseem": [9, 10, 11],
    "Potato": [9, 10, 1, 2],
    "Onion": [10, 11, 12, 5, 6],
    "Cauliflower": [8, 9, 10, 11],
    "Cabbage": [9, 10, 11],
    "Tomato": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Okra (Ladyfinger)": [2, 3, 6, 7],
    "Brinjal (Eggplant)": [2, 3, 6, 7, 10, 11],
    "Carrot": [8, 9, 10, 11],
    "Radish": [8, 9, 10, 11, 12],
    "Peas": [10, 11],
    "Capsicum (Shimla mirch)": [11, 12, 1, 2],
    "Chillies": [2, 3, 6, 7],
    "Turmeric": [4, 5],
    "Ginger": [4, 5],
    "Kinnow mandarin": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Guava": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Mango": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Banana": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "Strawberry": [9, 10, 11, 2] 
}

class CropSelection(BaseModel):
    """
    Schema for linking a crop to a device with seasonal validation.
    """
    device_id: str = Field(..., example="device_001")
    # CHANGED: Use 'crop_name' to match your JSON input and avoid 422 errors
    crop_name: str = Field(..., example="Paddy (Rice)") 
    sowing_date: date = Field(..., description="Date when the crop was planted")

    @field_validator("sowing_date")
    @classmethod
    def validate_sowing_season(cls, v: date, info):
        # 1. Ensure we have the crop_name from the input
        crop_name = info.data.get('crop_name', '')
        sowing_month = v.month

        # 2. Check against Punjab's Agronomic Dataset
        if crop_name in CROP_SEASONS:
            allowed_months = CROP_SEASONS[crop_name]
            if sowing_month not in allowed_months:
                raise ValueError(
                    f"Agronomic Error: {crop_name} is not typically sown in month {sowing_month}. "
                    "This entry is considered faulty for the Punjab region."
                )
        return v