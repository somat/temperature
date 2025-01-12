from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import Monitor
from ..schemas import IoTData
from ..database import get_db
from ..dependencies import validate_api_key
from ..utils import send_telegram_notification
from ..config import settings

router = APIRouter()

@router.post("/api/data", dependencies=[Depends(validate_api_key)])
async def receive_data(data: IoTData, db: Session = Depends(get_db)):
    """Endpoint to receive IoT data and save to the database."""
    new_entry = Monitor(temperature=data.temperature, humidity=data.humidity)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    # Check temperature threshold
    if data.temperature > settings.TEMP_THRESHOLD:
        message = (f"🚨 <b>Temperature Alert</b> 🚨\n"
                   f"Temperature: {data.temperature}°C\n"
                   f"Threshold: {settings.TEMP_THRESHOLD}°C\n"
                   f"Timestamp: {new_entry.created_at.isoformat()}")
        send_telegram_notification(message)

    return {"message": "Data saved successfully", "id": new_entry.id}
