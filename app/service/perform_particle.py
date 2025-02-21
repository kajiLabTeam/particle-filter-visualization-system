import time
from collections.abc import Sequence
from pathlib import Path

from PIL import Image

from app.config.const.coordinate import (
    CORRECT_TRAJECTORY_COORDINATES1,
    CORRECT_TRAJECTORY_COORDINATES2,
    CORRECT_TRAJECTORY_COORDINATES3,
)
from app.config.const.path import (
    IDEAL_IMAGE_PATH,
    IDEAL_OUTPUT_NORMAL_PATH,
    IDEAL_OUTPUT_REVERSED_PATH,
)
from app.domain.correct_trajectory.correct_trajectory import CorrectTrajectory
from app.domain.floor_map.floor_map import FloorMap
from app.domain.particle_floor_map.particle_floor_map import ParticleFloorMap
from app.domain.realtime_estimated_trajectory.realtime_estimated_trajectory import (
    RealtimeEstimatedTrajectory,
)
from app.domain.tracking_particle.tracking_particle import TrackingParticle


def track_ideal(
    floor_map_path: str,
    correct_trajectory_coordinates: Sequence[Sequence[int | float]],
    output_path: str,
    output_reversed_path: str,
    # hyperparameters
    initial_particle_count: int,
    particle_step_error_sd: int,
    particle_angle_error_sd: int,
    convergence_judgment_clusters_count: int,
    # settings
    #use_fingerprint: bool,
    use_clusters_color: bool,
    display_correct_trajectory: bool,
    display_estimated_trajectory: bool,
) -> None:
    print(f"理想 {floor_map_path} start")  # noqa: T201
    ut = time.time()

    # フロアマップと正解軌跡の生成
    floor_image = Image.open(floor_map_path)
    floor_map = FloorMap(floor_image)

    correct_trajectory = CorrectTrajectory(correct_trajectory_coordinates)



    # パーティクルフィルタによる追跡の実行
    # アルゴリズム説明:https://kjlb.esa.io/posts/5514

    # パーティクルフィルタにおける初期状態の作成
    particle_count = initial_particle_count  # 値を取得
    step_error_sd = particle_step_error_sd  # 値を取得
    angle_error_sd = particle_angle_error_sd  # 値を取得

    tracking_particle = TrackingParticle(
        correct_trajectory=correct_trajectory,
        floor_map=floor_map,
        # hyperparameters
        initial_particle_count=particle_count, 
        particle_step_error_sd=step_error_sd,
        particle_angle_error_sd=angle_error_sd,
        convergence_judgment_clusters_count=convergence_judgment_clusters_count,
        # settings
        #use_fingerprint=use_fingerprint,
    )
    tracking_particle.track()

    realtime_estimated_trajectory = RealtimeEstimatedTrajectory(tracking_particle=tracking_particle)

    # Gifの生成処理
    if tracking_particle.get_coverage_position() is not None:
        ParticleFloorMap.generate_realtime_gif(
            floor_map=floor_map,
            tracking_particle=tracking_particle,
            realtime_estimated_trajectory=realtime_estimated_trajectory,
            file_path=output_path,
            use_cluster_color=use_clusters_color,
            display_correct_trajectory=display_correct_trajectory,
            display_estimated_trajectory=display_estimated_trajectory,
        )


    print(f"elapsed_time: {time.time() - ut}")  # noqa: T201


def perform_particle(
    # hyperparameters
    initial_particle_count: int,
    particle_step_error_sd: int,
    particle_angle_error_sd: int,
    convergence_judgment_clusters_count: int,
    # settings
    use_map_matching: bool,
    #use_fingerprint: bool,
    use_clusters_color: bool,
    display_correct_trajectory: bool,
    display_estimated_trajectory: bool,
    use_maps_number: int,
) -> None:
    # 理想の軌跡を生成
    if(use_map_matching == True):
        track_ideal(
            floor_map_path=f"{IDEAL_IMAGE_PATH}/floor{use_maps_number}.png",
            correct_trajectory_coordinates=(
                CORRECT_TRAJECTORY_COORDINATES1
            ),
                output_path=f"{IDEAL_OUTPUT_NORMAL_PATH}/result-{use_maps_number}.gif",
                output_reversed_path=f"{IDEAL_OUTPUT_REVERSED_PATH}/reversed-result-{use_maps_number}.gif",
                # hyperparameters
                initial_particle_count=int(initial_particle_count),
                particle_step_error_sd=int(particle_step_error_sd),
                particle_angle_error_sd=int(particle_angle_error_sd),
                convergence_judgment_clusters_count=int(convergence_judgment_clusters_count),
                # settings
                #use_fingerprint=bool(use_fingerprint),
                use_clusters_color=bool(use_clusters_color),
                display_correct_trajectory=bool(display_correct_trajectory),
                display_estimated_trajectory=bool(display_estimated_trajectory)
            )
        
        # ideal_file_count = len(list(Path(IDEAL_IMAGE_PATH).glob("*")))
        # for i in range(1, ideal_file_count + 1):
        # パーティクルフィルタの実行
        # if(use_map_matching == True):
        #     track_ideal(
        #         floor_map_path=f"{IDEAL_IMAGE_PATH}/floor{i}.png",
        #         correct_trajectory_coordinates=(
        #             CORRECT_TRAJECTORY_COORDINATES1
        #             if i == 1
        #             else (
        #                 CORRECT_TRAJECTORY_COORDINATES2
        #                 if i == 2  # noqa: PLR2004
        #                 else CORRECT_TRAJECTORY_COORDINATES3
        #             )
        #         ),
        #             output_path=f"{IDEAL_OUTPUT_NORMAL_PATH}/result-{i}.gif",
        #             output_reversed_path=f"{IDEAL_OUTPUT_REVERSED_PATH}/reversed-result-{i}.gif",
        #             # hyperparameters
        #             initial_particle_count=int(initial_particle_count),
        #             particle_step_error_sd=int(particle_step_error_sd),
        #             particle_angle_error_sd=int(particle_angle_error_sd),
        #             convergence_judgment_clusters_count=int(convergence_judgment_clusters_count),
        #             # settings
        #             #use_fingerprint=bool(use_fingerprint),
        #             use_clusters_color=bool(use_clusters_color),
        #             display_correct_trajectory=bool(display_correct_trajectory),
        #             display_estimated_trajectory=bool(display_estimated_trajectory)
        #         )
        