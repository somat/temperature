from pydantic import BaseModel

class IoTData(BaseModel):
    temperature: float
    humidity: float
