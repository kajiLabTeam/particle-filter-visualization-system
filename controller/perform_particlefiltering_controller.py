from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# モジュールレベルの変数として particle_count を定義
particle_count = 1000 # 初期値

class PerformParticleFilteringRequest(BaseModel):
    """
    Request model for the perform_particlefiltering_controller
    """
    particle_count: int
    particle_step_error_sd : int
    particle_angle_error_sd : int

router = APIRouter()


@router.post(
    "/api/building/{building_id}/floors/{floor_id}/trajectries/{trajectry_id}/",
    response_model=PerformParticleFilteringRequest,
    status_code=201,
)

def get_particle_count() -> int:
    """
    現在の particle_count を取得する関数
    """
    return particle_count

def set_particle_count(value: int):
    """
    particle_count を更新する関数
    """
    global particle_count
    particle_count = value

async def perform_particlefiltering(
    request: PerformParticleFilteringRequest
):
    """
    Perform particle filtering
    """
    # Use the request data to perform particle filtering
    # For now, we'll just return a dummy response
    set_particle_count(1010)
    return {
    "message": "Particle filtering performed successfully",
    "particle_count": 1010,
    "particle_step_error_sd": 10,
    "particle_angle_error_sd": 10
    }
