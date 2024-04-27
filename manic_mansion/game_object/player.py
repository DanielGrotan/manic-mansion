import pygame
from pygame import Rect
from pygame.key import ScancodeWrapper

from ..constants import COLORS, PLAYER_ENCUMBERED_SPEED, PLAYER_SPEED
from ..custom_types import RectPosition
from .game_object import GameObject
from .sheep import Sheep


class Player(GameObject):
    __COLOR = COLORS["blue"]
    __SPEED = PLAYER_SPEED
    __ENCUMBERED_SPEED = PLAYER_ENCUMBERED_SPEED

    def __init__(
        self,
        bounding_rect: Rect,
        x: int,
        y: int,
        size: int,
        rect_position: RectPosition = "topleft",
    ) -> None:
        super().__init__(bounding_rect, x, y, size, size, self.__COLOR, rect_position)

        self.carried_sheep: Sheep | None = None
        self.previous_position = (x, y, rect_position)

    def update(self, keys_pressed: ScancodeWrapper, delta_time: float) -> None:
        self.previous_position = (self.rect.left, self.rect.top, "topleft")

        up_pressed = keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]
        down_pressed = keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]
        left_pressed = keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]
        right_pressed = keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]

        speed = self.__ENCUMBERED_SPEED if self.is_carrying_sheep else self.__SPEED

        dx = (
            speed
            * (left_pressed ^ right_pressed)
            * delta_time
            * (right_pressed - left_pressed)
        )
        dy = (
            speed
            * (up_pressed ^ down_pressed)
            * delta_time
            * (down_pressed - up_pressed)
        )

        self.rect.move_ip(dx, dy)
        self.rect.clamp_ip(self.bounding_rect)

        if self.carried_sheep is not None:
            self.carried_sheep.set_position(self.rect.topright, "topleft")

    def revert_movement(self) -> None:
        setattr(
            self.rect,
            self.previous_position[2],
            (self.previous_position[0], self.previous_position[1]),
        )

    def pick_up_sheep(self, sheep: Sheep) -> None:
        self.carried_sheep = sheep

    def is_carried_sheep(self, sheep: Sheep) -> bool:
        return sheep == self.carried_sheep

    @property
    def is_carrying_sheep(self):
        return self.carried_sheep is not None

    def drop_sheep(self) -> None:
        if self.carried_sheep is not None:
            self.carried_sheep.set_position(self.rect.center, "center")
            self.carried_sheep.drop()

        self.carried_sheep = None
