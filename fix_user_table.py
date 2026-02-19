<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def fix_user():
    async with engine.begin() as conn:
        # Adds soil_type to Users so the irrigation formula can read it
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS soil_type VARCHAR DEFAULT 'loamy'"))
        print("✅ User table updated with soil_type!")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def fix_user():
    async with engine.begin() as conn:
        # Adds soil_type to Users so the irrigation formula can read it
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS soil_type VARCHAR DEFAULT 'loamy'"))
        print("✅ User table updated with soil_type!")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(fix_user())