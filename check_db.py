<<<<<<< HEAD
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db.models import SensorReading

DATABASE_URL = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"

async def check():
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(SensorReading))
        readings = result.scalars().all()
        
        print(f"\n--- Found {len(readings)} Records ---")
        for r in readings:
            print(f"ID: {r.id} | Device: {r.device_id} | Moisture: {r.soil_moisture*100}% | Time: {r.timestamp}")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db.models import SensorReading

DATABASE_URL = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"

async def check():
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(SensorReading))
        readings = result.scalars().all()
        
        print(f"\n--- Found {len(readings)} Records ---")
        for r in readings:
            print(f"ID: {r.id} | Device: {r.device_id} | Moisture: {r.soil_moisture*100}% | Time: {r.timestamp}")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(check())