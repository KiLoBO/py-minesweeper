"""Dracula color palette (https://draculatheme.com/contribute)."""

BACKGROUND = (40, 42, 54)       # #282a36
CURRENT_LINE = (68, 71, 90)     # #44475a
FOREGROUND = (248, 248, 242)    # #f8f8f2
COMMENT = (98, 114, 164)        # #6272a4
CYAN = (139, 233, 253)          # #8be9fd
GREEN = (80, 250, 123)          # #50fa7b
ORANGE = (255, 184, 108)        # #ffb86c
PINK = (255, 121, 198)          # #ff79c6
PURPLE = (189, 147, 249)        # #bd93f9
RED = (255, 85, 85)             # #ff5555
YELLOW = (241, 250, 140)        # #f1fa8c

# Classic minesweeper number colors, mapped onto the Dracula palette.
NUMBER_COLORS = {
    1: CYAN,
    2: GREEN,
    3: RED,
    4: PURPLE,
    5: ORANGE,
    6: PINK,
    7: YELLOW,
    8: FOREGROUND,
}

CELL_HIDDEN = CURRENT_LINE
CELL_HIDDEN_HOVER = (82, 86, 110)
CELL_REVEALED = (33, 34, 44)
GRID_LINE = BACKGROUND

MINE_COLOR = RED
MINE_BG_HIT = (120, 40, 50)
FLAG_POLE = FOREGROUND
FLAG_CLOTH = RED

HUD_BG = CURRENT_LINE
HUD_TEXT = FOREGROUND

FACE_IDLE = PURPLE
FACE_WIN = GREEN
FACE_LOSE = RED
FACE_FEATURES = BACKGROUND
