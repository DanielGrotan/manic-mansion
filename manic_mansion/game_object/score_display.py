from pygame.font import SysFont
from pygame.sprite import Sprite

from ..custom_types import Color, RectPosition


class ScoreDisplay(Sprite):
    def __init__(
        self, x: int, y: int, text_color: Color, rect_position: RectPosition
    ) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.text_color = text_color
        self.rect_position = rect_position

        self.font = SysFont("Arial", 34)
        self.score = 0

        self._render_text()

    def _render_text(self) -> None:
        self.image = self.font.render(f"Score: {self.score}", True, self.text_color)
        self.rect = self.image.get_rect(**{self.rect_position: (self.x, self.y)})

    def increment_score(self) -> None:
        self.score += 1
        self._render_text()
