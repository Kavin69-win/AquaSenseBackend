import requests
import time
from unittest.mock import patch

BASE_URL = "http://127.0.0.1:8000/api/v1"

# --- TOGGLE THIS FOR TESTING ---
FORCE_RAIN = True  # Set to True to test "WAIT_FOR_RAIN", False for "START_PUMP"

def test_complete_system():
    unique_id = int(time.time())
    test_farmer = {
        "full_name": "Kavin Logic-Test",
        "phone_or_email": f"kavin_{unique_id}@test.com",
        "village_id": 1, 
        "crop_id": 1, 
        "device_id": f"DEV_{unique_id}",
        "land_size_value": 2.0, 
        "land_size_unit": "killa", 
        "water_source": "tubewell",
        "preferred_language": "en"
    }

    # 1. Register
    reg = requests.post(f"{BASE_URL}/users/register", json=test_farmer)
    user_id = reg.json().get("user_id")

    # 2. Ingest Dry Soil
    requests.post(f"{BASE_URL}/sensors/ingest", json={
        "device_id": f"DEV_{unique_id}",
        "moisture": 0.10, # Dry soil
        "temperature": 31.0
    })

    # 3. Fetch Recommendation with Mocked Weather
    # This 'patch' line tells the backend to use our fake value instead of calling the API
    with patch("app.services.weather.get_rain_forecast", return_value=(FORCE_RAIN, 0.85 if FORCE_RAIN else 0.10)):
        headers = {"X-User-ID": str(user_id)}
        response = requests.get(f"{BASE_URL}/recommendations/daily", headers=headers)
        data = response.json()

        print(f"\n--- Testing with FORCE_RAIN = {FORCE_RAIN} ---")
        print(f"Decision: {data['recommendation']['decision']}")
        print(f"Action: {data['recommendation']['action']}")
        print(f"Reasoning: {data['recommendation']['reasoning']}")

if __name__ == "__main__":
    test_complete_system()