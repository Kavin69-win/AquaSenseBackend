import logging
from app.models.sensor import SensorPayload
from app.schemas.weather import WeatherData

logger = logging.getLogger("aquasense.ai.v280")

class RecommendationEngine:
    """
    Level 280 Smart Irrigation Intelligence.
    Integrates Soil Hydraulics, Crop Physiology, and Atmospheric Demand.
    """
    def __init__(self):
        # Soil Hydraulics Matrix: Permanent Wilting Point (PWP) and Field Capacity (FC)
        # Infiltration rate in mm/hr for Punjab-specific soil textures
        self.SOIL_PHYSICS = {
            "Sandy": {"pwp": 0.12, "fc": 0.22, "infil_rate": 30.0},
            "Sandy loam": {"pwp": 0.15, "fc": 0.26, "infil_rate": 20.0},
            "Loamy sand": {"pwp": 0.14, "fc": 0.24, "infil_rate": 25.0},
            "Kandi hill soil": {"pwp": 0.13, "fc": 0.23, "infil_rate": 35.0},
            "Alluvial": {"pwp": 0.18, "fc": 0.32, "infil_rate": 12.0},
            "Loamy": {"pwp": 0.18, "fc": 0.32, "infil_rate": 10.0},
            "Clay loam": {"pwp": 0.22, "fc": 0.38, "infil_rate": 5.0}
        }
        self.ROOT_ZONE_DEPTH = 300  # mm (Average root depth for Wheat/Paddy)
        self.RAIN_INHIBIT_THRESHOLD = 4.0  # mm

    def _get_physics(self, soil_type: str):
        # Match primary soil type from the delimited string
        primary = soil_type.split('|')[0].strip() if soil_type else "Loamy"
        return self.SOIL_PHYSICS.get(primary, self.SOIL_PHYSICS["Loamy"])

    def calculate_runtime(self, soil_type: str, current_vwc: float, target_vwc: float) -> int:
        """
        Calculates required pump time in minutes to restore root zone moisture.
        Ensures application does not exceed infiltration rate to prevent runoff.
        """
        physics = self._get_physics(soil_type)
        deficit = max(0, target_vwc - current_vwc)
        water_needed_mm = deficit * self.ROOT_ZONE_DEPTH
        
        # Runtime calculation (mm needed / infiltration capacity per hour)
        runtime_minutes = (water_needed_mm / physics["infil_rate"]) * 60
        return min(int(runtime_minutes), 240) # Safety cap at 4 hours

    def analyze(self, sensor_data: SensorPayload, weather_data: WeatherData, 
                soil_type: str, crop_stage: dict) -> dict:
        """
        Multi-factor hybrid logic: Sensor + Forecast + Biology.
        """
        physics = self._get_physics(soil_type)
        current_vwc = sensor_data.soil_moisture
        
        # 1. Delta-Check (Sensor Anomaly Handling)
        # In production, this would compare against historical readings in Redis
        if sensor_data.battery_voltage < 3.3:
            logger.warning(f"Low battery voltage ({sensor_data.battery_voltage}V) on device.")

        # 2. Calculate Physiological Trigger Point (PTP)
        # We tighten the MAD (Management Allowed Depletion) during peak demand stages
        base_mad = 0.5 
        adjusted_mad = base_mad / crop_stage.get("multiplier", 1.0)
        ptp = physics["pwp"] + (adjusted_mad * (physics["fc"] - physics["pwp"]))

        logger.info(f"Analysis | Soil: {soil_type} | Stage: {crop_stage['name_en']} | VWC: {current_vwc:.2f} | PTP: {ptp:.2f}")

        # --- Decision Branch 1: Weather Weighting (Pre-emptive Inhibition) ---
        if weather_data.rainfall_mm >= self.RAIN_INHIBIT_THRESHOLD:
            return {"should_irrigate": False, "reason_code": "RAIN_FORECAST", "confidence": 0.98}

        # --- Decision Branch 2: Critical Depletion ---
        if current_vwc <= ptp:
            runtime = self.calculate_runtime(soil_type, current_vwc, physics["fc"])
            return {
                "should_irrigate": True, 
                "reason_code": "CRITICAL_MOISTURE", 
                "confidence": 0.95,
                "runtime_minutes": runtime
            }

        # --- Decision Branch 3: Vapor Pressure Deficit / Heat Stress ---
        if weather_data.temp_celsius > 35.0 and current_vwc < (ptp + 0.05):
            return {
                "should_irrigate": True, 
                "reason_code": "HEAT_STRESS", 
                "confidence": 0.88,
                "runtime_minutes": 30 # Short cooling pulse
            }

        return {"should_irrigate": False, "reason_code": "WAIT_AND_WATCH", "confidence": 0.82}

engine = RecommendationEngine()