import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
DEVICE_ID = "device_001" # Ensure this is in your DB

def test_irrigation_flow():
    print(f"🚀 Starting Irrigation Logic Verification for {DEVICE_ID}...")

    # 1. Get the Recommendation (The Formula)
    # This calls the logic that uses sowing_date, soil, and crop age
    rec_response = requests.get(f"{BASE_URL}/recommendations/daily?device_id={DEVICE_ID}")
    
    if rec_response.status_code != 200:
        print(f"❌ Failed to get recommendation: {rec_response.text}")
        return

    data = rec_response.json()
    smart_minutes = data.get("minutes")
    crop = data.get("crop")
    
    print(f"📈 Formula Result for {crop}: {smart_minutes} minutes.")

    # 2. Send the Pump Command using that Formula result
    pump_payload = {
        "device_id": DEVICE_ID,
        "command": "ON",
        "duration_minutes": int(smart_minutes) # Formula output goes here
    }
    
    pump_response = requests.post(f"{BASE_URL}/sensors/pump-control", json=pump_payload)
    
    if pump_response.status_code == 200:
        print(f"✅ SUCCESS: Pump command sent for {smart_minutes} mins.")
        print(f"Response: {pump_response.json()['message']}")
    else:
        print(f"❌ Pump Control Failed: {pump_response.text}")

if __name__ == "__main__":
    test_irrigation_flow()