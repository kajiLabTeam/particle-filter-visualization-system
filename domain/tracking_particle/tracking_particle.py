from typing import List, Optional, Tuple

from config.const.amount import CONVERGENCE_JUDGEMENT_NUMBER
from domain.correct_position.correct_position import CorrectPosition
from domain.correct_trajectory.correct_trajectory import CorrectTrajectory
from domain.estimated_particle.estimated_particle import (
    EstimatedParticle, EstimatedParticleFactory)
from domain.estimated_position.estimated_position import EstimatedPosition
from domain.floor_map.floor_map import FloorMap
from utils.angle import reverse_angle


class TrackingParticle:
    def __init__(
        self,
        floor_map: FloorMap,
        correct_trajectory: CorrectTrajectory,
        initial_particle_count: int
        # model_path: str = RSSI_MODEL_PATH,
    ) -> None:
        self.__coverage_count = 0
        self.initial_particle_count = initial_particle_count
        self.__correct_trajectory = correct_trajectory
        # self.__likelihood = Likelihood(mode_path=model_path)
        self.__estimation_particles: List[EstimatedParticle] = [
            EstimatedParticleFactory().create(
                floor_map=floor_map,
                initial_position=correct_trajectory.get_correct_trajectory()[0],
                initial_particle_count = initial_particle_count
            )
        ]
        self.__coverage_position: Optional[EstimatedPosition] = None

    def get_estimation_particles(self) -> List[EstimatedParticle]:
        return self.__estimation_particles

    def get_correct_trajectory(self) -> CorrectTrajectory:
        return self.__correct_trajectory

    def get_correct_trajectory_reverse(self, index: int) -> List[CorrectPosition]:
        correct_positions = [
            pos.reverse()
            for pos in self.__correct_trajectory.get_correct_trajectory()[:index]
        ]
        correct_positions.reverse()
        return correct_positions

    def get_coverage_position(self) -> Optional[Tuple[EstimatedPosition, int]]:
        """
        ## 収束地点を取得する
        """
        if self.__coverage_position is None:
            return None

        return (
            EstimatedPosition(
                x=self.__coverage_position.get_x(),
                y=self.__coverage_position.get_y(),
                step=self.__coverage_position.get_step(),
                direction=reverse_angle(self.__coverage_position.get_direction()),
                changed_angle=self.__coverage_position.get_changed_angle(),
            ),
            self.__coverage_count,
        )

    def set_estimation_particles(
        self, estimation_particles: List[EstimatedParticle]
    ) -> None:
        self.__estimation_particles = estimation_particles

    def last_estimation_particles(self) -> EstimatedParticle:
        return self.__estimation_particles[-1]

    def last_estimated_position(self) -> EstimatedPosition:
        return self.last_estimation_particles().estimate_position()

    def reverse(self) -> None:
        self.__estimation_particles.reverse()

    def add(self, estimation_particles: EstimatedParticle) -> None:
        self.__estimation_particles.append(estimation_particles)

    def track(self):
        """
        ## パーティクルフィルタによるトラッキングを実行する
        """
        for i, position_sample in enumerate(self.__correct_trajectory):
            estimation_particles = self.last_estimation_particles()
            estimation_particles.remove_by_floor_map()
            move_estimation_particles = estimation_particles.move(
                current_position=position_sample
            )
            move_estimation_particles.remove_by_floor_map()
            move_estimation_particles.remove_by_direction(
                step=position_sample.get_step()
            )
            move_estimation_particles.resampling(
                step=position_sample.get_step(), mode="reversed"
            )

            if i % 10 == 0:
                # move_estimation_particles.update_weight(
                #     likelihood=self.__likelihood, rssi=position_sample.get_rssi1()
                # )
                move_estimation_particles.resampling_by_weight()

            if (
                self.__coverage_position is None
                and i != 0
                and i % CONVERGENCE_JUDGEMENT_NUMBER == 0
                and estimation_particles.is_converged()
            ):
                print("収束しました")
                print(f"Initial particle count: {self.initial_particle_count}")
                print(i)
                estimation_particles = estimation_particles
                self.__coverage_count = i
                self.__coverage_position = move_estimation_particles.estimate_position()

            self.add(move_estimation_particles)

    def __iter__(self):
        return iter(self.__estimation_particles)

    def __len__(self):
        return len(self.__estimation_particles)

    def __getitem__(self, index: int):
        return self.__estimation_particles[index]
