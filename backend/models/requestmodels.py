from pydantic import BaseModel, Field
from typing import Optional

class VerifyTextRequest(BaseModel):
    """Request model for text verification"""
    text: str = Field(..., min_length=1, max_length=2000)

    class Config:
        example = {
            "text": "The government announced free laptops for everyone tomorrow.",
            
        }

class VerifyVoiceRequest(BaseModel):
    """Request model for voice verification"""
    
    class Config:
        example = {
        }

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    apis_available: dict