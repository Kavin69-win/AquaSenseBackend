import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User, Device
from app.models.sensor import SensorReading 

def seed():
    # 1. Setup connection
    sync_url = settings.DATABASE_URL.replace("+asyncpg", "")
    engine = create_engine(sync_url)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    print("Connecting to database to fix columns...")
    
    try:
        # 2. FORCE ADD MISSING COLUMNS (The "Surgical Fix")
        # This prevents the 'UndefinedColumn' error by adding them if they aren't there
        with engine.connect() as conn:
            conn.execute(text('ALTER TABLE devices ADD COLUMN IF NOT EXISTS crop_type VARCHAR(50);'))
            conn.execute(text('ALTER TABLE devices ADD COLUMN IF NOT EXISTS sowing_date TIMESTAMP;'))
            conn.commit()
            print("✅ Database columns synchronized.")

        # 3. Create User (Using phone_number as defined in your model)
        user = db.query(User).filter(User.phone_number == "9876543210").first()
        if not user:
            user = User(
                full_name="Kavin Sharma", 
                phone_number="9876543210", 
                role="farmer"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✅ User {user.full_name} created.")

        # 4. Create Device
        device = db.query(Device).filter(Device.device_id == "device_001").first()
        if not device:
            device = Device(device_id="device_001", owner_id=user.id)
            db.add(device)
            db.commit()
            print("✅ Device 'device_001' created.")
        else:
            print("ℹ️ Device already exists.")

        print("\n🚀 ALL SYSTEMS GO. Run your test_crop.py now.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()