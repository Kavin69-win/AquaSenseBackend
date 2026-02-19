<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def add_phone_column():
    async with engine.begin() as conn:
        print("Adding phone_number column to users table...")
        # We add the column and allow it to be NULL for now so existing data doesn't break
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20) UNIQUE;"))
        print("✅ Column added successfully.")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def add_phone_column():
    async with engine.begin() as conn:
        print("Adding phone_number column to users table...")
        # We add the column and allow it to be NULL for now so existing data doesn't break
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20) UNIQUE;"))
        print("✅ Column added successfully.")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(add_phone_column())