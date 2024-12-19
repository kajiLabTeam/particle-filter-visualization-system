import math
from typing import Tuple

from PIL import ImageDraw
from PIL.Image import Image as ImageType

from config.const.amount import PEDESTRIAN_SIZE
from config.const.color import INSIDE_PARTICLE_COLOR


class FloorMap:
    def __init__(self, floor_map_image: ImageType) -> None:
        self.__floor_map = floor_map_image
        self.__draw = ImageDraw.Draw(self.__floor_map)
        self.__map_width, self.__map_height = self.__floor_map.size

    def get_floor_map(self) -> ImageType:
        return self.__floor_map

    def get_map_width(self) -> int:
        return self.__map_width

    def get_map_height(self) -> int:
        return self.__map_height

    def clone(self) -> "FloorMap":
        return FloorMap(self.__floor_map.copy())

    def depict(
        self, position: Tuple[int, int], color: Tuple[int, int, int, int]
    ) -> None:
        """
        ## 指定した座標位置を描画する
        """
        try:
            x, y = position
            self.__floor_map.putpixel((x, y), color)
        except Exception:
            pass

    def depict_circle(
        self,
        position: Tuple[int, int],
        color: Tuple[int, int, int, int],
        outline_color: Tuple[int, int, int, int],
    ) -> None:
        """
        ## 指定した座標位置を中心とする円を描画する
        """
        try:
            x, y = position
            self.__draw.ellipse(
                (
                    x - PEDESTRIAN_SIZE,
                    y - PEDESTRIAN_SIZE,
                    x + PEDESTRIAN_SIZE,
                    y + PEDESTRIAN_SIZE,
                ),
                fill=color,
                outline=outline_color,
            )
        except Exception:
            pass

    def depict_rectangle(
        self, position: Tuple[int, int], color: Tuple[int, int, int, int]
    ) -> None:
        """
        ## 指定した座標位置を中心とする四角形を描画する
        """
        try:
            x, y = position
            self.__draw.rectangle(
                (
                    x - PEDESTRIAN_SIZE,
                    y - PEDESTRIAN_SIZE,
                    x + PEDESTRIAN_SIZE,
                    y + PEDESTRIAN_SIZE,
                ),
                fill=color,
            )
        except Exception:
            pass

    def depict_cross(self, x: int, y: int, color: Tuple[int, int, int, int]) -> None:
        """
        ## 指定した座標位置を十字形に描画する
        """
        self.__floor_map.putpixel((x, y), color)
        self.__floor_map.putpixel((x + 1, y), color)
        self.__floor_map.putpixel((x - 1, y), color)
        self.__floor_map.putpixel((x, y + 1), color)
        self.__floor_map.putpixel((x, y - 1), color)

    def depict_correct_trajectory(self, x: int, y: int) -> None:
        """
        ## 正解軌跡を描画する
        """
        for i in range(-PEDESTRIAN_SIZE, PEDESTRIAN_SIZE):
            for j in range(-PEDESTRIAN_SIZE, PEDESTRIAN_SIZE):
                self.depict((x + i, y + j), color=INSIDE_PARTICLE_COLOR)

    def is_inside_floor(self, x: int, y: int) -> bool:
        """
        ## 指定した座標が歩行可能領域内に存在するかどうかを判定する
        """
        if 0 <= x < self.__map_width and 0 <= y < self.__map_height:
            if self.__floor_map.getpixel((x, y)) == INSIDE_PARTICLE_COLOR:
                return True

        return False

    def get_nearest_inside_coordinate(
        self, outside_position: Tuple[int, int], search_range: int
    ) -> Tuple[int, int]:
        """
        ## 指定した座標から最も近い歩行可能領域内の座標を取得する
        """
        # すでに歩行可能領域内に存在する場合は引数をそのまま返す
        for x, y in [outside_position]:
            if self.is_inside_floor(x, y):
                return x, y

            for radius in range(1, search_range):
                for angle in range(0, 360, 10):
                    estimated_x = int(x + radius * math.cos(math.radians(angle)))
                    estimated_y = int(y + radius * math.sin(math.radians(angle)))

                    if self.is_inside_floor(x=estimated_x, y=estimated_y):
                        return estimated_x, estimated_y

        return outside_position
