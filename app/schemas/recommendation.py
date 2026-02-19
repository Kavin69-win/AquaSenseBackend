from pydantic import BaseModel
from typing import Dict, Any

class IrrigationAdvice(BaseModel):
    """
    Final decision object sent to the client.
    Contains both the binary decision and the human-readable explanation.
    """
    # Context
    district: str
    analyzed_at: str  # ISO timestamp
    
    # The Decision (Boolean for UI logic: Red/Green indicator)
    should_irrigate: bool
    
    # The Explanation (Localized string based on headers)
    message: str
    
    # Supporting Data (For "Details" view in App)
    metrics: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "district": "Ludhiana",
                "analyzed_at": "2024-05-20T14:35:00Z",
                "should_irrigate": True,
                "message": "मिट्टी की नमी कम है। सिंचाई की सिफारिश की जाती है।",
                "metrics": {
                    "soil_moisture": 0.12,
                    "rainfall_forecast": 0.0
                }
            }
        }