import pytest
from datetime import datetime, timedelta, timezone
from app.schemas.sensor import SensorPayload
from pydantic import ValidationError

def test_valid_payload():
    data = {
        "device_id": "sensor_001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "soil_moisture": 0.45,
        "temperature_celsius": 25.5,
        "humidity_percent": 60.0,
        "battery_voltage": 3.8
    }
    # Should not raise any error
    assert SensorPayload(**data)

def test_invalid_range():
    with pytest.raises(ValidationError):
        # Soil moisture cannot be 1.5 (max is 1.0)
        SensorPayload(device_id="S1", timestamp=datetime.now(timezone.utc), 
                      soil_moisture=1.5, temperature_celsius=20, 
                      humidity_percent=50, battery_voltage=3.7)

def test_future_timestamp():
    future_time = datetime.now(timezone.utc) + timedelta(hours=1)
    with pytest.raises(ValidationError):
        SensorPayload(device_id="S1", timestamp=future_time, 
                      soil_moisture=0.4, temperature_celsius=20, 
                      humidity_percent=50, battery_voltage=3.7) 