import asyncio
from app.adapters.weather.open_meteo import weather_service

async def test_live_weather_adapter():
    print("--- TESTING OPEN-METEO ADAPTER (DIRECT API) ---")
    
    # Testing a few specific districts in Punjab
    test_districts = ["Ludhiana", "Amritsar", "Bathinda", "InvalidCity"]
    
    for district in test_districts:
        print(f"\nFetching weather for: {district}...")
        try:
            # This calls your OpenMeteoProvider directly
            result = await weather_service.get_district_weather(district)
            
            print(f"🌡️  Temperature: {result.temp_celsius}°C")
            print(f"💧  Humidity: {result.humidity_percent}%")
            print(f"🌧️  Rainfall: {result.rainfall_mm} mm")
            print(f"💨  Wind Speed: {result.wind_speed_ms} m/s")
            print(f"📝  Summary: {result.forecast_summary_en}")
            
        except Exception as e:
            print(f"❌ Error testing {district}: {e}")

if __name__ == "__main__":
    # Run the async test function
    asyncio.run(test_live_weather_adapter())