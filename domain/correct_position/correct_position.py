from utils.angle import reverse_angle, turn_angle


class CorrectPosition:
    def __init__(
        self,
        x: int,
        y: int,
        step: int,
        direction: float,
        changed_angle: int,
        rssi1: float,
        rssi2: float,
    ) -> None:
        self.__x = x
        self.__y = y
        self.__step = step
        self.__direction = direction
        self.__changed_angle = changed_angle
        self.__rssi1 = rssi1
        self.__rssi2 = rssi2

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_step(self) -> int:
        return self.__step

    def get_direction(self) -> float:
        return self.__direction

    def get_changed_angle(self) -> int:
        return self.__changed_angle

    def get_rssi1(self) -> float:
        return self.__rssi1

    def get_rssi2(self) -> float:
        return self.__rssi2

    def reverse(self) -> "CorrectPosition":
        return CorrectPosition(
            x=self.__x,
            y=self.__y,
            step=self.__step,
            direction=reverse_angle(self.__direction),
            changed_angle=turn_angle(self.__changed_angle),
            rssi1=self.__rssi1,
            rssi2=self.__rssi2,
        )
