import pygame

from . import layout, theme
from .config import HUD_HEIGHT
from .game import Game, GameState

FACE_COLORS = {
    GameState.READY: theme.FACE_IDLE,
    GameState.PLAYING: theme.FACE_IDLE,
    GameState.WON: theme.FACE_WIN,
    GameState.LOST: theme.FACE_LOSE,
}

MIN_CELL_FONT_SIZE = 10


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        pygame.font.init()
        self.hud_font = pygame.font.SysFont("consolas", 20, bold=True)
        self._cell_fonts: dict[int, pygame.font.Font] = {}

    def _cell_font(self, cell_size: int) -> pygame.font.Font:
        font = self._cell_fonts.get(cell_size)
        if font is None:
            size = max(MIN_CELL_FONT_SIZE, int(cell_size * 0.55))
            font = pygame.font.SysFont("consolas", size, bold=True)
            self._cell_fonts[cell_size] = font
        return font

    def draw(self, game: Game, mouse_cell: tuple[int, int] | None):
        self.screen.fill(theme.BACKGROUND)
        offset_x = layout.board_offset_x(game.difficulty, game.cell_size, self.screen.get_width())
        self._draw_hud(game)
        self._draw_board(game, mouse_cell, offset_x)

    def _draw_hud(self, game: Game):
        width = self.screen.get_width()
        hud_rect = pygame.Rect(0, 0, width, HUD_HEIGHT)
        pygame.draw.rect(self.screen, theme.HUD_BG, hud_rect)
        pygame.draw.line(self.screen, theme.GRID_LINE, (0, HUD_HEIGHT - 1), (width, HUD_HEIGHT - 1))

        mines_surface = self.hud_font.render(
            f"MINES {max(game.board.remaining_mines(), 0):03d}", True, theme.HUD_TEXT
        )
        self.screen.blit(mines_surface, (12, HUD_HEIGHT // 2 - mines_surface.get_height() // 2))

        timer_surface = self.hud_font.render(f"TIME {int(game.elapsed):03d}", True, theme.HUD_TEXT)
        self.screen.blit(
            timer_surface,
            (width - timer_surface.get_width() - 12, HUD_HEIGHT // 2 - timer_surface.get_height() // 2),
        )

        self._draw_face(game, width)

    def _draw_face(self, game: Game, width: int):
        rect = layout.face_rect(width)
        color = FACE_COLORS[game.state]
        pygame.draw.circle(self.screen, color, rect.center, rect.width // 2)
        pygame.draw.circle(self.screen, theme.BACKGROUND, rect.center, rect.width // 2, 2)
        self._draw_face_expression(game, rect)

    def _draw_face_expression(self, game: Game, rect: pygame.Rect):
        cx, cy = rect.center
        dark = theme.FACE_FEATURES
        eye_dx, eye_y = 7, cy - 5

        if game.state == GameState.LOST:
            for ex in (cx - eye_dx, cx + eye_dx):
                pygame.draw.line(self.screen, dark, (ex - 3, eye_y - 3), (ex + 3, eye_y + 3), 2)
                pygame.draw.line(self.screen, dark, (ex - 3, eye_y + 3), (ex + 3, eye_y - 3), 2)
            mouth = [(cx - 6, cy + 8), (cx, cy + 4), (cx + 6, cy + 8)]
        else:
            for ex in (cx - eye_dx, cx + eye_dx):
                pygame.draw.circle(self.screen, dark, (ex, eye_y), 2)
            if game.state == GameState.WON:
                mouth = [(cx - 7, cy + 4), (cx - 3, cy + 9), (cx + 3, cy + 9), (cx + 7, cy + 4)]
            else:
                mouth = [(cx - 5, cy + 6), (cx, cy + 9), (cx + 5, cy + 6)]
        pygame.draw.lines(self.screen, dark, False, mouth, 2)

    def _draw_board(self, game: Game, mouse_cell: tuple[int, int] | None, offset_x: int):
        board = game.board
        for row in range(board.rows):
            for col in range(board.columns):
                self._draw_cell(game, col, row, mouse_cell, offset_x)

    def _draw_cell(
        self, game: Game, col: int, row: int, mouse_cell: tuple[int, int] | None, offset_x: int
    ):
        cell = game.board.cell_at(col, row)
        rect = layout.cell_rect(col, row, game.cell_size, offset_x)
        exploded = cell.is_mine and cell.is_revealed and game.state == GameState.LOST and not cell.is_flagged

        if cell.is_revealed:
            pygame.draw.rect(self.screen, theme.MINE_BG_HIT if exploded else theme.CELL_REVEALED, rect)
        else:
            hovered = game.is_active() and mouse_cell == (col, row)
            pygame.draw.rect(self.screen, theme.CELL_HIDDEN_HOVER if hovered else theme.CELL_HIDDEN, rect)

        pygame.draw.rect(self.screen, theme.GRID_LINE, rect, 1)

        if cell.is_flagged:
            self._draw_flag(rect)
        elif cell.is_revealed:
            if cell.is_mine:
                self._draw_mine(rect)
            elif cell.adjacent_mines > 0:
                self._draw_number(rect, cell.adjacent_mines)

    def _draw_number(self, rect: pygame.Rect, number: int):
        color = theme.NUMBER_COLORS.get(number, theme.FOREGROUND)
        surface = self._cell_font(rect.width).render(str(number), True, color)
        self.screen.blit(surface, surface.get_rect(center=rect.center))

    def _draw_mine(self, rect: pygame.Rect):
        radius = max(3, rect.width // 3)
        pygame.draw.circle(self.screen, theme.MINE_COLOR, rect.center, radius)
        pygame.draw.circle(self.screen, theme.FOREGROUND, rect.center, radius, 1)

    def _draw_flag(self, rect: pygame.Rect):
        margin = max(2, rect.height // 5)
        pole_x = rect.centerx - max(1, rect.width // 8)
        top = rect.top + margin
        bottom = rect.bottom - margin
        base = max(2, (rect.width - 4) // 4)
        pygame.draw.line(self.screen, theme.FLAG_POLE, (pole_x, top), (pole_x, bottom), 2)
        pygame.draw.line(self.screen, theme.FLAG_POLE, (pole_x - base, bottom), (pole_x + base, bottom), 2)
        pygame.draw.polygon(
            self.screen,
            theme.FLAG_CLOTH,
            [(pole_x, top), (pole_x, top + base * 2), (pole_x + base * 2, top + base)],
        )
