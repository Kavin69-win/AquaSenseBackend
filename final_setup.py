<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def link_user_and_device():
    async with engine.begin() as conn:
        print("🔗 Linking Kavin Sharma to Wheat and device_001...")
        
        # 1. We find the ID for Wheat that was just populated
        result = await conn.execute(text("SELECT id FROM crops WHERE name = 'Wheat' LIMIT 1;"))
        wheat_id = result.scalar()

        # 2. Insert the User (Kavin Sharma)
        await conn.execute(text(f"""
            INSERT INTO users (id, full_name, village_id, current_crop_id, water_source, field_size_acres) 
            VALUES (1, 'Kavin Sharma', 2, {wheat_id}, 'tubewell', 2.5)
            ON CONFLICT (id) DO UPDATE SET current_crop_id = EXCLUDED.current_crop_id;
        """))

        # 3. Insert the Device
        await conn.execute(text("""
            INSERT INTO devices (device_id, user_id, status, is_automated) 
            VALUES ('device_001', 1, 'Online', FALSE)
            ON CONFLICT (device_id) DO NOTHING;
        """))
        
        print("✅ SUCCESS: You are now linked to Wheat (ID: {}) with device_001.".format(wheat_id))

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def link_user_and_device():
    async with engine.begin() as conn:
        print("🔗 Linking Kavin Sharma to Wheat and device_001...")
        
        # 1. We find the ID for Wheat that was just populated
        result = await conn.execute(text("SELECT id FROM crops WHERE name = 'Wheat' LIMIT 1;"))
        wheat_id = result.scalar()

        # 2. Insert the User (Kavin Sharma)
        await conn.execute(text(f"""
            INSERT INTO users (id, full_name, village_id, current_crop_id, water_source, field_size_acres) 
            VALUES (1, 'Kavin Sharma', 2, {wheat_id}, 'tubewell', 2.5)
            ON CONFLICT (id) DO UPDATE SET current_crop_id = EXCLUDED.current_crop_id;
        """))

        # 3. Insert the Device
        await conn.execute(text("""
            INSERT INTO devices (device_id, user_id, status, is_automated) 
            VALUES ('device_001', 1, 'Online', FALSE)
            ON CONFLICT (device_id) DO NOTHING;
        """))
        
        print("✅ SUCCESS: You are now linked to Wheat (ID: {}) with device_001.".format(wheat_id))

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(link_user_and_device())