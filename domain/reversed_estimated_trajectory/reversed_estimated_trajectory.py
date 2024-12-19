from typing import List, Literal

from domain.estimated_position.estimated_position import EstimatedPosition
from domain.reversed_estimated_trajectory.cluster_tracking import \
    ClusterTracking
from domain.reversed_estimated_trajectory.reversed_particle_filter import \
    ReversedEstimationParticleFilter
from domain.tracking_particle.tracking_particle import TrackingParticle


class ReversedEstimatedTrajectory:
    def __init__(
        self,
        tracking_particle: TrackingParticle,
        method: Literal["cluster", "particle_filter"],
    ) -> None:
        self.__tracking_particle = tracking_particle
        self.__reversed_estimated_trajectory: List[EstimatedPosition] = []

        if method == "cluster":
            self.__cluster_tracking()
        elif method == "particle_filter":
            self.__particle_filter()

        self.__reversed()

    def get_reversed_estimated_trajectory(self) -> List[EstimatedPosition]:
        return self.__reversed_estimated_trajectory

    def last_position(self) -> EstimatedPosition:
        return self.__reversed_estimated_trajectory[-1]

    def __cluster_tracking(self):
        self.__reversed_estimated_trajectory = ClusterTracking.run(
            self.__tracking_particle
        )

    def __particle_filter(self):
        self.__reversed_estimated_trajectory = ReversedEstimationParticleFilter.run(
            self.__tracking_particle
        )

    def __reversed(self):
        self.__reversed_estimated_trajectory.reverse()

    def __iter__(self):
        return iter(self.__reversed_estimated_trajectory)

    def __len__(self):
        return len(self.__reversed_estimated_trajectory)

    def __getitem__(self, index):
        return self.__reversed_estimated_trajectory[index]
