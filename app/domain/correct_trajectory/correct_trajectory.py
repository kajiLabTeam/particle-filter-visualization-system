from collections.abc import Iterator, Sequence

from app.domain.correct_position.correct_position import CorrectPosition


class CorrectTrajectory:
    def __init__(self, trajectory: Sequence[Sequence[int | float]]) -> None:
        if not trajectory:  # 空リストを考慮
            self.__correct_trajectory = []
            return

        if len(trajectory[0]) == 7:  # noqa: PLR2004
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
        elif len(trajectory[0]) == 5:  # noqa: PLR2004
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

    def get_correct_trajectory(self) -> list[CorrectPosition]:
        return self.__correct_trajectory

    def reverse(self) -> list[CorrectPosition]:
        reversed_correct_positions = [position.reverse() for position in self.__correct_trajectory]
        reversed_correct_positions.reverse()

        return reversed_correct_positions

    def __len__(self) -> int:
        return len(self.__correct_trajectory)

    def __iter__(self) -> Iterator[CorrectPosition]:
        return iter(self.__correct_trajectory)

    def __getitem__(self, index: int) -> CorrectPosition:
        return self.__correct_trajectory[index]
