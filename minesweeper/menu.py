import pygame

from . import config, theme
from .config import Difficulty
from .ui import Button

WINDOW_SIZE = (440, 540)

_PRESET_COUNT = len(config.PRESETS)
_CUSTOM_INDEX = _PRESET_COUNT

_MARGIN_X = 36
_BUTTON_HEIGHT = 46
_BUTTON_GAP = 12
_STEPPER_SIZE = 28


class Menu:
    """Pre-game difficulty selector: Beginner/Intermediate/Expert presets, or a
    Custom board (up to 50x50) tuned with +/- steppers."""

    def __init__(self, selected: Difficulty):
        pygame.font.init()
        self._title_font = pygame.font.SysFont("consolas", 30, bold=True)
        self._button_font = pygame.font.SysFont("consolas", 16, bold=True)
        self._label_font = pygame.font.SysFont("consolas", 14, bold=True)
        self._hint_font = pygame.font.SysFont("consolas", 13)

        if selected in config.PRESETS:
            self.selected_index = config.PRESETS.index(selected)
            self.custom_columns = config.CUSTOM_DEFAULT.columns
            self.custom_rows = config.CUSTOM_DEFAULT.rows
            self.custom_mines = config.CUSTOM_DEFAULT.mines
        else:
            self.selected_index = _CUSTOM_INDEX
            self.custom_columns = selected.columns
            self.custom_rows = selected.rows
            self.custom_mines = selected.mines

        self._build_layout()

    def _build_layout(self):
        width, _ = WINDOW_SIZE
        button_width = width - _MARGIN_X * 2
        x, y = _MARGIN_X, 96

        self._preset_buttons: list[Button] = []
        for difficulty in config.PRESETS:
            label = f"{difficulty.name}   {difficulty.columns}x{difficulty.rows}   {difficulty.mines} mines"
            self._preset_buttons.append(
                Button(pygame.Rect(x, y, button_width, _BUTTON_HEIGHT), label, self._button_font)
            )
            y += _BUTTON_HEIGHT + _BUTTON_GAP

        self._custom_button = Button(
            pygame.Rect(x, y, button_width, _BUTTON_HEIGHT), "Custom", self._button_font
        )
        y += _BUTTON_HEIGHT + _BUTTON_GAP + 8

        stepper_width = (button_width - 2 * 16) // 3
        self._steppers = {
            "columns": self._stepper_geometry(x, y, stepper_width),
            "rows": self._stepper_geometry(x + stepper_width + 16, y, stepper_width),
            "mines": self._stepper_geometry(x + (stepper_width + 16) * 2, y, stepper_width),
        }
        y += 78

        self._play_button = Button(pygame.Rect(x, y, button_width, _BUTTON_HEIGHT), "PLAY", self._button_font)
        self._hint_y = y + _BUTTON_HEIGHT + 28

    @staticmethod
    def _stepper_geometry(x: int, y: int, width: int) -> dict:
        return {
            "x": x,
            "y": y,
            "w": width,
            "minus": pygame.Rect(x, y + 22, _STEPPER_SIZE, _STEPPER_SIZE),
            "plus": pygame.Rect(x + width - _STEPPER_SIZE, y + 22, _STEPPER_SIZE, _STEPPER_SIZE),
        }

    def current_difficulty(self) -> Difficulty:
        if self.selected_index < _PRESET_COUNT:
            return config.PRESETS[self.selected_index]
        return config.clamp_custom(self.custom_columns, self.custom_rows, self.custom_mines)

    def handle_event(self, event: pygame.event.Event) -> Difficulty | None:
        if event.type == pygame.KEYDOWN:
            return self._handle_key(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self._handle_click(event.pos)
        return None

    def _handle_key(self, event: pygame.event.Event) -> Difficulty | None:
        if event.key == pygame.K_RETURN:
            return self.current_difficulty()
        preset_keys = (pygame.K_1, pygame.K_2, pygame.K_3)
        if event.key in preset_keys:
            self.selected_index = preset_keys.index(event.key)
        elif event.key == pygame.K_4:
            self.selected_index = _CUSTOM_INDEX
        return None

    def _handle_click(self, pos: tuple[int, int]) -> Difficulty | None:
        for i, button in enumerate(self._preset_buttons):
            if button.is_hovered(pos):
                self.selected_index = i
                return None

        if self._custom_button.is_hovered(pos):
            self.selected_index = _CUSTOM_INDEX
            return None

        if self.selected_index == _CUSTOM_INDEX:
            if self._steppers["columns"]["minus"].collidepoint(pos):
                self._adjust_dimension("columns", -1)
            elif self._steppers["columns"]["plus"].collidepoint(pos):
                self._adjust_dimension("columns", 1)
            elif self._steppers["rows"]["minus"].collidepoint(pos):
                self._adjust_dimension("rows", -1)
            elif self._steppers["rows"]["plus"].collidepoint(pos):
                self._adjust_dimension("rows", 1)
            elif self._steppers["mines"]["minus"].collidepoint(pos):
                self._adjust_mines(-5)
            elif self._steppers["mines"]["plus"].collidepoint(pos):
                self._adjust_mines(5)

        if self._play_button.is_hovered(pos):
            return self.current_difficulty()
        return None

    def _adjust_dimension(self, which: str, delta: int):
        value = self.custom_columns if which == "columns" else self.custom_rows
        value = max(config.MIN_DIMENSION, min(config.MAX_DIMENSION, value + delta))
        if which == "columns":
            self.custom_columns = value
        else:
            self.custom_rows = value
        self.custom_mines = min(self.custom_mines, config.max_mines_for(self.custom_columns, self.custom_rows))

    def _adjust_mines(self, delta: int):
        bound = config.max_mines_for(self.custom_columns, self.custom_rows)
        self.custom_mines = max(config.MIN_MINES, min(bound, self.custom_mines + delta))

    def draw(self, screen: pygame.Surface):
        screen.fill(theme.BACKGROUND)
        mouse_pos = pygame.mouse.get_pos()
        width = WINDOW_SIZE[0]

        title = self._title_font.render("MINESWEEPER", True, theme.PURPLE)
        screen.blit(title, title.get_rect(center=(width // 2, 44)))

        for i, button in enumerate(self._preset_buttons):
            button.draw(screen, mouse_pos, selected=(self.selected_index == i))

        self._custom_button.draw(screen, mouse_pos, selected=(self.selected_index == _CUSTOM_INDEX))

        if self.selected_index == _CUSTOM_INDEX:
            self._draw_steppers(screen, mouse_pos)

        self._play_button.draw(screen, mouse_pos)

        hint = self._hint_font.render("1 / 2 / 3 / 4 to pick   Enter or PLAY to start", True, theme.COMMENT)
        screen.blit(hint, hint.get_rect(center=(width // 2, self._hint_y)))

    def _draw_steppers(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        specs = (
            ("COLUMNS", self.custom_columns, self._steppers["columns"]),
            ("ROWS", self.custom_rows, self._steppers["rows"]),
            ("MINES", self.custom_mines, self._steppers["mines"]),
        )
        for label, value, stepper in specs:
            label_surface = self._label_font.render(label, True, theme.HUD_TEXT)
            screen.blit(label_surface, (stepper["x"], stepper["y"]))

            for rect, symbol in ((stepper["minus"], "-"), (stepper["plus"], "+")):
                hovered = rect.collidepoint(mouse_pos)
                pygame.draw.rect(
                    screen, theme.CELL_HIDDEN_HOVER if hovered else theme.CURRENT_LINE, rect, border_radius=4
                )
                pygame.draw.rect(screen, theme.GRID_LINE, rect, 1, border_radius=4)
                symbol_surface = self._button_font.render(symbol, True, theme.FOREGROUND)
                screen.blit(symbol_surface, symbol_surface.get_rect(center=rect.center))

            value_surface = self._button_font.render(str(value), True, theme.FOREGROUND)
            center = (stepper["x"] + stepper["w"] // 2, stepper["y"] + 22 + _STEPPER_SIZE // 2)
            screen.blit(value_surface, value_surface.get_rect(center=center))
