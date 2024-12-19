from typing import List, Sequence

from domain.correct_position.correct_position import CorrectPosition


class CorrectTrajectory:
    def __init__(self, trajectory: Sequence[Sequence[int | float]]) -> None:
        if len(trajectory[0]) == 7:
            self.__correct_trajectory = [
                CorrectPosition(
                    int(x),
                    int(y),
                    int(step),
                    direction,
                    int(changed_angle),
                    rssi1,
                    rssi2,
                )
                for x, y, step, direction, changed_angle, rssi1, rssi2 in trajectory
            ]
        elif len(trajectory[0]) == 5:
            self.__correct_trajectory = [
                CorrectPosition(
                    int(x),
                    int(y),
                    int(step),
                    direction,
                    int(changed_angle),
                    0,
                    0,
                )
                for x, y, step, direction, changed_angle in trajectory
            ]

    def get_correct_trajectory(self) -> List[CorrectPosition]:
        return self.__correct_trajectory

    def reverse(self) -> List[CorrectPosition]:
        reversed_correct_positions = [
            position.reverse() for position in self.__correct_trajectory
        ]
        reversed_correct_positions.reverse()

        return reversed_correct_positions

    def __len__(self):
        return len(self.__correct_trajectory)

    def __iter__(self):
        return iter(self.__correct_trajectory)

    def __getitem__(self, index):
        return self.__correct_trajectory[index]
