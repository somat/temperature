from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from .config import settings

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

def validate_api_key(api_key: str = Depends(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
