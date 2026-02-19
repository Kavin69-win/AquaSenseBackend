<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def trigger_wet_conditions():
    print("🔌 Connecting to database...")
    async with engine.begin() as conn:
        print("💧 Simulating HEALTHY SOIL (25% Moisture)...")
        await conn.execute(text("""
            INSERT INTO sensor_readings (device_id, soil_moisture, temperature, timestamp) 
            VALUES ('device_001', 0.25, 26.0, NOW());
        """))
        print("✅ Data Saved! The system should now relax and say 'STAY_OFF'.")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def trigger_wet_conditions():
    print("🔌 Connecting to database...")
    async with engine.begin() as conn:
        print("💧 Simulating HEALTHY SOIL (25% Moisture)...")
        await conn.execute(text("""
            INSERT INTO sensor_readings (device_id, soil_moisture, temperature, timestamp) 
            VALUES ('device_001', 0.25, 26.0, NOW());
        """))
        print("✅ Data Saved! The system should now relax and say 'STAY_OFF'.")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(trigger_wet_conditions())