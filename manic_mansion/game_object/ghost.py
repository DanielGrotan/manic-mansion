import random

from pygame import Rect, Vector2
from pygame.key import ScancodeWrapper

from ..constants import COLORS, GHOST_MAX_SPEED
from ..custom_types import RectPosition
from .game_object import GameObject


class Ghost(GameObject):
    __COLOR = COLORS["grey"]
    __MAX_SPEED = GHOST_MAX_SPEED

    def __init__(
        self,
        bounding_rect: Rect,
        x: int,
        y: int,
        size: int,
        rect_position: RectPosition = "topleft",
    ) -> None:
        super().__init__(bounding_rect, x, y, size, size, self.__COLOR, rect_position)

        self.velocity = Vector2(
            self.__MAX_SPEED * random.choice([-1, 1]),
            self.__MAX_SPEED * random.choice([-1, 1]),
        )

    def update(self, keys_pressed: ScancodeWrapper, delta_time: float) -> None:
        self.rect.move_ip(self.velocity * delta_time)

        if (
            self.rect.top < self.bounding_rect.top
            or self.rect.bottom > self.bounding_rect.bottom
        ):
            self.velocity.y *= -1

        if (
            self.rect.left < self.bounding_rect.left
            or self.rect.right > self.bounding_rect.right
        ):
            self.velocity.x *= -1

        self.rect.clamp_ip(self.bounding_rect)
