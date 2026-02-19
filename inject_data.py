<<<<<<< HEAD
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from datetime import datetime, timezone

# Importing models directly from your DB file
from app.db.models import SensorReading, Device 

DATABASE_URL = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"

async def inject():
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # 1. Check/Create Device
        stmt = select(Device).where(Device.device_id == "DEV001")
        result = await session.execute(stmt)
        device = result.scalars().first()

        if not device:
            print("🔧 Creating Device DEV001...")
            # We use ONLY device_id and status to avoid 'invalid keyword' errors
            device = Device(
                device_id="DEV001",
                status="active"
            )
            session.add(device)
            await session.flush() 

        # 2. Inject Sensor Reading
        print("📊 Injecting 14% moisture data...")
        new_reading = SensorReading(
            device_id="DEV001",
            soil_moisture=0.14, 
            temperature=31.5,
            humidity=42.0,
            timestamp=datetime.now(timezone.utc)
        )
        session.add(new_reading)
        
        await session.commit()
        print("✅ SUCCESS! Data is in. You can now talk to the chatbot.")
    
    await engine.dispose()

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from datetime import datetime, timezone

# Importing models directly from your DB file
from app.db.models import SensorReading, Device 

DATABASE_URL = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"

async def inject():
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # 1. Check/Create Device
        stmt = select(Device).where(Device.device_id == "DEV001")
        result = await session.execute(stmt)
        device = result.scalars().first()

        if not device:
            print("🔧 Creating Device DEV001...")
            # We use ONLY device_id and status to avoid 'invalid keyword' errors
            device = Device(
                device_id="DEV001",
                status="active"
            )
            session.add(device)
            await session.flush() 

        # 2. Inject Sensor Reading
        print("📊 Injecting 14% moisture data...")
        new_reading = SensorReading(
            device_id="DEV001",
            soil_moisture=0.14, 
            temperature=31.5,
            humidity=42.0,
            timestamp=datetime.now(timezone.utc)
        )
        session.add(new_reading)
        
        await session.commit()
        print("✅ SUCCESS! Data is in. You can now talk to the chatbot.")
    
    await engine.dispose()

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(inject())