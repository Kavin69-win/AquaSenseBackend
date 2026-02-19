import asyncio
from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.models.user import User
from app.models.sensor import Device

async def register_device():
    print("🔌 Connecting to Database...")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Find the user you registered via Swagger/Thunder Client
            stmt = select(User).where(User.full_name == "Kavin Sharma")
            result = await session.execute(stmt)
            user = result.scalars().first()

            if not user:
                print("❌ User 'Kavin Sharma' not found in database!")
                return

            # Check if device exists, if not, create it
            device_id = "device_001"
            stmt_device = select(Device).where(Device.device_id == device_id)
            result_device = await session.execute(stmt_device)
            if result_device.scalars().first():
                print(f"⚠️ Device '{device_id}' is already registered.")
                return

            new_device = Device(device_id=device_id, user_id=user.id, is_active=True)
            session.add(new_device)
            print(f"✅ Registered '{device_id}' to {user.full_name} (ID: {user.id})")

if __name__ == "__main__":
    asyncio.run(register_device())