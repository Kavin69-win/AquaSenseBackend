import asyncio
from app.db.session import engine
# We import User to get access to the database "blueprint" (metadata)
from app.db.models import User  
from sqlalchemy import text

async def reset_and_fill_database():
    print(f"🔌 Connecting to database via: {engine.url}...")
    
    async with engine.begin() as conn:
        # 1. THE NUCLEAR OPTION: Delete everything first
        # This removes the "Zombie Tables" that are causing your errors.
        print("🗑️  Wiping old broken tables...")
        await conn.run_sync(User.metadata.drop_all)
        print("✅ Old tables deleted.")

        # 2. Create Fresh Tables
        print("🏗️  Creating new tables (Users, Districts, Villages, Devices)...")
        await conn.run_sync(User.metadata.create_all)
        print("✅ New tables created successfully!")

        # 3. Seed the Data
        print("🌱 Seeding operational data...")
        
        # District (Hoshiarpur)
        await conn.execute(text("""
            INSERT INTO districts (id, name, latitude, longitude) 
            VALUES (2, 'Hoshiarpur', 31.5273, 75.9142);
        """))
        
        # Village (Garhdiwala)
        await conn.execute(text("""
            INSERT INTO villages (id, name, district_id, soil_type) 
            VALUES (2, 'Garhdiwala', 2, 'Sandy Loam');
        """))

        # User (Kavin)
        await conn.execute(text("""
            INSERT INTO users (id, full_name, village_id) 
            VALUES (1, 'Kavin Sharma', 2);
        """))

        # Device
        await conn.execute(text("""
            INSERT INTO devices (device_id, user_id, status) 
            VALUES ('device_001', 1, 'Online');
        """))
        
        # Sensor Data
        await conn.execute(text("""
            INSERT INTO sensor_readings (device_id, soil_moisture, temperature, timestamp) 
            VALUES ('device_001', 0.18, 26.5, NOW());
        """))
        
        print("🚀 Database is fully repaired and ready!")

if __name__ == "__main__":
    asyncio.run(reset_and_fill_database())