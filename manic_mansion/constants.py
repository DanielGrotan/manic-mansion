from typing import Literal

from custom_types import Color

type ColorName = Literal["brown", "pink", "blue", "grey"]

COLORS: dict[ColorName, Color] = {
    "brown": (139, 69, 19),
    "pink": (255, 105, 180),
    "blue": (30, 144, 255),
    "grey": (128, 128, 128),
}

PLAYER_SPEED = 100
PLAYER_ENCUMBERED_SPEED = 60

GHOST_MAX_SPEED = 100
