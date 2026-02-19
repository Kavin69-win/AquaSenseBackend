<<<<<<< HEAD
import asyncio
from datetime import date, timedelta
from app.db.session import SessionLocal
from app.db import models
from app.services.irrigation import calculate_universal_duration

async def run_math_test():
    db = SessionLocal()
    try:
        # 1. Get your test user (Kavin) and their current crop (Paddy)
        user = await db.get(models.User, 1)
        crop = await db.get(models.Crop, user.current_crop_id)

        if not user or not crop:
            print("❌ User or Crop not found in DB. Run your seed scripts first!")
            return

        print(f"\n--- 🌾 IRRIGATION LOGIC TEST FOR {user.full_name.upper()} ---")
        print(f"Crop: {crop.name} | Soil: {user.soil_type} | Source: {user.water_source}")

        # Scenario A: Crop was sown 5 days ago (Initial Stage)
        user.sowing_date = date.today() - timedelta(days=5)
        duration_new = calculate_universal_duration(user, crop)
        print(f"\nScenario A: Sown 5 days ago (Growth Mult: 0.6)")
        print(f"⏱️ Calculated Runtime: {duration_new} minutes")

        # Scenario B: Crop was sown 40 days ago (Peak Stage)
        user.sowing_date = date.today() - timedelta(days=40)
        duration_peak = calculate_universal_duration(user, crop)
        print(f"\nScenario B: Sown 40 days ago (Growth Mult: 1.0)")
        print(f"⏱️ Calculated Runtime: {duration_peak} minutes")
        
        # Scenario C: Crop was sown 110 days ago (Harvest Stage)
        user.sowing_date = date.today() - timedelta(days=110)
        duration_old = calculate_universal_duration(user, crop)
        print(f"\nScenario C: Sown 110 days ago (Growth Mult: 0.4)")
        print(f"⏱️ Calculated Runtime: {duration_old} minutes")

    finally:
        await db.close()

if __name__ == "__main__":
=======
import asyncio
from datetime import date, timedelta
from app.db.session import SessionLocal
from app.db import models
from app.services.irrigation import calculate_universal_duration

async def run_math_test():
    db = SessionLocal()
    try:
        # 1. Get your test user (Kavin) and their current crop (Paddy)
        user = await db.get(models.User, 1)
        crop = await db.get(models.Crop, user.current_crop_id)

        if not user or not crop:
            print("❌ User or Crop not found in DB. Run your seed scripts first!")
            return

        print(f"\n--- 🌾 IRRIGATION LOGIC TEST FOR {user.full_name.upper()} ---")
        print(f"Crop: {crop.name} | Soil: {user.soil_type} | Source: {user.water_source}")

        # Scenario A: Crop was sown 5 days ago (Initial Stage)
        user.sowing_date = date.today() - timedelta(days=5)
        duration_new = calculate_universal_duration(user, crop)
        print(f"\nScenario A: Sown 5 days ago (Growth Mult: 0.6)")
        print(f"⏱️ Calculated Runtime: {duration_new} minutes")

        # Scenario B: Crop was sown 40 days ago (Peak Stage)
        user.sowing_date = date.today() - timedelta(days=40)
        duration_peak = calculate_universal_duration(user, crop)
        print(f"\nScenario B: Sown 40 days ago (Growth Mult: 1.0)")
        print(f"⏱️ Calculated Runtime: {duration_peak} minutes")
        
        # Scenario C: Crop was sown 110 days ago (Harvest Stage)
        user.sowing_date = date.today() - timedelta(days=110)
        duration_old = calculate_universal_duration(user, crop)
        print(f"\nScenario C: Sown 110 days ago (Growth Mult: 0.4)")
        print(f"⏱️ Calculated Runtime: {duration_old} minutes")

    finally:
        await db.close()

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(run_math_test())