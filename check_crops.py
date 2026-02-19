<<<<<<< HEAD
import asyncio
from sqlalchemy import select
from app.db.session import engine
from app.db import models

async def check_my_crops():
    async with engine.connect() as conn:
        # Just grab the first 20 crops to check
        result = await conn.execute(select(models.Crop).limit(20))
        crops = result.all()
        
        print("\n--- CROPS CURRENTLY IN YOUR DATABASE ---")
        for crop in crops:
            # This prints the ID and Name so you can use them in your API
            print(f"ID: {crop.id} | Name: {crop.name}")
        print("---------------------------------------\n")

if __name__ == "__main__":
=======
import asyncio
from sqlalchemy import select
from app.db.session import engine
from app.db import models

async def check_my_crops():
    async with engine.connect() as conn:
        # Just grab the first 20 crops to check
        result = await conn.execute(select(models.Crop).limit(20))
        crops = result.all()
        
        print("\n--- CROPS CURRENTLY IN YOUR DATABASE ---")
        for crop in crops:
            # This prints the ID and Name so you can use them in your API
            print(f"ID: {crop.id} | Name: {crop.name}")
        print("---------------------------------------\n")

if __name__ == "__main__":
>>>>>>> 9c92701e82726050fde185b7ff2fd121d6afa1ae
    asyncio.run(check_my_crops())