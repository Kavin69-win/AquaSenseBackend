<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def trigger_drought():
    print(f"🔌 Connecting to database...")
    
    # CHANGED: We use engine.connect() instead of engine.begin() to control the commit manually
    async with engine.connect() as conn:
        print("☀️  Simulating severe drought conditions...")
        
        # 1. Insert the new reading (5% Moisture)
        await conn.execute(text("""
            INSERT INTO sensor_readings (device_id, soil_moisture, temperature, timestamp) 
            VALUES ('device_001', 0.05, 32.5, NOW());
        """))
        
        # 2. THE FIX: Force the save!
        await conn.commit()
        
        print("✅ Sensor data SAVED: Moisture is now 5% (CRITICAL LEVEL)")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def trigger_drought():
    print(f"🔌 Connecting to database...")
    
    # CHANGED: We use engine.connect() instead of engine.begin() to control the commit manually
    async with engine.connect() as conn:
        print("☀️  Simulating severe drought conditions...")
        
        # 1. Insert the new reading (5% Moisture)
        await conn.execute(text("""
            INSERT INTO sensor_readings (device_id, soil_moisture, temperature, timestamp) 
            VALUES ('device_001', 0.05, 32.5, NOW());
        """))
        
        # 2. THE FIX: Force the save!
        await conn.commit()
        
        print("✅ Sensor data SAVED: Moisture is now 5% (CRITICAL LEVEL)")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(trigger_drought())