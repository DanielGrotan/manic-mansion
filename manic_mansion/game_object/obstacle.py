from pygame import Rect

from ..constants import COLORS
from ..custom_types import RectPosition
from .game_object import GameObject


class Obstacle(GameObject):
    __COLOR = COLORS["brown"]

    def __init__(
        self,
        bounding_rect: Rect,
        x: int,
        y: int,
        size: int,
        rect_position: RectPosition = "topleft",
    ) -> None:
        super().__init__(bounding_rect, x, y, size, size, self.__COLOR, rect_position)
