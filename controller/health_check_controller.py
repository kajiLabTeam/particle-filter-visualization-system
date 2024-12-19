
# Hello world controller

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class HealthCheckResponse(BaseModel):
    """
    Response model for the health_check_controller
    """
    message: str

router = APIRouter()

@router.get(
    "/",
    response_model=HealthCheckResponse,
    status_code=200,
)
async def health_check():
    """
    Health check
    """
    return {
        "message": "I'm alive"
    }
