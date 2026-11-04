class Cell:
    __slots__ = ("is_mine", "is_revealed", "is_flagged", "adjacent_mines")

    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
