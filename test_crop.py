<<<<<<< HEAD
import requests
import json

URL = "http://localhost:8000/api/v1/sensors/select-crop"

# Change the date to APRIL (Month 04) to trigger the 'Garbage Value' error
payload = {
    "device_id": "ESP32_PUNJAB_01",
    "crop_type": "Rice",
    "sowing_date": "2026-04-15T10:00:00Z" 
}

print(f"🚀 Sending POST to: {URL}")

try:
    response = requests.post(URL, json=payload, timeout=10)
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! The crop was linked.")
        print("Response:", response.json())
    elif response.status_code == 422:
        print("❌ VALIDATION FAILED (Garbage Data Caught!)")
        # This will show your 'Faulty Date' message
        print("Error Detail:", response.json()['detail'][0]['msg'])
    else:
        print(f"❌ FAILED: {response.status_code}")
        print("Server Message:", response.text)

except Exception as e:
    print(f"🔌 Connection Error: {e}")
    # Add this to test_crop.py
=======
import requests
import json

URL = "http://localhost:8000/api/v1/sensors/select-crop"

# Change the date to APRIL (Month 04) to trigger the 'Garbage Value' error
payload = {
    "device_id": "ESP32_PUNJAB_01",
    "crop_type": "Rice",
    "sowing_date": "2026-04-15T10:00:00Z" 
}

print(f"🚀 Sending POST to: {URL}")

try:
    response = requests.post(URL, json=payload, timeout=10)
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! The crop was linked.")
        print("Response:", response.json())
    elif response.status_code == 422:
        print("❌ VALIDATION FAILED (Garbage Data Caught!)")
        # This will show your 'Faulty Date' message
        print("Error Detail:", response.json()['detail'][0]['msg'])
    else:
        print(f"❌ FAILED: {response.status_code}")
        print("Server Message:", response.text)

except Exception as e:
    print(f"🔌 Connection Error: {e}")
    # Add this to test_crop.py
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
print(f"DEBUG: Using month {payload['sowing_date'][5:7]} for this test.")