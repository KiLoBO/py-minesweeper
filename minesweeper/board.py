import random

from .cell import Cell


class Board:
    def __init__(self, columns: int, rows: int, mine_count: int):
        self.columns = columns
        self.rows = rows
        self.mine_count = mine_count
        self.grid = [[Cell() for _ in range(columns)] for _ in range(rows)]
        self.mines_placed = False
        self.flags_used = 0
        self.revealed_count = 0

    def in_bounds(self, col: int, row: int) -> bool:
        return 0 <= col < self.columns and 0 <= row < self.rows

    def neighbors(self, col: int, row: int):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nc, nr = col + dc, row + dr
                if self.in_bounds(nc, nr):
                    yield nc, nr

    def cell_at(self, col: int, row: int) -> Cell:
        return self.grid[row][col]

    def place_mines(self, safe_col: int, safe_row: int):
        """Place mines, keeping the first-clicked cell and its neighbors safe."""
        safe_cells = {(safe_col, safe_row)} | set(self.neighbors(safe_col, safe_row))
        candidates = [
            (c, r)
            for r in range(self.rows)
            for c in range(self.columns)
            if (c, r) not in safe_cells
        ]
        for c, r in random.sample(candidates, self.mine_count):
            self.grid[r][c].is_mine = True

        for r in range(self.rows):
            for c in range(self.columns):
                cell = self.grid[r][c]
                if not cell.is_mine:
                    cell.adjacent_mines = sum(
                        1 for nc, nr in self.neighbors(c, r) if self.grid[nr][nc].is_mine
                    )
        self.mines_placed = True

    def reveal(self, col: int, row: int) -> bool:
        """Reveal a cell, flood-filling through connected zero-adjacency cells.

        Returns True if a mine was revealed.
        """
        if not self.mines_placed:
            self.place_mines(col, row)

        hit_mine = False
        stack = [(col, row)]
        while stack:
            c, r = stack.pop()
            cell = self.cell_at(c, r)
            if cell.is_revealed or cell.is_flagged:
                continue
            cell.is_revealed = True
            self.revealed_count += 1
            if cell.is_mine:
                hit_mine = True
                continue
            if cell.adjacent_mines == 0:
                stack.extend(self.neighbors(c, r))
        return hit_mine

    def chord(self, col: int, row: int) -> bool:
        """Reveal the unflagged neighbors of a revealed numbered cell when the
        surrounding flag count matches its number. Returns True if a mine was
        revealed.
        """
        cell = self.cell_at(col, row)
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return False

        neighbors = list(self.neighbors(col, row))
        flagged = sum(1 for nc, nr in neighbors if self.cell_at(nc, nr).is_flagged)
        if flagged != cell.adjacent_mines:
            return False

        hit_mine = False
        for nc, nr in neighbors:
            target = self.cell_at(nc, nr)
            if not target.is_flagged and not target.is_revealed:
                if self.reveal(nc, nr):
                    hit_mine = True
        return hit_mine

    def toggle_flag(self, col: int, row: int):
        cell = self.cell_at(col, row)
        if cell.is_revealed:
            return
        cell.is_flagged = not cell.is_flagged
        self.flags_used += 1 if cell.is_flagged else -1

    def reveal_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True

    def is_won(self) -> bool:
        total_cells = self.columns * self.rows
        return self.revealed_count == total_cells - self.mine_count

    def remaining_mines(self) -> int:
        return self.mine_count - self.flags_used
