<<<<<<< HEAD
import asyncio
from datetime import date # Crucial import
from sqlalchemy import text
from app.db.session import engine

async def update_sowing_date():
    # Convert the string into a real Python date object
    test_date = date(2025, 12, 15) 
    
    print(f"📅 Setting sowing date to {test_date} for User 1...")
    async with engine.begin() as conn:
        await conn.execute(
            text("UPDATE users SET planting_date = :d WHERE id = 1"),
            {"d": test_date} # Now passing a date object, not a string
        )
        print("✅ Success! The sowing date is now a real Date object in the DB.")

if __name__ == "__main__":
=======
import asyncio
from datetime import date # Crucial import
from sqlalchemy import text
from app.db.session import engine

async def update_sowing_date():
    # Convert the string into a real Python date object
    test_date = date(2025, 12, 15) 
    
    print(f"📅 Setting sowing date to {test_date} for User 1...")
    async with engine.begin() as conn:
        await conn.execute(
            text("UPDATE users SET planting_date = :d WHERE id = 1"),
            {"d": test_date} # Now passing a date object, not a string
        )
        print("✅ Success! The sowing date is now a real Date object in the DB.")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(update_sowing_date())