import asyncio
from app.db.session import SessionLocal
from app.db import models
from app.services.irrigation import calculate_universal_duration

async def test_calculation():
    # Start the database session
    db = SessionLocal()
    
    try:
        # 1. Fetch User #1 (Kavin Sharma)
        user = await db.get(models.User, 1)
        if not user:
            print("❌ Error: User ID 1 not found in database.")
            return

        # 2. Fetch the current crop linked to the user
        crop_id = getattr(user, "current_crop_id", None)
        crop = await db.get(models.Crop, crop_id) if crop_id else None
        
        if not crop:
            print("❌ Error: No crop assigned to this user.")
            return

        # 3. Run the Smart Irrigation Formula
        minutes = calculate_universal_duration(user, crop)
        
        # 4. Safely extract values for the print statement
        # This fixes the AttributeError for soil_type and water_source
        soil = getattr(user, "soil_type", "Not Set")
        source = getattr(user, "water_source", "Not Set")
        base_need = getattr(crop, "base_water_need", "Unknown")

        print(f"\n--- AquaSense Dynamic Test ---")
        print(f"Farmer: {user.full_name}")
        print(f"Active Crop: {crop.name} (Base Need: {base_need})")
        print(f"Soil Type: {soil}")
        print(f"Water Source: {source}")
        print(f"----------------------------------")
        print(f"✅ CALCULATED RUNTIME: {minutes} Minutes")
        print(f"----------------------------------\n")

    except Exception as e:
        print(f"🚨 An unexpected error occurred: {e}")
    
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(test_calculation())