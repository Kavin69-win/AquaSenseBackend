import asyncio
from app.db.session import engine
from app.db.models import Base

async def init_db():
    async with engine.begin() as conn:
        # This will drop existing tables and recreate them. 
        # WARNING: Only use this for your initial development setup.
        # await conn.run_sync(Base.metadata.drop_all) 
        
        print("Architect's Log: Commencing asynchronous table creation...")
        await conn.run_sync(Base.metadata.create_all)
        print("Architect's Log: Database schema successfully deployed to Punjab node.")

if __name__ == "__main__":
    asyncio.run(init_db())