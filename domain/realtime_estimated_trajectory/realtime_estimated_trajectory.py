from typing import List

from domain.estimated_position.estimated_position import EstimatedPosition
from domain.tracking_particle.tracking_particle import TrackingParticle


class RealtimeEstimatedTrajectory:
    def __init__(self, tracking_particle: TrackingParticle) -> None:
        self.__tracking_particle = tracking_particle
        self.__realtime_estimated_trajectory: List[EstimatedPosition] = []

        self.__caption()

    def get_realtime_estimated_trajectory(self) -> List[EstimatedPosition]:
        return self.__realtime_estimated_trajectory

    def __caption(self):
        """
        ## 重みづけ平均による推定軌跡を計算する
        """
        for estimation_particles in self.__tracking_particle:
            self.__realtime_estimated_trajectory.append(
                estimation_particles.estimate_position()
            )

    def __iter__(self):
        return iter(self.__realtime_estimated_trajectory)

    def __len__(self):
        return len(self.__realtime_estimated_trajectory)

    def __getitem__(self, key):
        return self.__realtime_estimated_trajectory[key]
