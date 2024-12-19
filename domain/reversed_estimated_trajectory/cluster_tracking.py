from typing import List

from config.const.circle import REVERSE_RADIUS
from domain.estimated_position.estimated_position import EstimatedPosition
from domain.tracking_particle.tracking_particle import TrackingParticle


class ClusterTracking:
    @staticmethod
    def run(tracking_particle: TrackingParticle) -> List[EstimatedPosition]:
        starting_point = tracking_particle.last_estimated_position()

        reversed_estimated_positions: List[EstimatedPosition] = [
            EstimatedPosition(
                x=starting_point.get_x(),
                y=starting_point.get_y(),
                step=starting_point.get_step(),
                direction=starting_point.get_direction(),
                changed_angle=starting_point.get_changed_angle(),
            )
        ]

        tracking_particle.reverse()

        for _, estimation_particles in enumerate(tracking_particle):
            tracking_particle_collection = (
                estimation_particles.get_particles_within_radius(
                    x=reversed_estimated_positions[-1].get_x(),
                    y=reversed_estimated_positions[-1].get_y(),
                    radius=REVERSE_RADIUS,
                )
            )

            reversed_estimated_positions.append(
                tracking_particle_collection.estimate_position()
            )

        tracking_particle.reverse()

        return reversed_estimated_positions
