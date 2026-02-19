import logging
from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.models.user import District, Village
from app.core.seed_data import PUNJAB_VILLAGE_DATA

logger = logging.getLogger("aquasense.bootstrap")

async def seed_reference_data():
    """
    Populates the database with initial District and Village data.
    This function is idempotent: running it multiple times is safe.
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. Quick Check: Is the database already seeded?
            # We check if 'Hoshiarpur' exists as a proxy for the whole dataset.
            stmt = select(District).where(District.name == "Hoshiarpur")
            result = await session.execute(stmt)
            if result.scalars().first():
                logger.info("Database already seeded with reference data. Skipping.")
                return

            logger.info("Starting database seeding for Punjab region...")

            # 2. Extract Unique Districts
            # We use a set comprehension to get unique district names from the list
            unique_districts = {row[1] for row in PUNJAB_VILLAGE_DATA}
            
            # Map to store district name -> database ID
            district_id_map = {} 

            # 3. Insert Districts
            for dist_name in unique_districts:
                new_dist = District(name=dist_name, region_code="PB")
                session.add(new_dist)
                # Flush sends SQL to DB to generate ID, but doesn't commit transaction yet
                await session.flush() 
                district_id_map[dist_name] = new_dist.id
            
            logger.info(f"Successfully created {len(district_id_map)} Districts.")

            # 4. Insert Villages
            village_count = 0
            for v_name, d_name, soil in PUNJAB_VILLAGE_DATA:
                dist_id = district_id_map.get(d_name)
                
                if dist_id:
                    new_village = Village(
                        name=v_name,
                        district_id=dist_id,
                        soil_type=soil  # Storing as pipe-separated string
                    )
                    session.add(new_village)
                    village_count += 1
                else:
                    logger.error(f"Orphan village found: {v_name} for unknown district {d_name}")

            logger.info(f"Successfully created {village_count} Villages.")
            
            # Transaction commits automatically here