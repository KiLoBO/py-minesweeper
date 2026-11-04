# py-minesweeper

Minesweeper, written in Python with pygame, styled with the [Dracula theme](https://draculatheme.com/).

## Run

```
uv run main.py
```

## Difficulty selector

On launch you land on a menu: pick **Beginner** (9x9, 10 mines), **Intermediate**
(16x16, 40 mines), **Expert** (30x16, 99 mines), or **Custom** — tune columns,
rows (5-50 each), and mine count with the +/- steppers, then hit PLAY. Cell
size automatically shrinks for large boards (down to 12px) so even a 50x50
grid stays on screen.

## Controls

**Menu**
- **Click** a preset or Custom, adjust steppers, then **PLAY** (or **Enter**)
- **1 / 2 / 3 / 4** — quick-select Beginner / Intermediate / Expert / Custom

**In-game**
- **Left click** — reveal a cell (or chord a revealed number if its flag count is satisfied)
- **Right click** — flag / unflag a cell
- **Middle click** — chord a revealed number
- **Click the face** or **R** — restart the current difficulty
- **Esc** — back to the difficulty selector

## Layout

- `minesweeper/theme.py` — Dracula color palette
- `minesweeper/config.py` — difficulty presets, custom-board bounds, adaptive cell sizing
- `minesweeper/cell.py` — single-cell state
- `minesweeper/board.py` — grid, mine placement, reveal/flood-fill/chord logic
- `minesweeper/game.py` — game state machine (ready/playing/won/lost) and timer
- `minesweeper/layout.py` — shared pixel geometry (window size, cell rects, hit-testing)
- `minesweeper/ui.py` — reusable button widget
- `minesweeper/menu.py` — difficulty selector screen
- `minesweeper/renderer.py` — all in-game pygame drawing
- `main.py` — pygame setup and the menu/game loop
