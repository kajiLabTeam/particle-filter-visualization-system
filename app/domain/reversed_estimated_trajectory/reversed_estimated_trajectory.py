from collections.abc import Iterator
from typing import Literal

from app.domain.estimated_position.estimated_position import EstimatedPosition
from app.domain.reversed_estimated_trajectory.cluster_tracking import ClusterTracking
from app.domain.reversed_estimated_trajectory.reversed_particle_filter import (
    ReversedEstimationParticleFilter,
)
from app.domain.tracking_particle.tracking_particle import TrackingParticle


class ReversedEstimatedTrajectory:
    def __init__(
        self,
        tracking_particle: TrackingParticle,
        method: Literal["cluster", "particle_filter"],
    ) -> None:
        self.__tracking_particle = tracking_particle
        self.__reversed_estimated_trajectory: list[EstimatedPosition] = []

        if method == "cluster":
            self.__cluster_tracking()
        elif method == "particle_filter":
            self.__particle_filter()

        self.__reversed()

    def get_reversed_estimated_trajectory(self) -> list[EstimatedPosition]:
        return self.__reversed_estimated_trajectory

    def last_position(self) -> EstimatedPosition:
        return self.__reversed_estimated_trajectory[-1]

    def __cluster_tracking(self) -> None:
        self.__reversed_estimated_trajectory = ClusterTracking.run(self.__tracking_particle)

    def __particle_filter(self) -> None:
        self.__reversed_estimated_trajectory = ReversedEstimationParticleFilter.run(
            self.__tracking_particle
        )

    def __reversed(self) -> None:
        self.__reversed_estimated_trajectory.reverse()

    def __iter__(self) -> Iterator[EstimatedPosition]:
        return iter(self.__reversed_estimated_trajectory)

    def __len__(self) -> int:
        return len(self.__reversed_estimated_trajectory)

    def __getitem__(self, index: int) -> EstimatedPosition:
        return self.__reversed_estimated_trajectory[index]
