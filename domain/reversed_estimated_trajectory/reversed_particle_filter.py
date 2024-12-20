from typing import List

from domain.estimated_particle.estimated_particle import (
    EstimatedParticle, EstimatedParticleFactory)
from domain.estimated_position.estimated_position import EstimatedPosition
from domain.tracking_particle.tracking_particle import TrackingParticle


class ReversedEstimationParticleFilter:
    @staticmethod
    def run(tracking_particle: TrackingParticle) -> List[EstimatedPosition]:
        starting_point, coverage_count = tracking_particle.get_coverage_position()

        print(
            "逆推定開始点",
            "x:",
            starting_point.get_x(),
            "y:",
            starting_point.get_y(),
            "方向:",
            starting_point.get_direction(),
            "収束回数:",
            coverage_count,
        )

        reversed_estimated_positions: List[EstimatedPosition] = [
            EstimatedPosition(
                x=starting_point.get_x(),
                y=starting_point.get_y(),
                step=starting_point.get_step(),
                direction=starting_point.get_direction(),
                changed_angle=starting_point.get_changed_angle(),
            )
        ]
        reversed_estimation_particles: List[EstimatedParticle] = [
            EstimatedParticleFactory().reverse_create(
                floor_map=tracking_particle.last_estimation_particles().get_floor_map(),
                final_position=starting_point,
            )
        ]

        reversed_correct_trajectory = tracking_particle.get_correct_trajectory_reverse(
            index=coverage_count
        )

        for _, reversed_position_sample in enumerate(reversed_correct_trajectory):
            estimation_particles = reversed_estimation_particles[-1]
            estimation_particles.remove_by_floor_map()
            move_estimation_particles = estimation_particles.move(
                current_position=reversed_position_sample
                
            )

            estimation_particles.remove_by_floor_map()
            estimation_particles.remove_by_direction(
                step=reversed_position_sample.get_step()
            )
            # estimation_particles.update_weight()
            move_estimation_particles.resampling(
                step=reversed_position_sample.get_step(), mode="reversed"
            )

            reversed_estimation_particles.append(move_estimation_particles)
            reversed_estimated_positions.append(
                move_estimation_particles.estimate_position()
            )

        tracking_particle.set_estimation_particles(reversed_estimation_particles)

        return reversed_estimated_positions
