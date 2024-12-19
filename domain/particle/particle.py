import math
import random
from typing import Callable, Tuple

from config.const.error import PARTICLES_ANGLE_ERROR


class Particle:
    def __init__(
        self,
        x: int,
        y: int,
        weight: float,
        direction: float,
    ):
        self.__x = x
        self.__y = y
        self.__weight = weight
        self.__direction = direction

    @classmethod
    def create_random_particle(cls, x_range: int, y_range: int) -> "Particle":
        """
        ## ランダムなパーティクルを生成する
        """
        x = random.randint(0, x_range)
        y = random.randint(0, y_range)
        direction = random.randint(0, 359)

        return Particle(x=x, y=y, weight=1.0, direction=direction)

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    def get_direction(self) -> float:
        return self.__direction

    def get_color(self) -> Tuple[int, int, int, int]:
        return self.__color

    def get_weight(self) -> float:
        return self.__weight

    def set_weight(self, weight: float):
        self.__weight = weight

    def set_color(self, color: Tuple[int, int, int, int]):
        self.__color = color

    def new(self, weight: float, step: int, direction_error: float) -> "Particle":
        """
        ## 指定されたパーティクルの座標と角度を元に新しいパーティクルを生成する
        """
        if step < 0:
            new_x = int(self.__x + random.randint(step, -step))
            new_y = int(self.__y + random.randint(step, -step))
        else:
            new_x = int(self.__x + random.randint(-step, step))
            new_y = int(self.__y + random.randint(-step, step))
        new_direction = self.__direction + direction_error

        return Particle(
            x=new_x,
            y=new_y,
            direction=new_direction,
            weight=weight,
        )

    def move(
        self, changed_angle: float, step: int, step_error: int, angle_error: int
    ) -> "Particle":
        # 方向を変更
        move_direction = self.__direction + changed_angle + angle_error
        move_direction %= 360  # 0-359度に正規化

        # ステップとステップエラーを加算
        step_total = step + step_error

        # 角度をラジアンに変換
        radian = math.radians(move_direction)

        # 移動量を計算
        move_x = int(self.__x + step_total * math.cos(radian))
        move_y = int(self.__y + step_total * math.sin(radian))

        return Particle(
            x=move_x, y=move_y, direction=move_direction, weight=self.__weight
        )

    def is_straight_direction_to_wall(
        self, step: int, is_inside_floor: Callable[[int, int], bool]
    ) -> bool:
        """
        ## パーティクルの歩幅以内に壁に向いているかを判定する
        """
        radian = math.radians(self.__direction)

        for i in range(1, step + 1):
            move_x = int(self.__x + i * math.cos(radian))
            move_y = int(self.__y + i * math.sin(radian))

            if not is_inside_floor(move_x, move_y):
                return True

        return False

    def is_turn_direction_to_wall(
        self, step: int, is_inside_floor: Callable[[int, int], bool]
    ) -> bool:
        """
        ## 90度回転したパーティクルが壁に埋まっているかを判定する
        """
        plus_turn_move_particle = self.move(
            changed_angle=90,
            step=step,
            step_error=0,
            angle_error=PARTICLES_ANGLE_ERROR(),
        )
        minus_turn_move_particle = self.move(
            step=step,
            changed_angle=-90,
            step_error=0,
            angle_error=PARTICLES_ANGLE_ERROR(),
        )

        return not is_inside_floor(
            plus_turn_move_particle.get_x(), plus_turn_move_particle.get_y()
        ) and not is_inside_floor(
            minus_turn_move_particle.get_x(), minus_turn_move_particle.get_y()
        )

    def is_inside_circle(self, circle_center: Tuple[int, int], radius: int) -> bool:
        """
        ## 指定された座標が円の中にあるかどうかを判定する。
        """
        cx, cy = circle_center
        px, py = self.__x, self.__y

        # 円の中心と点との距離を計算
        distance = math.sqrt((px - cx) * (px - cx) + (py - cy) * (py - cy))

        # 距離が半径以下であれば円の中にある
        return distance <= radius
