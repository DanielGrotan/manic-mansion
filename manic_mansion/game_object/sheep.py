from pygame import Rect

from ..constants import COLORS
from ..custom_types import RectPosition
from .game_object import GameObject


class Sheep(GameObject):
    __COLOR = COLORS["pink"]

    def __init__(
        self,
        bounding_rect: Rect,
        x: int,
        y: int,
        size: int,
        rect_position: RectPosition = "topleft",
    ) -> None:
        super().__init__(bounding_rect, x, y, size, size, self.__COLOR, rect_position)

        self._has_been_moved = False

    def set_position(
        self, position: tuple[int, int], rect_position: RectPosition
    ) -> None:
        setattr(self.rect, rect_position, position)

    @property
    def has_been_moved(self) -> bool:
        return self._has_been_moved

    def drop(self) -> None:
        self._has_been_moved = True
