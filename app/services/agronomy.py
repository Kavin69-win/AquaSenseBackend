# app/services/agronomy.py

def get_irrigation_decision(soil_type: str, current_moisture: float, rain_prob: float):
    """
    Determines if the pump should be ON or OFF based on soil type and weather.
    """
    
    # 1. Define Thresholds based on Soil Type
    # Sandy soils drain fast -> lower threshold (15%)
    # Clay soils hold water -> higher threshold (30%)
    thresholds = {
        "Sandy Loam": 0.15,  # 15%
        "Clay": 0.30,        # 30%
        "Silt": 0.20,        # 20%
        "Loam": 0.25         # 25% (Default)
    }
    
    # Get threshold for user's soil (default to 0.25 if unknown)
    limit = thresholds.get(soil_type, 0.25)

    # 2. The Decision Logic
    decision = "STAY_OFF"
    reasoning = "Moisture levels are sufficient."

    # Rule 1: Don't water if it's going to rain (Save Water!)
    if rain_prob > 70:
        decision = "STAY_OFF"
        reasoning = f"Rain probability is high ({rain_prob}%). Irrigation paused."
    
    # Rule 2: Water if moisture is below the limit
    elif current_moisture < limit:
        decision = "START_PUMP"
        reasoning = f"Soil moisture ({current_moisture*100:.1f}%) is below the {limit*100:.0f}% threshold for {soil_type}."
    
    else:
        decision = "STAY_OFF"
        reasoning = f"Current moisture ({current_moisture*100:.1f}%) is sufficient for healthy crop growth."

    return {
        "decision": decision,
        "reasoning": reasoning,
        "threshold": limit
    }