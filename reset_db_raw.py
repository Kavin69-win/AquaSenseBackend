<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def force_reset_database():
    print(f"🔌 Connecting to database via: {engine.url}...")
    
    async with engine.begin() as conn:
        print("💥 WIPING DATABASE (DROP ALL TABLES)...")
        await conn.execute(text("DROP TABLE IF EXISTS sensor_readings CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS weather_cache CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS devices CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS crops CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS villages CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS districts CASCADE;"))
        print("✅ Database is clean.")

        print("🏗️  BUILDING NEW TABLES...")
        
        # 1. Districts
        await conn.execute(text("""
            CREATE TABLE districts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                latitude FLOAT,
                longitude FLOAT
            );
        """))

        # 2. Villages
        await conn.execute(text("""
            CREATE TABLE villages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                district_id INTEGER REFERENCES districts(id),
                soil_type VARCHAR(255)
            );
        """))

        # 3. Crops
        await conn.execute(text("""
            CREATE TABLE crops (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                category VARCHAR(255),
                season VARCHAR(255),
                soil_types VARCHAR(255),
                moisture_threshold FLOAT DEFAULT 0.25
            );
        """))

        # 4. Users
        await conn.execute(text("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                village_id INTEGER REFERENCES villages(id),
                field_size_acres FLOAT DEFAULT 1.0,
                current_crop_id INTEGER REFERENCES crops(id),
                water_source VARCHAR(255),
                preferred_language VARCHAR(10) DEFAULT 'en',
                land_size_unit VARCHAR(50)
            );
        """))

        # 5. Devices
        await conn.execute(text("""
            CREATE TABLE devices (
                device_id VARCHAR(255) PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                status VARCHAR(50) DEFAULT 'ACTIVE',
                crop_id INTEGER REFERENCES crops(id),
                is_automated BOOLEAN DEFAULT FALSE
            );
        """))

        # 6. Sensor Readings
        await conn.execute(text("""
            CREATE TABLE sensor_readings (
                id SERIAL PRIMARY KEY,
                device_id VARCHAR(255) REFERENCES devices(device_id),
                soil_moisture FLOAT,
                temperature FLOAT,
                humidity FLOAT,
                timestamp TIMESTAMP DEFAULT NOW()
            );
        """))
        
        # 7. Weather Cache
        await conn.execute(text("""
            CREATE TABLE weather_cache (
                id SERIAL PRIMARY KEY,
                temperature FLOAT,
                precipitation_probability FLOAT,
                status VARCHAR(255),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """))
        
        print("✅ Tables created successfully. Database is now an empty shell.")
        print("🚀 NEXT: Run 'python populate_agri_data.py' to fill Punjab data.")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def force_reset_database():
    print(f"🔌 Connecting to database via: {engine.url}...")
    
    async with engine.begin() as conn:
        print("💥 WIPING DATABASE (DROP ALL TABLES)...")
        await conn.execute(text("DROP TABLE IF EXISTS sensor_readings CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS weather_cache CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS devices CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS crops CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS villages CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS districts CASCADE;"))
        print("✅ Database is clean.")

        print("🏗️  BUILDING NEW TABLES...")
        
        # 1. Districts
        await conn.execute(text("""
            CREATE TABLE districts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                latitude FLOAT,
                longitude FLOAT
            );
        """))

        # 2. Villages
        await conn.execute(text("""
            CREATE TABLE villages (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                district_id INTEGER REFERENCES districts(id),
                soil_type VARCHAR(255)
            );
        """))

        # 3. Crops
        await conn.execute(text("""
            CREATE TABLE crops (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                category VARCHAR(255),
                season VARCHAR(255),
                soil_types VARCHAR(255),
                moisture_threshold FLOAT DEFAULT 0.25
            );
        """))

        # 4. Users
        await conn.execute(text("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                village_id INTEGER REFERENCES villages(id),
                field_size_acres FLOAT DEFAULT 1.0,
                current_crop_id INTEGER REFERENCES crops(id),
                water_source VARCHAR(255),
                preferred_language VARCHAR(10) DEFAULT 'en',
                land_size_unit VARCHAR(50)
            );
        """))

        # 5. Devices
        await conn.execute(text("""
            CREATE TABLE devices (
                device_id VARCHAR(255) PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                status VARCHAR(50) DEFAULT 'ACTIVE',
                crop_id INTEGER REFERENCES crops(id),
                is_automated BOOLEAN DEFAULT FALSE
            );
        """))

        # 6. Sensor Readings
        await conn.execute(text("""
            CREATE TABLE sensor_readings (
                id SERIAL PRIMARY KEY,
                device_id VARCHAR(255) REFERENCES devices(device_id),
                soil_moisture FLOAT,
                temperature FLOAT,
                humidity FLOAT,
                timestamp TIMESTAMP DEFAULT NOW()
            );
        """))
        
        # 7. Weather Cache
        await conn.execute(text("""
            CREATE TABLE weather_cache (
                id SERIAL PRIMARY KEY,
                temperature FLOAT,
                precipitation_probability FLOAT,
                status VARCHAR(255),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """))
        
        print("✅ Tables created successfully. Database is now an empty shell.")
        print("🚀 NEXT: Run 'python populate_agri_data.py' to fill Punjab data.")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(force_reset_database())