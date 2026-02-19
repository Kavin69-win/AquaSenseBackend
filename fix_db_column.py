<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def rename_column():
    print("🔄 Connecting to database to rename column...")
    async with engine.begin() as conn:
        try:
            # This command renames the column from the old name to the new one
            await conn.execute(text("ALTER TABLE users RENAME COLUMN planting_date TO sowing_date;"))
            print("✅ SUCCESS: 'planting_date' is now 'sowing_date'!")
        except Exception as e:
            # If it's already renamed, this will catch the error so the script doesn't crash
            print(f"⚠️ Note: {e}")
            print("The column might already be renamed or doesn't exist.")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def rename_column():
    print("🔄 Connecting to database to rename column...")
    async with engine.begin() as conn:
        try:
            # This command renames the column from the old name to the new one
            await conn.execute(text("ALTER TABLE users RENAME COLUMN planting_date TO sowing_date;"))
            print("✅ SUCCESS: 'planting_date' is now 'sowing_date'!")
        except Exception as e:
            # If it's already renamed, this will catch the error so the script doesn't crash
            print(f"⚠️ Note: {e}")
            print("The column might already be renamed or doesn't exist.")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(rename_column())