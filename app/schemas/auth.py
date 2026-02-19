from pydantic import BaseModel, Field, field_validator
from typing import Optional

class UserCreate(BaseModel):
    """
    Comprehensive payload for registering a new farmer.
    Required fields are kept to a minimum to ensure a smooth UX.
    """
    # Identification
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="Full name of the farmer"
    )
    phone_number: str = Field(
        ..., 
        description="Mobile number used for SMS alerts and login"
    )

    # Location
    village: str = Field(
        ..., 
        description="Village name used to link soil and weather data"
    )
    district: str = Field(
        "Hoshiarpur", 
        description="District name (defaults to Hoshiarpur)"
    )

    # System Role
    role: str = Field(
        "farmer", 
        description="User role: 'farmer' or 'admin'"
    )

    # --- OPTIONAL FIELDS (The "Pro" Data) ---
    # These are Optional so the API doesn't throw a 422 error if they are missing
    village_id: Optional[int] = Field(None, description="Database ID for the village")
    crop_id: Optional[int] = Field(None, description="ID of the currently sown crop")
    device_id: Optional[str] = Field(None, description="Hardware ID of the ESP32 unit")
    land_size_value: Optional[float] = Field(1.0, description="Size of the land holding")
    land_size_unit: Optional[str] = Field("acres", description="Unit of measurement (acres/kanals)")
    water_source: Optional[str] = Field("tubewell", description="Primary source of irrigation")

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v.lower() not in ('farmer', 'admin'):
            raise ValueError("Role must be 'farmer' or 'admin'")
        return v.lower()

class UserResponse(BaseModel):
    """
    The response sent back to the mobile app after successful registration.
    """
    id: int = Field(..., description="Unique ID assigned by the database")
    msg: str = Field(..., description="Localized welcome message")

    class Config:
        # This allows Pydantic to read data directly from the SQLAlchemy 'User' object
        from_attributes = True 
        json_schema_extra = {
            "example": {
                "id": 1,
                "msg": "Welcome to AquaSense! Your registration is complete."
            }
        }