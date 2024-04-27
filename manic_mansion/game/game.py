import random

import pygame
from pygame.sprite import AbstractGroup, Group, GroupSingle
from pygame.time import Clock

from ..constants import COLORS, OBJECT_SIZE
from ..game_object import Ghost, Obstacle, Player, ScoreDisplay, Sheep, Zone

type SpawnableGameObject = type[Ghost] | type[Sheep] | type[Obstacle]


class Game:
    __TITLE = "Manic Mansion"

    def __init__(self, window_width: int, window_height: int):
        pygame.font.init()

        self.window_width = window_width
        self.window_height = window_height

        self.window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(self.__TITLE)

        self.aesthetic_sprite_groups: list[AbstractGroup] = []
        self.dynamic_sprite_groups: list[AbstractGroup] = []

        self.zone_group = Group()
        self.aesthetic_sprite_groups.append(self.zone_group)

        self.score_display_group = GroupSingle()
        self.aesthetic_sprite_groups.append(self.score_display_group)

        self.player_group = GroupSingle()
        self.dynamic_sprite_groups.append(self.player_group)

        self.ghost_group = Group()
        self.dynamic_sprite_groups.append(self.ghost_group)

        self.sheep_group = Group()
        self.dynamic_sprite_groups.append(self.sheep_group)

        self.obstacle_group = Group()
        self.dynamic_sprite_groups.append(self.obstacle_group)

        self.draw_order: list[AbstractGroup] = [
            self.zone_group,
            self.player_group,
            self.ghost_group,
            self.sheep_group,
            self.obstacle_group,
            self.score_display_group,
        ]

        self.running = False

    def run(self, fps: int) -> None:
        self._setup()

        clock = Clock()

        while self.running:
            delta_time = clock.tick(fps) / 1000

            self._handle_events()
            self._update(delta_time)
            self._draw()

            pygame.display.update()

    def _setup(self) -> None:
        self._clear_sprite_groups()
        self._spawn_initial_game_objects()

        self.running = True

    def _clear_sprite_groups(self) -> None:
        for group in self.aesthetic_sprite_groups + self.dynamic_sprite_groups:
            group.empty()

    def _spawn_initial_game_objects(self) -> None:
        self._spawn_initial_zones()
        self._spawn_initial_score_display()
        self._spawn_initial_player()
        self._spawn_initial_ghost()
        self._spawn_initial_obstacles()
        self._spawn_initial_sheep()

        [print(sheep.rect) for sheep in self.sheep_group]

    def _spawn_initial_zones(self) -> None:
        self.left_zone = Zone(
            self.window.get_rect(),
            0,
            0,
            self.window_width // 5,
            self.window_height,
            COLORS["green"],
        )
        self.middle_zone = Zone(
            self.window.get_rect(),
            self.left_zone.rect.right,
            0,
            self.window_width * 3 // 5,
            self.window_height,
            COLORS["white"],
        )
        self.right_zone = Zone(
            self.window.get_rect(),
            self.middle_zone.rect.right,
            0,
            self.window_width // 5,
            self.window_height,
            COLORS["green"],
        )

        self.zone_group.add(self.left_zone, self.middle_zone, self.right_zone)

    def _spawn_initial_score_display(self) -> None:
        self.score_display = ScoreDisplay(
            self.window_width // 2, 20, COLORS["black"], "midtop"
        )
        self.score_display_group.sprite = self.score_display

    def _spawn_initial_player(self) -> None:
        self.player = Player(
            self.window.get_rect(),
            self.left_zone.rect.right,
            self.left_zone.rect.centery,
            OBJECT_SIZE,
            "midright",
        )

        self.player_group.sprite = self.player

    def _spawn_initial_ghost(self) -> None:
        self._spawn_game_object(Ghost, self.middle_zone.rect, self.ghost_group)

    def _spawn_initial_sheep(self) -> None:
        [
            self._spawn_game_object(Sheep, self.right_zone.rect, self.sheep_group)
            for _ in range(3)
        ]

    def _spawn_initial_obstacles(self) -> None:
        [
            self._spawn_game_object(
                Obstacle, self.middle_zone.rect, self.obstacle_group
            )
            for _ in range(3)
        ]

    def _spawn_game_object(
        self,
        game_object_class: SpawnableGameObject,
        bounding_rect: pygame.Rect,
        target_group: Group,
    ) -> None:
        while True:
            x = random.randint(bounding_rect.left, bounding_rect.right - OBJECT_SIZE)
            y = random.randint(bounding_rect.top, bounding_rect.bottom - OBJECT_SIZE)

            game_object = game_object_class(bounding_rect, x, y, OBJECT_SIZE)

            if any(
                pygame.sprite.spritecollideany(game_object, group)
                for group in self.dynamic_sprite_groups
            ):
                continue

            target_group.add(game_object)
            return

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, delta_time: float) -> None:
        keys_pressed = pygame.key.get_pressed()

        for group in self.dynamic_sprite_groups:
            group.update(keys_pressed, delta_time)

        if pygame.sprite.spritecollideany(self.player, self.ghost_group):
            self.running = False

        if pygame.sprite.spritecollideany(self.player, self.obstacle_group):
            self.player.revert_movement()

        if sheep := pygame.sprite.spritecollideany(self.player, self.sheep_group):
            if self.player.is_carrying_sheep and not self.player.is_carried_sheep(
                sheep
            ):
                self.running = False
                return

            if not sheep.has_been_moved:
                self.player.pick_up_sheep(sheep)

        if (
            self.player.rect.right <= self.left_zone.rect.right
            and self.player.is_carrying_sheep
        ):
            self.player.drop_sheep()
            self._spawn_game_object(Sheep, self.right_zone.rect, self.sheep_group)
            self._spawn_game_object(Ghost, self.middle_zone.rect, self.ghost_group)
            self._spawn_game_object(
                Obstacle, self.middle_zone.rect, self.obstacle_group
            )

            self.score_display.increment_score()

    def _draw(self) -> None:
        for group in self.draw_order:
            group.draw(self.window)
