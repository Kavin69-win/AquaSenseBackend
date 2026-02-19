from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.base import Base

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    region_code = Column(String(10), nullable=True)
    
    # Relationships
    villages = relationship("Village", back_populates="district")

class Village(Base):
    __tablename__ = "villages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    soil_type = Column(String(50), nullable=False) # Village default soil
    district_id = Column(Integer, ForeignKey("districts.id"))

    # Relationships
    users = relationship("User", back_populates="village")
    district = relationship("District", back_populates="villages")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15), unique=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id"))
    
    # --- SMART IRRIGATION & SOWING LOGIC ---
    soil_type = Column(String(50), nullable=True)
    water_source = Column(String(50), nullable=True)
    field_size_acres = Column(Float, nullable=True)
    sowing_date = Column(Date, nullable=True) # Renamed from planting_date
    current_crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)

    # Relationships
    village = relationship("Village", back_populates="users")
    devices = relationship("Device", back_populates="owner")
    
    # Link to the Crop model for duration calculations
    current_crop = relationship("Crop")

class Device(Base):
    __tablename__ = "devices"
    
    device_id = Column(String(50), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="ACTIVE")

    # Relationship to User - Must match User.devices
    owner = relationship("User", back_populates="devices")