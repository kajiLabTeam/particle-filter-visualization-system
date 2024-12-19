from typing import List, Tuple

from PIL.Image import Image

from config.const.color import (CANDIDATE_PARTICLES_COLOR,
                                CORRECT_CURRENT_POSITION_COLOR,
                                CORRECT_TRAJECTORY_COLOR, OUTLINE_COLOR,
                                PARTICLE_OUTLINE_COLOR,
                                REALTIME_ESTIMATED__CURRENT_POSITION_COLOR,
                                REALTIME_ESTIMATED_TRAJECTORY_COLOR,
                                REVERSE_CURRENT_ESTIMATED_POSITION_COLOR,
                                REVERSE_ESTIMATED_TRAJECTORY_COLOR)
from domain.correct_trajectory.correct_trajectory import CorrectTrajectory
from domain.estimated_particle.estimated_particle import EstimatedParticle
from domain.floor_map.floor_map import FloorMap
from domain.realtime_estimated_trajectory.realtime_estimated_trajectory import \
    RealtimeEstimatedTrajectory
from domain.reversed_estimated_trajectory.reversed_estimated_trajectory import \
    ReversedEstimatedTrajectory
from domain.tracking_particle.tracking_particle import TrackingParticle


class ParticleFloorMap:
    @staticmethod
    def generate_reversed_gif(
        floor_map: FloorMap,
        tracking_particle: TrackingParticle,
        reversed_estimated_trajectory: ReversedEstimatedTrajectory,
        file_path: str,
    ):
        """
        ## 推定されたパーティクルの軌跡をGIFアニメーションとして生成する
        """
        images_cluster: List[Image] = []

        for i, estimation_particles in enumerate(tracking_particle):
            floor_map_copy = floor_map.clone()

            # パーティクルの位置を描画
            for particle in estimation_particles:
                floor_map_copy.depict_circle(
                    position=(particle.get_x(), particle.get_y()),
                    color=CANDIDATE_PARTICLES_COLOR,
                    outline_color=PARTICLE_OUTLINE_COLOR,
                )

            # 正解軌跡を描画
            ParticleFloorMap.__drawing_trajectory(
                floor_map=floor_map_copy,
                current_position=(
                    estimation_particles.get_current_position().get_x(),
                    estimation_particles.get_current_position().get_y(),
                ),
                current_color=CORRECT_CURRENT_POSITION_COLOR,
                trajectory=tracking_particle.get_correct_trajectory(),
                trajectory_color=CORRECT_TRAJECTORY_COLOR,
            )

            # 逆推定軌跡を描画
            ParticleFloorMap.__drawing_trajectory(
                floor_map=floor_map_copy,
                current_position=(
                    reversed_estimated_trajectory[i].get_x(),
                    reversed_estimated_trajectory[i].get_y(),
                ),
                current_color=REVERSE_CURRENT_ESTIMATED_POSITION_COLOR,
                trajectory=reversed_estimated_trajectory,
                trajectory_color=REVERSE_ESTIMATED_TRAJECTORY_COLOR,
            )

            images_cluster.append(floor_map_copy.get_floor_map().copy())

        images_cluster[0].save(
            file_path,
            save_all=True,
            append_images=images_cluster[1:],
            duration=100,
            loop=0,
        )

        print(f"Generated GIF: {file_path}")

    @staticmethod
    def generate_realtime_gif(
        floor_map: FloorMap,
        tracking_particle: TrackingParticle,
        realtime_estimated_trajectory: RealtimeEstimatedTrajectory,
        file_path: str,
    ):
        """
        ## 推定されたパーティクルの軌跡をGIFアニメーションとして生成する
        """
        images_cluster: List[Image] = []

        for i, estimation_particles in enumerate(tracking_particle):
            floor_map_copy = floor_map.clone()

            # パーティクルの位置を描画
            for particle in estimation_particles:
                floor_map_copy.depict_circle(
                    position=(particle.get_x(), particle.get_y()),
                    color=CANDIDATE_PARTICLES_COLOR,
                    outline_color=PARTICLE_OUTLINE_COLOR,
                )

            # 正解軌跡を描画
            ParticleFloorMap.__drawing_trajectory(
                floor_map=floor_map_copy,
                current_position=(
                    estimation_particles.get_current_position().get_x(),
                    estimation_particles.get_current_position().get_y(),
                ),
                current_color=CORRECT_CURRENT_POSITION_COLOR,
                trajectory=tracking_particle.get_correct_trajectory(),
                trajectory_color=CORRECT_TRAJECTORY_COLOR,
            )

            # リアルタイム推定軌跡を描画
            ParticleFloorMap.__drawing_trajectory(
                floor_map=floor_map_copy,
                current_position=(
                    realtime_estimated_trajectory[i].get_x(),
                    realtime_estimated_trajectory[i].get_y(),
                ),
                current_color=REALTIME_ESTIMATED__CURRENT_POSITION_COLOR,
                trajectory=realtime_estimated_trajectory,
                trajectory_color=REALTIME_ESTIMATED_TRAJECTORY_COLOR,
            )

            images_cluster.append(floor_map_copy.get_floor_map().copy())

        images_cluster[0].save(
            file_path,
            save_all=True,
            append_images=images_cluster[1:],
            duration=100,
            loop=0,
        )

        print(f"Generated GIF: {file_path}")

    @staticmethod
    def __drawing_trajectory(
        floor_map: FloorMap,
        current_position: Tuple[int, int],
        current_color: Tuple[int, int, int, int],
        trajectory: (
            EstimatedParticle
            | CorrectTrajectory
            | RealtimeEstimatedTrajectory
            | ReversedEstimatedTrajectory
        ),
        trajectory_color: Tuple[int, int, int, int],
    ):
        for position_sample in trajectory:
            floor_map.depict_circle(
                position=(position_sample.get_x(), position_sample.get_y()),
                color=trajectory_color,
                outline_color=OUTLINE_COLOR,
            )
        floor_map.depict_rectangle(position=current_position, color=current_color)
