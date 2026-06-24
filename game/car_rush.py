"""Endless lane-dodging car game with keyboard and touch controls."""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass

import pygame

# Base resolution; window scales on desktop, native on mobile.
WIDTH = 480
HEIGHT = 800
FPS = 60

LANE_COUNT = 3
ROAD_MARGIN = 60
LANE_WIDTH = (WIDTH - ROAD_MARGIN * 2) // LANE_COUNT

PLAYER_WIDTH = 56
PLAYER_HEIGHT = 96
ENEMY_WIDTH = 56
ENEMY_HEIGHT = 96

PLAYER_SPEED = 9
ENEMY_MIN_SPEED = 5
ENEMY_MAX_SPEED = 11
SPAWN_EVERY_MS = 900

COLOR_BG = (34, 139, 34)
COLOR_ROAD = (55, 55, 55)
COLOR_LANE = (220, 220, 220)
COLOR_PLAYER = (52, 152, 219)
COLOR_ENEMY = (231, 76, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_OVERLAY = (0, 0, 0, 160)


@dataclass
class Car:
    lane: int
    y: float
    speed: float
    color: tuple[int, int, int]

    @property
    def rect(self) -> pygame.Rect:
        x = ROAD_MARGIN + self.lane * LANE_WIDTH + (LANE_WIDTH - ENEMY_WIDTH) // 2
        return pygame.Rect(int(x), int(self.y), ENEMY_WIDTH, ENEMY_HEIGHT)


def lane_center_x(lane: int, car_width: int) -> int:
    return ROAD_MARGIN + lane * LANE_WIDTH + (LANE_WIDTH - car_width) // 2


def draw_road(surface: pygame.Surface, scroll: float) -> None:
    surface.fill(COLOR_BG)
    road_rect = pygame.Rect(ROAD_MARGIN, 0, WIDTH - ROAD_MARGIN * 2, HEIGHT)
    pygame.draw.rect(surface, COLOR_ROAD, road_rect)

    dash_h = 40
    gap = 30
    offset = int(scroll) % (dash_h + gap)
    for lane in range(1, LANE_COUNT):
        x = ROAD_MARGIN + lane * LANE_WIDTH
        y = -offset
        while y < HEIGHT:
            pygame.draw.rect(surface, COLOR_LANE, (x - 2, y, 4, dash_h))
            y += dash_h + gap


def draw_car(surface: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int]) -> None:
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, (20, 20, 20), rect.inflate(-10, -18), border_radius=4)


def rects_overlap(a: pygame.Rect, b: pygame.Rect) -> bool:
    return a.colliderect(b)


def spawn_enemy(enemies: list[Car]) -> None:
    occupied = {e.lane for e in enemies if e.y < ENEMY_HEIGHT * 1.5}
    free_lanes = [lane for lane in range(LANE_COUNT) if lane not in occupied]
    if not free_lanes:
        return
    lane = random.choice(free_lanes)
    speed = random.uniform(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
    shade = random.randint(180, 240)
    enemies.append(Car(lane=lane, y=-ENEMY_HEIGHT, speed=speed, color=(shade, 55, 45)))


def draw_text(
    surface: pygame.Surface,
    text: str,
    size: int,
    y: int,
    *,
    center_x: int | None = None,
) -> None:
    font = pygame.font.SysFont("arial", size, bold=True)
    rendered = font.render(text, True, COLOR_TEXT)
    x = (center_x if center_x is not None else WIDTH // 2) - rendered.get_width() // 2
    surface.blit(rendered, (x, y))


def run_game() -> None:
    pygame.init()
    pygame.display.set_caption("Car Rush")

    flags = pygame.SCALED
    if pygame.display.get_driver() in {"android", "kmsdrm", "x11"}:
        flags |= pygame.FULLSCREEN

    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    clock = pygame.time.Clock()

    player_lane = 1
    player_y = HEIGHT - PLAYER_HEIGHT - 40
    player_rect = pygame.Rect(
        lane_center_x(player_lane, PLAYER_WIDTH),
        player_y,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )

    enemies: list[Car] = []
    score = 0
    scroll = 0.0
    running = True
    game_over = False
    last_spawn = pygame.time.get_ticks()
    while running:
        dt = clock.tick(FPS)
        scroll += 4

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if game_over and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    return run_game()
                if not game_over:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        player_lane = max(0, player_lane - 1)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        player_lane = min(LANE_COUNT - 1, player_lane + 1)
            elif event.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
                x = event.x * WIDTH if hasattr(event, "x") else event.pos[0]
                if game_over:
                    return run_game()
                elif x < WIDTH / 2:
                    player_lane = max(0, player_lane - 1)
                else:
                    player_lane = min(LANE_COUNT - 1, player_lane + 1)

        if not game_over:

            player_rect.x = lane_center_x(player_lane, PLAYER_WIDTH)

            now = pygame.time.get_ticks()
            if now - last_spawn >= SPAWN_EVERY_MS:
                spawn_enemy(enemies)
                last_spawn = now

            for enemy in enemies:
                enemy.y += enemy.speed

            enemies = [e for e in enemies if e.y < HEIGHT + ENEMY_HEIGHT]

            for enemy in enemies:
                if rects_overlap(player_rect, enemy.rect):
                    game_over = True
                    break

            score += dt // 16

        draw_road(screen, scroll)
        for enemy in enemies:
            draw_car(screen, enemy.rect, enemy.color)
        draw_car(screen, player_rect, COLOR_PLAYER)

        draw_text(screen, f"Score: {score}", 28, 16)

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(COLOR_OVERLAY)
            screen.blit(overlay, (0, 0))
            draw_text(screen, "CRASH!", 64, HEIGHT // 2 - 90)
            draw_text(screen, f"Final score: {score}", 32, HEIGHT // 2 - 10)
            draw_text(screen, "Tap or press SPACE to restart", 24, HEIGHT // 2 + 50)
        else:
            draw_text(screen, "Tap sides or use arrow keys", 20, HEIGHT - 34)

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)
