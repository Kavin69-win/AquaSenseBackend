from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field, field_validator
from typing import Optional

# Punjab's Agricultural Seasons (Month-based)
# Rice: Kharif season (May to August)
# Wheat: Rabi season (October to February)
CROP_SEASONS = {
    "Rice": [2,5, 6, 7, 8],      
    "Wheat": [10, 11, 12, 1, 2],  
    "Maize": [2, 3, 6, 7],
    "Strawberry": [9, 10, 11, 2] # Example window for Punjab
}

class SensorPayload(BaseModel):
    """
    Standardized Telemetry Schema for AquaSense IoT Nodes.
    """
    device_id: str = Field(..., example="device_001")
    timestamp: datetime = Field(..., description="ISO 8601 formatted timestamp (UTC)")
    soil_moisture: float = Field(..., ge=0.0, le=1.0)
    temperature_celsius: float = Field(..., ge=-10.0, le=60.0)
    humidity_percent: float = Field(..., ge=0.0, le=100.0)
    battery_voltage: float = Field(..., ge=0.0, le=5.0)

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v: datetime):
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            v = v.astimezone(timezone.utc)
        now = datetime.now(timezone.utc)
        if v > now + timedelta(minutes=10):
            raise ValueError(f"Sensor timestamp {v} is too far in the future.")
        if v < now - timedelta(hours=24):
             raise ValueError("Sensor data is older than 24 hours.")
        return v

class CropSelection(BaseModel):
    """
    Schema for linking a specific crop type to a device.
    Rejects 'garbage' dates that don't match Punjab's crop seasons.
    """
    device_id: str = Field(..., example="ESP32_PUNJAB_01")
    crop_name: str = Field(..., example="Rice")
    sowing_date: datetime = Field(..., description="Date when the crop was planted")

    @field_validator("sowing_date")
    @classmethod
    def validate_sowing_season(cls, v: datetime, info):
        # 1. Ensure timezone awareness
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        
        # 2. Get the crop_type from the input data
        crop_name = info.data.get('crop_type', '').capitalize()
        sowing_month = v.month

        # 3. Seasonal Check Logic
        if crop_name in CROP_SEASONS:
            allowed_months = CROP_SEASONS[crop_name]
            if sowing_month not in allowed_months:
                # This treats the date as a "garbage value" by rejecting it
                raise ValueError(
                    f"Faulty Date: {crop_name} is not typically sown in month {sowing_month}. "
                    f"This entry is considered garbage data for the Punjab region."
                )
        return v