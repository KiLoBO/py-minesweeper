import pygame

from . import theme


class Button:
    def __init__(self, rect: pygame.Rect, label: str, font: pygame.font.Font):
        self.rect = rect
        self.label = label
        self.font = font

    def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int], selected: bool = False):
        if selected:
            bg, text_color = theme.PURPLE, theme.BACKGROUND
        elif self.is_hovered(mouse_pos):
            bg, text_color = theme.CELL_HIDDEN_HOVER, theme.FOREGROUND
        else:
            bg, text_color = theme.CURRENT_LINE, theme.FOREGROUND

        pygame.draw.rect(screen, bg, self.rect, border_radius=6)
        pygame.draw.rect(screen, theme.GRID_LINE, self.rect, 2, border_radius=6)
        text = self.font.render(self.label, True, text_color)
        screen.blit(text, text.get_rect(center=self.rect.center))
