from datetime import date
from app.db import models 

def calculate_universal_duration(user: models.User, crop: models.Crop):
    # 1. Flow rates based on your frontend buttons
    source_flow = {
        "tubewell": 15.0,
        "canal": 10.0,
        "tap": 5.0,
        "tank": 3.0
    }

    # 2. Soil adjustment factors (Calibrated for Punjab Region)
    soil_multipliers = {
        # --- Punjab Specific Soils ---
        "loamy": 1.0,           # Standard alluvial (Central Punjab) - Baseline
        "silt_loam": 1.0,       # Very fertile, similar water needs to loamy
        "sandy_loam": 1.15,     # Common across Punjab, drains slightly faster
        "clay_loam": 0.9,       # Holds water well, needs slightly less runtime
        "sandy": 1.4,           # South-West Punjab (Bathinda/Mansa), drains very fast
        "clay": 0.8,            # Heavy soil (Gurdaspur/Hoshiarpur), holds water tightly
        "kandi": 1.5,           # Gravelly sub-mountainous soil, very poor water retention
        "saline": 1.2,          # Kallar/salt-affected soil, needs extra water for leaching salts
        
        # --- General/Other regions (Fallback) ---
        "red": 1.3,        
        "laterite": 1.5   
    }
    # 3. Extract user data safely
    acres = user.field_size_acres or 1.0
    soil = (getattr(user, "soil_type", "loamy") or "loamy").lower().strip()
    source = (user.water_source or "tubewell").lower().strip()
    
    # 4. NEW: Growth Multiplier Logic
    # Uses the renamed sowing_date field
    sowing_date = getattr(user, "sowing_date", None)
    growth_multiplier = 1.0
    
    if sowing_date:
        days_since_sowing = (date.today() - sowing_date).days
        
        if days_since_sowing < 15:
            growth_multiplier = 0.6  # Sowing stage: Less water
        elif days_since_sowing > 100:
            growth_multiplier = 0.4  # Near harvest: Minimum water
        else:
            growth_multiplier = 1.0  # Peak growth: Standard water

    # 5. Get factors from database/dictionaries
    base_need = getattr(crop, "base_water_need", 0.5)
    soil_adj = soil_multipliers.get(soil, 1.0)
    flow_rate = source_flow.get(source, 8.0)

    # FINAL CALCULATION
    # Added growth_multiplier to the formula to adjust minutes based on age
    duration_minutes = (acres * (base_need * soil_adj * growth_multiplier) * 100) / flow_rate
    
    return round(duration_minutes, 2)