from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from fastapi.security.api_key import APIKeyHeader


# Environment variable configuration
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME", "temperature")
api_key_env = os.getenv("API_KEY", "default_api_key")

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the database model
class Monitor(Base):
    __tablename__ = "monitor"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Key security
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != api_key_env:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Request model
class IoTData(BaseModel):
    temperature: float
    humidity: float

# Receive and process 
@app.post("/api/data", dependencies=[Depends(validate_api_key)])
async def receive_data(data: IoTData, db: SessionLocal = Depends(get_db)):
    """Endpoint to receive IoT data and save to the database."""
    new_entry = Monitor(temperature=data.temperature, humidity=data.humidity)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"message": "Data saved successfully", "id": new_entry.id}

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello!"}
