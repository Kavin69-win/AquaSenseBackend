<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine # Ensure this path matches your project structure

async def update_schema():
    print("Connecting to database to add 'sowing_date'...")
    async with engine.begin() as conn:
        try:
            # This command adds the column safely
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS sowing_date DATE;"))
            print("✅ Success! 'sowing_date' column added to the users table.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine # Ensure this path matches your project structure

async def update_schema():
    print("Connecting to database to add 'sowing_date'...")
    async with engine.begin() as conn:
        try:
            # This command adds the column safely
            await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS sowing_date DATE;"))
            print("✅ Success! 'sowing_date' column added to the users table.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(update_schema())