class EstimatedPosition:
    def __init__(
        self, x: int, y: int, step: int, direction: float, changed_angle: int
    ) -> None:
        self.__x = x
        self.__y = y
        self.__step = step
        self.__direction = direction
        self.__changed_angle = changed_angle

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
