from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class PerformParticleFilteringRequest(BaseModel):
    """
    Request model for the perform_particlefiltering_controller
    """
    particle_count: int
    particle_step_error_sd : int
    particle_angle_error_sd : int

router = APIRouter()

@router.post(
    "/api/walking/start",
    # response_model=StartWalkingResponse,
    status_code=201,
)

async def perform_particlefiltering_controller(
    request: PerformParticleFilteringRequest
):
    """
    Perform particle filtering
    """
    # Use the request data to perform particle filtering
    # For now, we'll just return a dummy response
    return {
        "message": "Particle filtering performed successfully",
        "particle_count": request.particle_count,
        "particle_step_error_sd": request.particle_step_error_sd,
        "particle_angle_error_sd": request.particle_angle_error_sd
    }
   