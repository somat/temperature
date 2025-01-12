from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from .database import Base

class Monitor(Base):
    __tablename__ = "monitor"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
