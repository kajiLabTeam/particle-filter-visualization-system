import random
from typing import List, Tuple

import numpy as np

from domain.likelihood.likelihood import Likelihood
from domain.particle.particle import Particle


class ParticleCollection:
    def __init__(self):
        self.__particles: List[Particle] = []

    def get_particles(self) -> List[Particle]:
        return self.__particles

    def clone(self) -> "ParticleCollection":
        clone = ParticleCollection()
        clone.add_all(self.__particles)
        return clone

    def get_weights(self) -> List[float]:
        return [particle.get_weight() for particle in self.__particles]

    def get_x_mean(self) -> int:
        return int(np.mean(self.__get_x_list()))

    def get_y_mean(self) -> int:
        return int(np.mean(self.__get_y_list()))

    def get_direction_mean(self) -> int:
        radians = np.radians(self.__get_direction_list())

        x = np.mean(np.cos(radians))
        y = np.mean(np.sin(radians))

        average_angle = np.degrees(np.arctan2(y, x))

        return int((average_angle + 360) % 360)

    def get_normalized_distances(self) -> List[float]:
        distances_x = np.abs(np.array(self.__get_x_list()) - self.get_x_mean())
        distances_y = np.abs(np.array(self.__get_y_list()) - self.get_y_mean())
        distances = np.sqrt(distances_x**2 + distances_y**2)

        weights = list(1 / (1 + distances / (self.__get_x_std() + self.__get_y_std())))

        return weights / np.sum(weights)

    def get_decentralization(self) -> float:
        distances_to_mean = np.sqrt(
            (np.array(self.__get_weighted_x_list()) - self.__get_weighted_x_mean()) ** 2
            + (np.array(self.__get_weighted_y_list()) - self.__get_weighted_y_mean())
            ** 2
        )

        return float(np.mean(distances_to_mean))

    def get_residuals_mean_and_std(
        self, estimated_x: int, estimated_y: int
    ) -> Tuple[float, float]:
        residuals = np.abs(
            np.array(self.__get_weighted_x_list()) - estimated_x
        ) + np.abs(np.array(self.__get_weighted_y_list()) - estimated_y)

        return float(np.mean(residuals)), float(np.std(residuals))

    def get_weighted_x_mean(self) -> float:
        return sum(self.__get_weighted_x_list()) // sum(
            [particle.get_weight() for particle in self.__particles]
        )

    def get_weighted_y_mean(self) -> float:
        return sum(self.__get_weighted_y_list()) // sum(
            [particle.get_weight() for particle in self.__particles]
        )

    def get_weighted_direction_mean(self) -> float:
        return sum(
            [
                particle.get_direction() * particle.get_weight()
                for particle in self.__particles
            ]
        ) // sum([particle.get_weight() for particle in self.__particles])

    def add(self, particle: Particle):
        self.__particles.append(particle)

    def add_all(self, particles: List[Particle]):
        self.__particles.extend(particles)

    def reset(self):
        self.__particles = []

    def set_color_by_coordinate(self, x: int, y: int, color: Tuple[int, int, int, int]):
        for particle in self.__particles:
            if particle.get_x() == x and particle.get_y() == y:
                particle.set_color(color=color)
                break

    def set_weights(self, rssi_input: float, likelihood: Likelihood):
        for particle in self.__particles:
            particle.set_weight(
                weight=likelihood.get_likelihood(particle=particle, rssi=rssi_input)
            )

    def shuffle(self):
        random.shuffle(self.__particles)

    def pop(self, index: int):
        self.__particles.pop(index)

    def pop_all(self, indexes: List[int]):
        indexes.sort(reverse=True)

        for index in indexes:
            del self.__particles[index]

    def pop_random(self, amount: int):
        indexes = random.sample(range(len(self.__particles)), amount)
        self.pop_all(indexes)

    def __get_x_list(self) -> List[int]:
        return [particle.get_x() for particle in self.__particles]

    def __get_y_list(self) -> List[int]:
        return [particle.get_y() for particle in self.__particles]

    def __get_direction_list(self) -> List[float]:
        return [particle.get_direction() for particle in self.__particles]

    def __get_weighted_x_list(self) -> List[float]:
        return [
            particle.get_x() * particle.get_weight() for particle in self.__particles
        ]

    def __get_weighted_y_list(self) -> List[float]:
        return [
            particle.get_y() * particle.get_weight() for particle in self.__particles
        ]

    def __get_weighted_x_mean(self) -> int:
        return int(np.mean(self.__get_weighted_x_list()))

    def __get_weighted_y_mean(self) -> int:
        return int(np.mean(self.__get_weighted_y_list()))

    def __get_x_std(self) -> float:
        return float(np.std(self.__get_x_list()))

    def __get_y_std(self) -> float:
        return float(np.std(self.__get_y_list()))

    def __iter__(self):
        return iter(self.__particles)

    def __len__(self):
        return len(self.__particles)

    def __getitem__(self, index: int):
        return self.__particles[index]
