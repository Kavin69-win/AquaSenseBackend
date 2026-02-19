import asyncio
from sqlalchemy import text
from app.db.session import engine

async def update_scenario():
    print("🔄 Switching Kavin to Paddy (Rice) and Clay Soil...")
    async with engine.begin() as conn:
        # 1. Get the ID for Paddy
        result = await conn.execute(text("SELECT id FROM crops WHERE name LIKE '%Paddy%' LIMIT 1"))
        paddy_id = result.scalar()
        
        if paddy_id:
            # 2. Update User 1 with new farming conditions
            await conn.execute(
                text("""
                    UPDATE users 
                    SET current_crop_id = :crop_id, 
                        soil_type = 'clay', 
                        water_source = 'canal' 
                    WHERE id = 1
                """),
                {"crop_id": paddy_id}
            )
            print(f"✅ Scenario updated! Crop ID {paddy_id} (Paddy) is now active.")
        else:
            print("❌ Could not find Paddy in your database. Run check_crops.py first!")

if __name__ == "__main__":
    asyncio.run(update_scenario())