import time
from enum import Enum, auto

from . import config
from .board import Board
from .config import Difficulty


class GameState(Enum):
    READY = auto()
    PLAYING = auto()
    WON = auto()
    LOST = auto()


class Game:
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.cell_size = config.cell_size_for(difficulty)
        self.board = Board(difficulty.columns, difficulty.rows, difficulty.mines)
        self.state = GameState.READY
        self.start_time = None
        self.elapsed = 0.0

    def restart(self, difficulty: Difficulty | None = None):
        self.difficulty = difficulty or self.difficulty
        self.cell_size = config.cell_size_for(self.difficulty)
        self.board = Board(self.difficulty.columns, self.difficulty.rows, self.difficulty.mines)
        self.state = GameState.READY
        self.start_time = None
        self.elapsed = 0.0

    def is_active(self) -> bool:
        return self.state in (GameState.READY, GameState.PLAYING)

    def reveal(self, col: int, row: int):
        if not self.is_active():
            return
        cell = self.board.cell_at(col, row)
        if cell.is_flagged or cell.is_revealed:
            return
        if self.state == GameState.READY:
            self.state = GameState.PLAYING
            self.start_time = time.monotonic()
        self._update_state(self.board.reveal(col, row))

    def chord(self, col: int, row: int):
        if self.state != GameState.PLAYING:
            return
        self._update_state(self.board.chord(col, row))

    def toggle_flag(self, col: int, row: int):
        if not self.is_active():
            return
        self.board.toggle_flag(col, row)

    def tick(self):
        if self.state == GameState.PLAYING:
            self.elapsed = time.monotonic() - self.start_time

    def _update_state(self, hit_mine: bool):
        if hit_mine:
            self.board.reveal_all_mines()
            self.state = GameState.LOST
        elif self.board.is_won():
            self.state = GameState.WON
