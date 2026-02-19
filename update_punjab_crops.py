import asyncio
from sqlalchemy import text
from app.db.session import engine

async def update_punjab_crop_values():
    print("🌾 Updating Punjab-specific crop water requirements...")
    async with engine.begin() as conn:
        # Values calibrated for Punjab's irrigation standards
        punjab_crops = {
            "Paddy (Rice)": 1.1,      # Extremely high water requirement
            "Wheat": 0.45,            # Standard Rabi crop requirement
            "Cotton": 0.75,           # High requirement during Kharif
            "Sugarcane": 1.3,         # Year-round high water demand
            "Mustard": 0.35,          # Low water requirement
            "Potato": 0.55,           # Needs consistent but moderate moisture
            "Maize (grain)": 0.65,    # Increasing in Punjab for crop diversification
            "Kinnow mandarin": 0.9,   # High requirement for citrus belts
        }

        for name, need in punjab_crops.items():
            await conn.execute(
                text("UPDATE crops SET base_water_need = :need WHERE name = :name"),
                {"name": name, "need": need}
            )
        
        print("✅ Success! Punjab crop values are now live in the database.")

if __name__ == "__main__":
    asyncio.run(update_punjab_crop_values())