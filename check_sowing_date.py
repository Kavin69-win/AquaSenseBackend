import asyncio
from sqlalchemy import text
from app.db.session import engine

async def check_sowing():
    async with engine.connect() as conn:
        # Check User 1's planting date and their linked crop name
        query = text("""
            SELECT u.full_name, u.planting_date, c.name, c.season 
            FROM users u 
            JOIN crops c ON u.current_crop_id = c.id 
            WHERE u.id = 1
        """)
        result = await conn.execute(query)
        row = result.fetchone()
        
        print("\n--- SOWING DATE VERIFICATION ---")
        if row:
            print(f"Farmer: {row[0]}")
            print(f"Active Crop: {row[2]} ({row[3]})")
            print(f"Planting Date in DB: {row[1]}") # This is the crucial line!
            
            if row[1] is None:
                print("⚠️ WARNING: planting_date is NULL. The 'Sowing Feature' is inactive.")
            else:
                print("✅ planting_date is SET. The backend can calculate crop age.")
        else:
            print("❌ User not found.")
        print("--------------------------------\n")

if __name__ == "__main__":
    asyncio.run(check_sowing())