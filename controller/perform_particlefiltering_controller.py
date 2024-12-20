from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.perform_particle import perform_particle 

# モジュールレベルの変数として particle_count を定義
initial_particle_count = 1000 # 初期値
particle_step_error_sd = 10
particle_angle_error_sd = 10

class PerformParticleFilteringRequest(BaseModel):
    """
    Request model for the perform_particlefiltering_controller
    """
    initial_particle_count: int
    particle_step_error_sd : int
    particle_angle_error_sd : int

router = APIRouter()


@router.post(
    "/api/building/{building_id}/floors/{floor_id}/trajectries/{trajectry_id}/",
    response_model=PerformParticleFilteringRequest,
    status_code=201,
)


async def perform_particlefiltering(
    request: PerformParticleFilteringRequest
):
    """
    Perform particle filtering
    """
    perform_particle(
        request.initial_particle_count,
        request.particle_step_error_sd,
        request.particle_angle_error_sd
    )
    
    # Use the request data to perform particle filtering
    # For now, we'll just return a dummy response
    return {
    "message": "Particle filtering performed successfully",
    "initial_particle_count": request.initial_particle_count,
    "particle_step_error_sd": request.particle_step_error_sd,
    "particle_angle_error_sd": request.particle_angle_error_sd
    }
