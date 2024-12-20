from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from service.perform_particle import perform_particle
import io
import os
from moviepy import VideoFileClip

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
    gif_path = "data/output/ideal/normal/result-1.gif"
    mp4_path = "data/output/ideal/normal/result-1.mp4"

    """
    Perform particle filtering
    """
    perform_particle(
        request.initial_particle_count,
        request.particle_step_error_sd,
        request.particle_angle_error_sd
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

