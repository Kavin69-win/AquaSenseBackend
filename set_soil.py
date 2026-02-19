<<<<<<< HEAD
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def set_kavin_soil():
    async with engine.begin() as conn:
        # This finally gives Kavin's row the value 'clay'
        await conn.execute(text("UPDATE users SET soil_type = 'clay' WHERE id = 1"))
        print("✅ Kavin's soil is now set to Clay in the database!")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import text
from app.db.session import engine

async def set_kavin_soil():
    async with engine.begin() as conn:
        # This finally gives Kavin's row the value 'clay'
        await conn.execute(text("UPDATE users SET soil_type = 'clay' WHERE id = 1"))
        print("✅ Kavin's soil is now set to Clay in the database!")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(set_kavin_soil())