<<<<<<< HEAD
import asyncio
from datetime import datetime, timezone
from app.services.recommendation_engine import engine
from app.models.sensor import SensorPayload
from app.schemas.weather import WeatherData

async def test_recommendation_logic():
    print("\n--- TESTING AQUASENSE AI DECISION ENGINE ---\n")

    # Mock crop stages (Engine expects a dictionary)
    stage_veg = {"name_en": "Vegetative", "multiplier": 1.0}
    stage_flower = {"name_en": "Flowering", "multiplier": 1.2}
    stage_fruit = {"name_en": "Fruiting", "multiplier": 1.1}

    # SCENARIO 1: Dry soil, but heavy rain is coming
    rainy_weather = WeatherData(
        district="Ludhiana",  # <--- ADDED THIS!
        temp_celsius=25.0, humidity_percent=80.0, rainfall_mm=12.0, wind_speed_ms=2.0, 
        forecast_summary_en="Heavy Rain", forecast_summary_hi="भारी बारिश", timestamp=datetime.now()
    )
    dry_sensor = SensorPayload(
        device_id="DEV001", timestamp=datetime.now(timezone.utc),
        soil_moisture=0.15, temperature_celsius=24.0, humidity_percent=75.0, battery_voltage=3.8
    )
    
    print("🌾 Scenario 1: Soil is dry (15%), but 12mm of rain is predicted.")
    res1 = engine.analyze(dry_sensor, rainy_weather, "Loamy", stage_veg)
    print(f"👉 Decision: Should Irrigate? {res1['should_irrigate']}")
    print(f"👉 Reason: {res1['reason_code']}\n")

    # SCENARIO 2: Extremely dry soil (Drought emergency)
    drought_weather = WeatherData(
        district="Bathinda",  # <--- ADDED THIS!
        temp_celsius=32.0, humidity_percent=40.0, rainfall_mm=0.0, wind_speed_ms=1.5, 
        forecast_summary_en="Clear", forecast_summary_hi="साफ", timestamp=datetime.now()
    )
    critical_sensor = SensorPayload(
        device_id="DEV001", timestamp=datetime.now(timezone.utc),
        soil_moisture=0.08, temperature_celsius=32.0, humidity_percent=40.0, battery_voltage=3.8
    )
    
    print("🌾 Scenario 2: Soil is critically dry (8%) and NO rain is predicted.")
    res2 = engine.analyze(critical_sensor, drought_weather, "Sandy", stage_flower)
    print(f"👉 Decision: Should Irrigate? {res2['should_irrigate']}")
    print(f"👉 Reason: {res2['reason_code']}\n")

    # SCENARIO 3: Heatwave (Protecting the crops)
    heatwave_weather = WeatherData(
        district="Amritsar",  # <--- ADDED THIS!
        temp_celsius=42.0, humidity_percent=20.0, rainfall_mm=0.0, wind_speed_ms=3.0, 
        forecast_summary_en="Severe Heat", forecast_summary_hi="भीषण गर्मी", timestamp=datetime.now()
    )
    okay_sensor = SensorPayload(
        device_id="DEV001", timestamp=datetime.now(timezone.utc),
        soil_moisture=0.25, temperature_celsius=41.0, humidity_percent=20.0, battery_voltage=3.8
    )
    
    print("🌾 Scenario 3: Soil moisture is okay (25%), but there is a 42°C heatwave.")
    res3 = engine.analyze(okay_sensor, heatwave_weather, "Clay", stage_fruit)
    print(f"👉 Decision: Should Irrigate? {res3['should_irrigate']}")
    print(f"👉 Reason: {res3['reason_code']}\n")

if __name__ == "__main__":
=======
import asyncio
from datetime import datetime, timezone
from app.services.recommendation_engine import engine
from app.models.sensor import SensorPayload
from app.schemas.weather import WeatherData

async def test_recommendation_logic():
    print("\n--- TESTING AQUASENSE AI DECISION ENGINE ---\n")

    # Mock crop stages (Engine expects a dictionary)
    stage_veg = {"name_en": "Vegetative", "multiplier": 1.0}
    stage_flower = {"name_en": "Flowering", "multiplier": 1.2}
    stage_fruit = {"name_en": "Fruiting", "multiplier": 1.1}

    # SCENARIO 1: Dry soil, but heavy rain is coming
    rainy_weather = WeatherData(
        district="Ludhiana",  # <--- ADDED THIS!
        temp_celsius=25.0, humidity_percent=80.0, rainfall_mm=12.0, wind_speed_ms=2.0, 
        forecast_summary_en="Heavy Rain", forecast_summary_hi="भारी बारिश", timestamp=datetime.now()
    )
    dry_sensor = SensorPayload(
        device_id="DEV001", timestamp=datetime.now(timezone.utc),
        soil_moisture=0.15, temperature_celsius=24.0, humidity_percent=75.0, battery_voltage=3.8
    )
    
    print("🌾 Scenario 1: Soil is dry (15%), but 12mm of rain is predicted.")
    res1 = engine.analyze(dry_sensor, rainy_weather, "Loamy", stage_veg)
    print(f"👉 Decision: Should Irrigate? {res1['should_irrigate']}")
    print(f"👉 Reason: {res1['reason_code']}\n")

    # SCENARIO 2: Extremely dry soil (Drought emergency)
    drought_weather = WeatherData(
        district="Bathinda",  # <--- ADDED THIS!
        temp_celsius=32.0, humidity_percent=40.0, rainfall_mm=0.0, wind_speed_ms=1.5, 
        forecast_summary_en="Clear", forecast_summary_hi="साफ", timestamp=datetime.now()
    )
    critical_sensor = SensorPayload(
        device_id="DEV001", timestamp=datetime.now(timezone.utc),
        soil_moisture=0.08, temperature_celsius=32.0, humidity_percent=40.0, battery_voltage=3.8
    )
    
    print("🌾 Scenario 2: Soil is critically dry (8%) and NO rain is predicted.")
    res2 = engine.analyze(critical_sensor, drought_weather, "Sandy", stage_flower)
    print(f"👉 Decision: Should Irrigate? {res2['should_irrigate']}")
    print(f"👉 Reason: {res2['reason_code']}\n")

    # SCENARIO 3: Heatwave (Protecting the crops)
    heatwave_weather = WeatherData(
        district="Amritsar",  # <--- ADDED THIS!
        temp_celsius=42.0, humidity_percent=20.0, rainfall_mm=0.0, wind_speed_ms=3.0, 
        forecast_summary_en="Severe Heat", forecast_summary_hi="भीषण गर्मी", timestamp=datetime.now()
    )
    okay_sensor = SensorPayload(
        device_id="DEV001", timestamp=datetime.now(timezone.utc),
        soil_moisture=0.25, temperature_celsius=41.0, humidity_percent=20.0, battery_voltage=3.8
    )
    
    print("🌾 Scenario 3: Soil moisture is okay (25%), but there is a 42°C heatwave.")
    res3 = engine.analyze(okay_sensor, heatwave_weather, "Clay", stage_fruit)
    print(f"👉 Decision: Should Irrigate? {res3['should_irrigate']}")
    print(f"👉 Reason: {res3['reason_code']}\n")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(test_recommendation_logic())