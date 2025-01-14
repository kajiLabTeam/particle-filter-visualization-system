from collections.abc import Iterator

from app.domain.estimated_position.estimated_position import EstimatedPosition
from app.domain.tracking_particle.tracking_particle import TrackingParticle


class RealtimeEstimatedTrajectory:
    def __init__(self, tracking_particle: TrackingParticle) -> None:
        self.__tracking_particle = tracking_particle
        self.__realtime_estimated_trajectory: list[EstimatedPosition] = []

        self.__caption()

    def get_realtime_estimated_trajectory(self) -> list[EstimatedPosition]:
        return self.__realtime_estimated_trajectory

    def __caption(self) -> None:
        """## 重みづけ平均による推定軌跡を計算する"""
        for estimation_particles in self.__tracking_particle:
            self.__realtime_estimated_trajectory.append(estimation_particles.estimate_position())

    def __iter__(self) -> Iterator[EstimatedPosition]:
        return iter(self.__realtime_estimated_trajectory)

    def __len__(self) -> int:
        return len(self.__realtime_estimated_trajectory)

    def __getitem__(self, key: int) -> EstimatedPosition:
        return self.__realtime_estimated_trajectory[key]
