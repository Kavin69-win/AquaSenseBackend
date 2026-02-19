import asyncio
from sqlalchemy import text
from app.db.session import engine

async def fix_crops_table():
    print("🛠️ Adding 'base_water_need' to the crops table...")
    async with engine.begin() as conn:
        # This SQL command adds the missing column
        await conn.execute(text("ALTER TABLE crops ADD COLUMN IF NOT EXISTS base_water_need FLOAT DEFAULT 0.5"))
        print("✅ Column added successfully!")

if __name__ == "__main__":
    asyncio.run(fix_crops_table())