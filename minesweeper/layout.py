import pygame

from .config import HUD_HEIGHT, MIN_WINDOW_WIDTH, Difficulty

FACE_SIZE = 32


def window_size(difficulty: Difficulty, cell_size: int) -> tuple[int, int]:
    width = max(difficulty.columns * cell_size, MIN_WINDOW_WIDTH)
    height = difficulty.rows * cell_size + HUD_HEIGHT
    return width, height


def board_offset_x(difficulty: Difficulty, cell_size: int, screen_width: int) -> int:
    board_width = difficulty.columns * cell_size
    return max((screen_width - board_width) // 2, 0)


def cell_rect(col: int, row: int, cell_size: int, offset_x: int = 0) -> pygame.Rect:
    return pygame.Rect(offset_x + col * cell_size, row * cell_size + HUD_HEIGHT, cell_size, cell_size)


def cell_at_pos(
    pos: tuple[int, int], difficulty: Difficulty, cell_size: int, offset_x: int = 0
) -> tuple[int, int] | None:
    x, y = pos
    if y < HUD_HEIGHT:
        return None
    col = (x - offset_x) // cell_size
    row = (y - HUD_HEIGHT) // cell_size
    if 0 <= col < difficulty.columns and 0 <= row < difficulty.rows:
        return col, row
    return None


def face_rect(screen_width: int) -> pygame.Rect:
    return pygame.Rect(0, 0, FACE_SIZE, FACE_SIZE).move(
        screen_width // 2 - FACE_SIZE // 2, HUD_HEIGHT // 2 - FACE_SIZE // 2
    )
