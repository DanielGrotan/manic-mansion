from pygame import Rect, Surface
from pygame.key import ScancodeWrapper
from pygame.sprite import Sprite

from ..custom_types import Color, RectPosition


class GameObject(Sprite):
    def __init__(
        self,
        bounding_rect: Rect,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Color,
        rect_position: RectPosition = "topleft",
    ) -> None:
        self.bounding_rect = bounding_rect

        self.image = Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect(**{rect_position: (x, y)})

    def update(self, keys_pressed: ScancodeWrapper, delta_time: float) -> None:
        pass
