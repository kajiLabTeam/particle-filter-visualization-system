import os
import time
from glob import glob
from typing import Sequence

from PIL import Image

from config.const.coordinate import (CORRECT_TRAJECTORY_COORDINATES1,
                                     CORRECT_TRAJECTORY_COORDINATES2,
                                     CORRECT_TRAJECTORY_COORDINATES3)
from config.const.path import (IDEAL_IMAGE_PATH, IDEAL_OUTPUT_NORMAL_PATH,
                               IDEAL_OUTPUT_REVERSED_PATH)
from domain.correct_trajectory.correct_trajectory import CorrectTrajectory
from domain.floor_map.floor_map import FloorMap
from domain.particle_floor_map.particle_floor_map import ParticleFloorMap
from domain.realtime_estimated_trajectory.realtime_estimated_trajectory import \
    RealtimeEstimatedTrajectory
from domain.reversed_estimated_trajectory.reversed_estimated_trajectory import \
    ReversedEstimatedTrajectory
from domain.tracking_particle.tracking_particle import TrackingParticle


def track_ideal(
    floor_map_path: str,
    correct_trajectory_coordinates: Sequence[Sequence[int | float]],
    output_path: str,
    output_reversed_path: str,
):
    print(f"理想 {floor_map_path} start")
    ut = time.time()

    floor_image = Image.open(floor_map_path)
    floor_map = FloorMap(floor_image)
    correct_trajectory = CorrectTrajectory(correct_trajectory_coordinates)

    # パーティクルフィルタによる追跡の実行
    tracking_particle = TrackingParticle(
        correct_trajectory=correct_trajectory,
        floor_map=floor_map,
    )
    tracking_particle.track()

    realtime_estimated_trajectory = RealtimeEstimatedTrajectory(
        tracking_particle=tracking_particle
    )

    # Gifの生成処理
    if tracking_particle.get_coverage_position() is not None:
        ParticleFloorMap.generate_realtime_gif(
            floor_map=floor_map,
            tracking_particle=tracking_particle,
            realtime_estimated_trajectory=realtime_estimated_trajectory,
            file_path=output_path,
        )

        reversed_estimated_by_cluster_trajectory = ReversedEstimatedTrajectory(
            tracking_particle=tracking_particle,
            method="particle_filter",
        )
        print(
            f"推定出発点 x: {reversed_estimated_by_cluster_trajectory[0].get_x()} y: {reversed_estimated_by_cluster_trajectory[0].get_y()} 方向: {reversed_estimated_by_cluster_trajectory[0].get_direction()}"
        )

        ParticleFloorMap.generate_reversed_gif(
            floor_map=floor_map,
            tracking_particle=tracking_particle,
            reversed_estimated_trajectory=reversed_estimated_by_cluster_trajectory,
            file_path=output_reversed_path,
        )
    else:
        ParticleFloorMap.generate_realtime_gif(
            floor_map=floor_map,
            tracking_particle=tracking_particle,
            realtime_estimated_trajectory=realtime_estimated_trajectory,
            file_path=output_path,
        )

    print(f"elapsed_time: {time.time() - ut}")


def main():
    # 理想の軌跡を生成
    ideal_file_count = len(glob(os.path.join(IDEAL_IMAGE_PATH, "*")))
    for i in range(1, ideal_file_count + 1):
        track_ideal(
            floor_map_path=f"{IDEAL_IMAGE_PATH}/floor{i}.png",
            correct_trajectory_coordinates=(
                CORRECT_TRAJECTORY_COORDINATES1
                if i == 1
                else (
                    CORRECT_TRAJECTORY_COORDINATES2
                    if i == 2
                    else CORRECT_TRAJECTORY_COORDINATES3
                )
            ),
            output_path=f"{IDEAL_OUTPUT_NORMAL_PATH}/result-{i}.gif",
            output_reversed_path=f"{IDEAL_OUTPUT_REVERSED_PATH}/reversed-result-{i}.gif",
        )


if __name__ == "__main__":
    main()
