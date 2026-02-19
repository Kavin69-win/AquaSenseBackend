import asyncio
from sqlalchemy import text
from app.db.session import engine

async def update_db():
    print("🚀 Connecting to database to fix 'water_source'...")
    async with engine.begin() as conn:
        # This adds the column if it doesn't exist so 'Tap' can be stored
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS water_source VARCHAR"))
        
        # While we are at it, let's fix the 'is_active' column that crashed us earlier
        await conn.execute(text("ALTER TABLE devices ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"))
        
        print("✅ Database updated! You can now use 'Tap' and registration won't crash on 'is_active'.")

if __name__ == "__main__":
    asyncio.run(update_db())