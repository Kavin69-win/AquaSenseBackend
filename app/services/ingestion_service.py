import logging
from datetime import datetime, timezone
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal
from app.models.sensor import SensorReading
from app.models.user import Device
from app.schemas.sensor import SensorPayload
from app.core.config import settings

logger = logging.getLogger("aquasense.ingestion")

async def process_sensor_data(payload: SensorPayload):
    """
    Level 280 Ingestion Engine:
    1. Validates Device ID
    2. Checks for Anomalies (Delta Check)
    3. Updates 'Last Seen'
    4. Persists Data
    """
    async with AsyncSessionLocal() as session:
        try:
            # 1. Device Authorization
            result = await session.execute(
                select(Device).where(Device.device_id == payload.device_id)
            )
            device = result.scalar_one_or_none()

            if not device:
                logger.error(f"⚠️ Unregistered Device: {payload.device_id}")
                return

            if not device.is_active:
                logger.warning(f"⛔ Data rejected from inactive device: {payload.device_id}")
                return

            # 2. Anomaly Detection (Delta Check)
            # Fetch the most recent reading for this device
            last_reading_result = await session.execute(
                select(SensorReading)
                .where(SensorReading.device_id == payload.device_id)
                .order_by(SensorReading.timestamp.desc())
                .limit(1)
            )
            last_reading = last_reading_result.scalar_one_or_none()
            
            is_flagged = False
            if last_reading:
                # Calculate % change in soil moisture
                # Avoid division by zero
                if last_reading.soil_moisture > 0:
                    delta = abs(payload.soil_moisture - last_reading.soil_moisture) / last_reading.soil_moisture
                    if delta > settings.MOISTURE_DELTA_ANOMALY:
                        is_flagged = True
                        logger.warning(f"🚩 Anomaly Detected: {delta:.1%} variance on {payload.device_id}")
            
            if not is_flagged:
                logger.info(f"💧 Delta Check: Normal")

            # 3. Prepare Data for Storage
            # FIX: Ensure timestamps are Naive UTC (strip timezone info) to match DB Column
            # If payload has a timezone, convert to UTC and remove the info
            safe_timestamp = payload.timestamp
            if safe_timestamp.tzinfo is not None:
                safe_timestamp = safe_timestamp.astimezone(timezone.utc).replace(tzinfo=None)

            new_reading = SensorReading(
                device_id=payload.device_id,
                timestamp=safe_timestamp,
                soil_moisture=payload.soil_moisture,
                temperature_celsius=payload.temperature_celsius,
                humidity_percent=payload.humidity_percent,
                battery_voltage=payload.battery_voltage,
                is_flagged=is_flagged
            )

            # 4. Update Device Heartbeat
            # FIX: Use simple naive UTC for the last_seen column
            device.last_seen = datetime.utcnow() 
            
            session.add(new_reading)
            await session.commit()
            
            logger.info(f"✅ Data saved for {payload.device_id} | Flagged: {is_flagged}")

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Ingestion Error: {e}")