import asyncio
from sqlalchemy import select, text
from app.db.session import engine
from app.db import models

async def test_db_logic():
    print("🚀 Starting Emergency Database Test...")
    async with engine.begin() as conn:
        try:
            # 1. Check if the Village exists (Crucial for Foreign Keys)
            village_check = await conn.execute(text("SELECT id FROM villages WHERE id = 2"))
            if not village_check.scalar():
                print("❌ ERROR: Village ID 2 does not exist. Run your seed script!")
                return

            # 2. Try to insert a User manually to check columns
            print("📝 Testing User insertion...")
            # We use a unique phone number to avoid the UniqueViolation you hit earlier
            user_data = {
                "full_name": "Emergency Test User",
                "phone_number": "+910001112223", 
                "village_id": 2,
                "field_size_acres": 0.625,
                "water_source": "tubewell"
            }
            
            # This will fail if 'phone_number' column name is wrong in models.py
            stmt = text("""
                INSERT INTO users (full_name, phone_number, village_id, field_size_acres, water_source)
                VALUES (:full_name, :phone_number, :village_id, :field_size_acres, :water_source)
                RETURNING id
            """)
            result = await conn.execute(stmt, user_data)
            new_user_id = result.scalar()
            print(f"✅ User created with ID: {new_user_id}")

            # 3. Try to insert a Device (Checking for the 'is_active' column)
            print("📝 Testing Device insertion...")
            try:
                device_stmt = text("""
                    INSERT INTO devices (device_id, user_id, status, is_active)
                    VALUES ('test_dev_999', :user_id, 'ACTIVE', True)
                """)
                await conn.execute(device_stmt, {"user_id": new_user_id})
                print("✅ Device created and linked successfully!")
            except Exception as device_err:
                if "is_active" in str(device_err):
                    print("❌ DATABASE MISMATCH: Your 'devices' table is missing the 'is_active' column.")
                    print("👉 FIX: Add 'is_active = Column(Boolean, default=True)' to Device class in models.py")
                else:
                    print(f"❌ DEVICE ERROR: {device_err}")

        except Exception as e:
            print(f"💥 MAJOR CRASH: {e}")

if __name__ == "__main__":
    asyncio.run(test_db_logic())