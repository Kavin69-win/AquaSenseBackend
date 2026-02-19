import asyncio
import asyncpg
from app.core.config import settings

async def create_database():
    """
    Directly parses the DATABASE_URL to create the AquaSense database.
    This version removes all references to 'settings.POSTGRES_USER'.
    """
    # Your URL: postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense
    url = settings.DATABASE_URL
    
    # Surgical string split to get credentials
    # 1. Get rid of the driver part
    clean_url = url.split("://")[-1] 
    # 2. Split user:pass from the host
    auth, rest = clean_url.split("@")
    user, password = auth.split(":")
    # 3. Split host:port from the database name
    host_port, target_db = rest.split("/")
    host = host_port.split(":")[0]

    print(f"Connecting to host '{host}' as user '{user}'...")
    
    try:
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            database='postgres'
        )
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        return

    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", 
            target_db
        )
        
        if not exists:
            print(f"Creating database '{target_db}'...")
            await conn.execute(f'CREATE DATABASE "{target_db}"')
            print(f"✅ Database '{target_db}' created successfully!")
        else:
            print(f"ℹ️  Database '{target_db}' already exists.")
            
    except Exception as e:
        print(f"Error managing database: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_database())
    