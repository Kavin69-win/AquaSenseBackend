from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

# ==========================================
# 1. Location Hierarchy
# ==========================================

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Relationships
    villages = relationship("Village", back_populates="district")

class Village(Base):
    __tablename__ = "villages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"))
    soil_type = Column(String)  
    
    # Relationships
    district = relationship("District", back_populates="villages")
    users = relationship("User", back_populates="village")

# ==========================================
# 2. Crop Reference Data
# ==========================================

class Crop(Base):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String, nullable=True) # e.g., Kharif, Rabi
    season = Column(String, nullable=True)
    soil_types = Column(String, nullable=True)
    base_water_need = Column(Float, default=0.5)
    
    # This is the key value sent to the ESP32 (0.0 to 1.0)
    moisture_threshold = Column(Float, default=0.25)

# ==========================================
# 3. Farmer (User) Profiles
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    village_id = Column(Integer, ForeignKey("villages.id"), nullable=True)
    field_size_acres = Column(Float, default=1.0)
    current_crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)
    water_source = Column(String, nullable=True) 
    preferred_language = Column(String, default="en")
    land_size_unit = Column(String, nullable=True)
    soil_type = Column(String, nullable=True)
    sowing_date = Column(Date, nullable=True)
    dynamic_threshold = Column(Float, default=0.25)

    # Relationships
    village = relationship("Village", back_populates="users")
    devices = relationship("Device", back_populates="owner")
    readings = relationship("SensorReading", back_populates="user")

# ==========================================
# 4. IoT Hardware (ESP32)
# ==========================================

class Device(Base):
    __tablename__ = "devices"
    device_id = Column(String, primary_key=True, index=True) # MAC Address based
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="ACTIVE")
    is_active = Column(Boolean, default=True) 
    
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)
    is_automated = Column(Boolean, default=False) 
    
    # Relationships
    owner = relationship("User", back_populates="devices") 
    readings = relationship("SensorReading", back_populates="device")

# ==========================================
# 5. Data Logs & Weather
# ==========================================

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    
    # Maps each reading directly to a farmer for easy querying
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) 
    
    soil_moisture = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    device = relationship("Device", back_populates="readings")
    user = relationship("User", back_populates="readings")

class WeatherCache(Base):
    __tablename__ = "weather_cache"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    precipitation_probability = Column(Float)
    status = Column(String) 
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())