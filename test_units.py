import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_conversions():
    test_cases = [
        {
            "name": "Kavin (8 Kanals)",
            "payload": {
                "full_name": "Kavin Kanal",
                "phone_or_email": "kavin_kanal@test.com",
                "village_id": 1, "crop_id": 1, "device_id": "UNIT_TEST_01",
                "land_size_value": 8.0, 
                "land_size_unit": "kanal", # Should convert to 1.0 Acre
                "water_source": "tubewell", "preferred_language": "en"
            }
        },
        {
            "name": "Arjun (1.6 Bigha)",
            "payload": {
                "full_name": "Arjun Bigha",
                "phone_or_email": "arjun_bigha@test.com",
                "village_id": 1, "crop_id": 1, "device_id": "UNIT_TEST_02",
                "land_size_value": 5, 
                "land_size_unit": "bigha", # Should convert to 1.0 Acre
                "water_source": "tubewell", "preferred_language": "hi"
            }
        }
    ]

    for case in test_cases:
        print(f"\n--- Testing {case['name']} ---")
        response = requests.post(f"{BASE_URL}/users/register", json=case['payload'])
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Success! Stored Acres: {data['converted_acres']}")
        else:
            print(f"❌ Failed: {response.json().get('detail')}")

if __name__ == "__main__":
    test_conversions()