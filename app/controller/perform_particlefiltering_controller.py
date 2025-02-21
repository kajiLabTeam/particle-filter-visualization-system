from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.service.perform_particle import perform_particle
from app.domain.tracking_particle.tracking_particle import TrackingParticle
import io
import os
from moviepy.editor import VideoFileClip

# モジュールレベルの変数として Hyperparameters を定義
initial_particle_count = 1000 # 初期値
particle_step_error_sd = 10
particle_angle_error_sd = 10
convergence_judgment_clusters_count = 2

class Hyperparameters(BaseModel):
    initial_particle_count: int
    convergence_judgment_clusters_count: int
    particle_step_error_sd: int
    particle_angle_error_sd: int

class Settings(BaseModel):
    use_map_matching: bool
    use_fingerprint: bool
    use_clusters_color: bool
    display_correct_trajectory: bool
    display_estimated_trajectory: bool
    use_maps_number: int

class PerformParticleFilteringRequest(BaseModel):
    """
    Request model for the perform_particlefiltering_controller
    """
    hyperparameters: Hyperparameters
    settings: Settings

class PerformParticleFilteringResponse(BaseModel):
    """
    Response model for the perform_particlefiltering_controller
    """
    particle_gif: str

router = APIRouter()


@router.post(
    "/api/building/{building_id}/floors/{floor_id}/trajectries/{trajectry_id}/",
    response_model=PerformParticleFilteringResponse,
    status_code=201,
)

async def perform_particlefiltering(
    request: PerformParticleFilteringRequest
):
    
    gif_path = f"data/output/ideal/normal/result-{request.settings.use_maps_number}.gif"
    mp4_path = f"data/output/ideal/normal/result-{request.settings.use_maps_number}.mp4"

    """
    Perform particle filtering
    """
    perform_particle(
        # hyperparameters
        initial_particle_count=request.hyperparameters.initial_particle_count,
        particle_step_error_sd=request.hyperparameters.particle_step_error_sd,
        particle_angle_error_sd=request.hyperparameters.particle_angle_error_sd,
        convergence_judgment_clusters_count=request.hyperparameters.convergence_judgment_clusters_count,
        # settings
        use_map_matching=request.settings.use_map_matching,
        #use_fingerprint=request.settings.use_fingerprint,
        use_clusters_color=request.settings.use_clusters_color,
        display_correct_trajectory=request.settings.display_correct_trajectory,
        display_estimated_trajectory=request.settings.display_estimated_trajectory,
        use_maps_number=request.settings.use_maps_number,

    )

    # GIFをMP4に変換
    try:
        clip = VideoFileClip(gif_path)
        clip.write_videofile(mp4_path, codec="libx264", fps=24)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="GIF file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting GIF to MP4: {str(e)}")

    try:
        with open(mp4_path, "rb") as mp4_file:
            video_raw = mp4_file.read()
            byte_io = io.BytesIO(video_raw)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="MP4 file not found")

    # MP4ファイルをレスポンスとして返す
    return StreamingResponse(byte_io, media_type="video/mp4")

