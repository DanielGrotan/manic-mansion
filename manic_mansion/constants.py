from typing import Literal

from .custom_types import Color

type ColorName = Literal["brown", "pink", "blue", "grey", "white", "green", "black"]

COLORS: dict[ColorName, Color] = {
    "brown": (139, 69, 19),
    "pink": (255, 105, 180),
    "blue": (30, 144, 255),
    "grey": (128, 128, 128),
    "white": (255, 255, 255),
    "green": (0, 128, 0),
    "black": (0, 0, 0),
}

PLAYER_SPEED = 180
PLAYER_ENCUMBERED_SPEED = 120

GHOST_MAX_SPEED = 150

OBJECT_SIZE = 50
