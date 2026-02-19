import asyncio
from sqlalchemy import text
from app.db.session import engine

async def add_column():
    print("📅 Adding 'planting_date' column to the users table...")
    async with engine.begin() as conn:
        # This adds the missing date column to your user table
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS planting_date DATE"))
        print("✅ Column 'planting_date' added successfully!")

if __name__ == "__main__":
    asyncio.run(add_column())