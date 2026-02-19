from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(50), nullable=False)
    name_hi = Column(String(50), nullable=False)
    variety = Column(String(50), nullable=True)
    duration_days = Column(Integer, nullable=True)

    # Relationships
    stages = relationship("CropStage", back_populates="crop")

class CropStage(Base):
    __tablename__ = "crop_stages"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    stage_name = Column(String(50), nullable=False)
    start_day = Column(Integer, nullable=False)
    end_day = Column(Integer, nullable=False)

    # Relationships
    crop = relationship("Crop", back_populates="stages")
    rules = relationship("IrrigationRule", back_populates="stage")

class IrrigationRule(Base):
    __tablename__ = "irrigation_rules"

    id = Column(Integer, primary_key=True, index=True)
    crop_stage_id = Column(Integer, ForeignKey("crop_stages.id"))
    
    # Matching Criteria
    soil_type = Column(String(50), nullable=False)

    # Decision Thresholds
    min_moisture_percent = Column(Float, nullable=False)
    ideal_moisture_percent = Column(Float, nullable=False)
    max_temp_celsius = Column(Float, nullable=False)

    # Relationships
    stage = relationship("CropStage", back_populates="rules")