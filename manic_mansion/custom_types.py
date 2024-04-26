from typing import Literal

type Color = tuple[int, int, int]
type RectPosition = Literal[
    "topleft",
    "bottomleft",
    "topright",
    "bottomright",
    "midtop",
    "midleft",
    "midbottom",
    "midright",
    "center",
]
