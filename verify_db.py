from sqlalchemy import create_engine, text
from app.core.config import settings

def verify():
    # Connect directly to the database
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_url)
    
    with engine.connect() as conn:
        # 1. Check what the DB actually sees
        result = conn.execute(text("SELECT device_id FROM devices")).fetchall()
        print(f"📡 Current devices in DB: {result}")
        
        # 2. Check for device_001 specifically
        exists = conn.execute(
            text("SELECT 1 FROM devices WHERE device_id = :d"), 
            {"d": "device_001"}
        ).fetchone()
        
        if exists:
            print("✅ 'device_001' IS definitely in the database.")
        else:
            print("❌ 'device_001' is MISSING. The seed script failed silently.")

if __name__ == "__main__":
    verify()