from dataclasses import dataclass


@dataclass(frozen=True)
class Difficulty:
    name: str
    columns: int
    rows: int
    mines: int


BEGINNER = Difficulty("Beginner", 9, 9, 10)
INTERMEDIATE = Difficulty("Intermediate", 16, 16, 40)
EXPERT = Difficulty("Expert", 30, 16, 99)
PRESETS = (BEGINNER, INTERMEDIATE, EXPERT)

CUSTOM_DEFAULT = Difficulty("Custom", 30, 30, 180)

TITLE = "Minesweeper"
HUD_HEIGHT = 56
FPS = 60

# Custom board bounds.
MIN_DIMENSION = 5
MAX_DIMENSION = 50
MIN_MINES = 1
SAFE_ZONE_CELLS = 9  # reserved around the first click so it can never be a mine

# Cell size shrinks for large boards so they stay on screen; grows up to
# MAX_CELL_SIZE for small ones.
MIN_CELL_SIZE = 12
MAX_CELL_SIZE = 32
MAX_BOARD_PIXELS_WIDTH = 900
MAX_BOARD_PIXELS_HEIGHT = 640

# Window is never narrower than this, so HUD text has room on tiny boards.
MIN_WINDOW_WIDTH = 300


def max_mines_for(columns: int, rows: int) -> int:
    return max(MIN_MINES, columns * rows - SAFE_ZONE_CELLS)


def clamp_custom(columns: int, rows: int, mines: int) -> Difficulty:
    columns = max(MIN_DIMENSION, min(MAX_DIMENSION, columns))
    rows = max(MIN_DIMENSION, min(MAX_DIMENSION, rows))
    mines = max(MIN_MINES, min(max_mines_for(columns, rows), mines))
    return Difficulty("Custom", columns, rows, mines)


def cell_size_for(difficulty: Difficulty) -> int:
    size = min(
        MAX_BOARD_PIXELS_WIDTH // difficulty.columns,
        MAX_BOARD_PIXELS_HEIGHT // difficulty.rows,
        MAX_CELL_SIZE,
    )
    return max(MIN_CELL_SIZE, size)
