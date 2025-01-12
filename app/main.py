from fastapi import FastAPI
from .routers import iot_data
from .database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# Include routers
app.include_router(iot_data.router)

@app.get("/")
async def root():
    return {"message": "Hello!"}
