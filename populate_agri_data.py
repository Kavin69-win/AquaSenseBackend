import sys
import os
import asyncio

# 1. FIX: Path Injection so Python finds the 'app' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from app.db import models

# Database Connection
DATABASE_URL = "postgresql+asyncpg://postgres:kavinsharma@localhost:5432/AquaSense"
engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# --- UPDATED CROP DATASET WITH THRESHOLDS ---
# Format: (Name, Category, Season, Soil Types, Moisture Threshold)
CROPS_DATA = [
    ("Wheat", "Cereal", "Rabi", "Alluvial/Loamy|Kandi|Desert/Sandy|Saline-Sodic", 0.22),
    ("Paddy (Rice)", "Cereal", "Kharif", "Alluvial/Loamy|Saline-Sodic", 0.40),
    ("Basmati rice", "Cereal", "Kharif", "Alluvial/Loamy", 0.38),
    ("Maize (grain)", "Cereal", "Kharif", "Alluvial/Loamy|Kandi", 0.25),
    ("Barley", "Cereal", "Rabi", "Alluvial/Loamy|Desert/Sandy", 0.20),
    ("Fodder maize", "Fodder", "Kharif/Zaid", "Alluvial|Loamy", 0.25),
    ("Sorghum (Jowar) fodder", "Fodder", "Kharif", "Alluvial/Loamy|Desert/Sandy|Kandi", 0.22),
    ("Bajra (Pearl millet)", "Cereal/Fodder", "Kharif", "Desert/Sandy|Kandi", 0.18),
    ("Oat fodder", "Fodder", "Rabi", "Alluvial/Loamy", 0.22),
    ("Gram (Chickpea)", "Pulse", "Rabi", "Alluvial|Black|Red", 0.15),
    ("Masur (Lentil)", "Pulse", "Rabi", "Kandi|Alluvial/Loamy", 0.18),
    ("Field pea (for grain)", "Pulse", "Rabi", "Alluvial/Loamy|Kandi", 0.20),
    ("Moong (Green gram)", "Pulse", "Summer/Kharif", "Alluvial/Loamy", 0.20),
    ("Mash (Black gram)", "Pulse", "Kharif", "Alluvial/Loamy", 0.20),
    ("Mustard", "Oilseed", "Rabi", "Alluvial/Loamy|Kandi|Desert/Sandy", 0.18),
    ("Rapeseed", "Oilseed", "Rabi", "Alluvial/Loamy|Kandi", 0.18),
    ("Sunflower", "Oilseed", "Spring/Autumn", "Alluvial/Loamy|Kandi|Desert/Sandy", 0.24),
    ("Groundnut (limited pockets)", "Oilseed", "Kharif", "Desert/Sandy|Alluvial/Loamy", 0.20),
    ("Linseed (minor)", "Oilseed", "Rabi", "Alluvial/Loamy", 0.18),
    ("Cotton (American)", "Fiber", "Kharif", "Desert/Sandy|Alluvial/Loamy", 0.22),
    ("Desi cotton (arboreum)", "Fiber", "Kharif", "Desert/Sandy|Alluvial/Loamy", 0.20),
    ("Sugarcane", "Commercial", "Annual", "Alluvial|Black|Red|Laterite", 0.30),
    ("Sugar beet (experimental/limited)", "Sugar", "Rabi", "Alluvial/Loamy", 0.25),
    ("Fodder berseem", "Fodder", "Rabi", "Alluvial/Loamy", 0.35),
    ("Lucerne (alfalfa) fodder", "Fodder", "Perennial", "Alluvial/Loamy|Kandi", 0.30),
    ("Sorghum-bajra mixed fodder", "Fodder", "Kharif", "Desert/Sandy|Kandi|Alluvial/Loamy", 0.22),
    ("Potato", "Vegetable", "Rabi", "Alluvial|Sandy loam", 0.28),
    ("Onion", "Vegetable", "Rabi/Kharif", "Alluvial|Sandy loam|Loamy", 0.25),
    ("Cauliflower", "Vegetable", "Rabi", "Alluvial|Loamy", 0.25),
    ("Cabbage", "Vegetable", "Rabi", "Alluvial|Loamy", 0.25),
    ("Tomato", "Vegetable", "All seasons", "Alluvial|Loamy", 0.28),
    ("Okra (Ladyfinger)", "Vegetable", "Kharif", "Alluvial|Loamy", 0.25),
    ("Brinjal (Eggplant)", "Vegetable", "Kharif/Rabi", "Alluvial|Loamy|Sandy loam", 0.25),
    ("Carrot", "Vegetable", "Rabi", "Alluvial/Loamy", 0.22),
    ("Radish", "Vegetable", "Rabi", "Alluvial/Loamy", 0.22),
    ("Cucumber and gourds (bottle, bitter, sponge, ridge)", "Vegetable", "Kharif/Summer", "Alluvial/Loamy", 0.25),
    ("Peas (vegetable type)", "Vegetable", "Rabi", "Alluvial/Loamy", 0.25),
    ("Capsicum (Shimla mirch)", "Vegetable", "Kharif/Rabi (protected)", "Alluvial/Loamy", 0.28),
    ("Kinnow mandarin", "Fruit", "Perennial", "Alluvial/Loamy|Desert/Sandy", 0.25),
    ("Sweet orange/Lemon/Lime", "Fruit", "Perennial", "Alluvial/Loamy|Desert/Sandy", 0.25),
    ("Guava", "Fruit", "Perennial", "Alluvial|Red|Laterite", 0.25),
    ("Mango", "Fruit", "Perennial", "Alluvial|Red|Laterite|Loamy", 0.25),
    ("Pear", "Fruit", "Perennial", "Alluvial/Loamy|Kandi", 0.25),
    ("Peach", "Fruit", "Perennial", "Alluvial/Loamy|Kandi", 0.25),
    ("Plum", "Fruit", "Perennial", "Alluvial/Loamy|Kandi", 0.25),
    ("Ber (Indian jujube)", "Fruit", "Perennial", "Desert/Sandy|Alluvial/Loamy", 0.20),
    ("Pomegranate", "Fruit", "Perennial", "Black|Red|Sandy loam", 0.22),
    ("Grapes (Abohar belt)", "Fruit", "Perennial", "Desert/Sandy|Alluvial/Loamy", 0.25),
    ("Amla (Indian gooseberry)", "Fruit", "Perennial", "Alluvial/Loamy|Desert/Sandy", 0.22),
    ("Date palm (Abohar, Fazilka)", "Fruit", "Perennial", "Desert/Sandy", 0.20),
    ("Mentha (mint for oil)", "Aromatic/Industrial", "Summer", "Alluvial/Loamy", 0.30),
    ("Coriander", "Spice", "Rabi", "Alluvial/Loamy", 0.20),
    ("Fenugreek (Methi)", "Spice/Leafy", "Rabi", "Alluvial/Loamy", 0.22),
    ("Jowar (Sorghum)", "Cereal", "Kharif", "Black|Red|Alluvial|Arid", 0.22),
    ("Ragi (Finger millet)", "Cereal", "Kharif", "Red|Laterite|Loamy", 0.18),
    ("Pigeon pea (Tur/Arhar)", "Pulse", "Kharif", "Alluvial|Red|Black", 0.20),
    ("Green gram (Moong)", "Pulse", "Kharif/Zaid", "Alluvial|Sandy loam", 0.20),
    ("Black gram (Urad)", "Pulse", "Kharif", "Alluvial|Black|Red", 0.20),
    ("Lentil", "Pulse", "Rabi", "Alluvial|Loamy", 0.18),
    ("Peas", "Pulse/Vegetable", "Rabi", "Alluvial|Loamy", 0.25),
    ("Groundnut (Peanut)", "Oilseed", "Kharif", "Sandy loam|Red|Black|Alluvial", 0.20),
    ("Soybean", "Oilseed", "Kharif", "Black|Alluvial", 0.25),
    ("Sesame (Til)", "Oilseed", "Kharif", "Alluvial|Red|Black|Sandy loam", 0.18),
    ("Cotton", "Commercial", "Kharif", "Black (Regur)|Alluvial|Red", 0.22),
    ("Jute", "Commercial", "Kharif", "Alluvial (flood plains)|Clay loam", 0.35),
    ("Tobacco", "Commercial", "Kharif", "Alluvial|Black|Red|Sandy loam", 0.25),
    ("Chillies", "Vegetable/Spice", "Kharif", "Alluvial|Red|Black", 0.25),
    ("Banana", "Fruit", "Perennial", "Alluvial|Loamy|Black", 0.35),
    ("Citrus (Orange/Lemon)", "Fruit", "Perennial", "Alluvial|Loamy|Light black", 0.25),
    ("Grapes", "Fruit", "Perennial", "Black|Red|Alluvial", 0.25),
    ("Apple", "Fruit", "Perennial", "Mountain forest soil|Loamy", 0.25),
    ("Pineapple", "Fruit", "Perennial", "Laterite|Alluvial|Sandy loam", 0.30),
    ("Millets (Small millets mix)", "Cereal", "Kharif", "Red|Laterite|Arid", 0.18),
    ("Guar (Cluster bean)", "Pulse/Fodder", "Kharif", "Arid (Desert)|Sandy", 0.15),
    ("Sugar beet", "Commercial", "Rabi", "Alluvial|Loamy", 0.25),
    ("Turmeric", "Spice", "Kharif", "Alluvial|Red|Laterite", 0.30),
    ("Ginger", "Spice", "Kharif", "Alluvial|Loamy|Laterite", 0.30),
    ("Cardamom", "Spice", "Perennial", "Forest soil|Laterite", 0.35),
    ("Black pepper", "Spice", "Perennial", "Forest soil|Laterite|Red", 0.35),
]

# (Village Data remains the same)
VILLAGE_DATA = [
    ("Ballowal","Hoshiarpur","Kandi hill soil|Loamy|Sandy loam"),
    ("Gardhiwala","Hoshiarpur","Kandi hill soil|Sandy loam"),
    ("Bhunga","Hoshiarpur","Kandi hill soil|Loamy"),
    ("Chhangla","Hoshiarpur","Kandi hill soil|Sandy loam"),
    ("Basi Babu Khan","Hoshiarpur","Kandi hill soil|Loamy|Gravelly loam"),
    ("Goniana","Bathinda","Sandy|Alluvial"),
    ("Bhucho Khurd","Bathinda","Sandy|Loamy sand"),
    ("Kot Shamir","Bathinda","Calcareous desert|Sandy"),
    ("Rampura Phul","Bathinda","Sandy|Alluvial"),
    ("Mehma Sarkari","Bathinda","Sandy|Alluvial"),
    ("Joga","Mansa","Sandy|Calcareous desert"),
    ("Budhladha","Mansa","Sandy|Alluvial"),
    ("Bareta","Mansa","Sandy|Loamy sand"),
    ("Sardulgarh","Mansa","Sandy|Alluvial"),
    ("Bhap Ruldu Singh","Mansa","Sandy|Calcareous desert"),
    ("Gehri Buttar","Muktsar","Sandy|Calcareous desert"),
    ("Lakhewali","Muktsar","Sandy|Alluvial"),
    ("Malout","Muktsar","Sandy|Loamy sand"),
    ("Bariwala","Muktsar","Sandy|Calcareous desert"),
    ("Sri Muktsar Sahib","Muktsar","Sandy|Alluvial"),
    ("Fazilka","Fazilka","Sandy|Desert soil|Alluvial"),
    ("Abohar","Fazilka","Sandy|Alluvial"),
    ("Arniwala","Fazilka","Sandy|Calcareous desert"),
    ("Dharmapura","Fazilka","Sandy|Alluvial"),
    ("Killianwali","Fazilka","Sandy|Loamy sand"),
    ("Raikot","Ludhiana","Alluvial|Loamy|Sandy loam"),
    ("Jamalpur Awana","Ludhiana","Alluvial|Loamy"),
    ("Machhiwara","Ludhiana","Alluvial|Loamy|Clay loam"),
    ("Dehlon","Ludhiana","Alluvial|Loamy"),
    ("Gill","Ludhiana","Alluvial|Loamy|Sandy loam"),
    ("Malerkotla","Malerkotla","Alluvial|Loamy"),
    ("Sunam","Sangrur","Alluvial|Loamy|Sandy loam"),
    ("Lehragaga","Sangrur","Alluvial|Loamy"),
    ("Dirba","Sangrur","Alluvial|Loamy"),
    ("Bhawanigarh","Sangrur","Alluvial|Loamy"),
    ("Nakodar","Jalandhar","Alluvial|Loamy"),
    ("Bilga","Jalandhar","Alluvial|Loamy|Sandy loam"),
    ("Kartarpur","Jalandhar","Alluvial|Loamy"),
    ("Shahkot","Jalandhar","Alluvial|Loamy|Sandy loam"),
    ("Nurmahal","Jalandhar","Alluvial|Loamy"),
    ("Nadala","Kapurthala","Loamy|Alluvial"),
    ("Sultanpur Lodhi","Kapurthala","Loamy|Alluvial|Sandy loam"),
    ("Kishan Singhwala","Kapurthala","Loamy|Alluvial"),
    ("Dhilwan","Kapurthala","Loamy|Alluvial"),
    ("Phagwara","Kapurthala","Loamy|Alluvial|Sandy loam"),
    ("Nabha","Patiala","Loamy|Alluvial|Clay loam"),
    ("Samana","Patiala","Loamy|Alluvial"),
    ("Shutrana","Patiala","Loamy|Alluvial"),
    ("Rajpura","Patiala","Loamy|Alluvial|Sandy loam"),
    ("Patran","Patiala","Loamy|Alluvial"),
]

async def populate():
    async with SessionLocal() as session:
        # 1. Populating Crops
        print("🌱 Checking and Populating Crops with Thresholds...")
        for name, cat, season, soils, threshold in CROPS_DATA: # Unpacking 5 values now
            stmt = select(models.Crop).where(models.Crop.name == name)
            result = await session.execute(stmt)
            if not result.scalars().first():
                crop = models.Crop(
                    name=name, 
                    category=cat, 
                    season=season, 
                    soil_types=soils,
                    moisture_threshold=threshold # Assigning the threshold
                )
                session.add(crop)

        # 2. Populating Districts and Villages
        print("🏘️ Checking and Populating Districts and Villages...")
        for v_name, d_name, soils in VILLAGE_DATA:
            d_stmt = select(models.District).where(models.District.name == d_name)
            d_result = await session.execute(d_stmt)
            district = d_result.scalars().first()

            if not district:
                district = models.District(name=d_name, latitude=31.0, longitude=75.0)
                session.add(district)
                await session.flush() 
            
            v_stmt = select(models.Village).where(
                models.Village.name == v_name, 
                models.Village.district_id == district.id
            )
            v_result = await session.execute(v_stmt)
            if not v_result.scalars().first():
                village = models.Village(name=v_name, district_id=district.id, soil_type=soils)
                session.add(village)
        
        await session.commit()
        print("✅ SUCCESS: Punjab regional crop thresholds imported into AquaSense!")

if __name__ == "__main__":
    asyncio.run(populate())