import sys

import pygame

from minesweeper import config, layout
from minesweeper.config import Difficulty
from minesweeper.game import Game
from minesweeper.menu import Menu
from minesweeper.menu import WINDOW_SIZE as MENU_WINDOW_SIZE
from minesweeper.renderer import Renderer


def handle_click(game: Game, button: int, target: tuple[int, int]):
    col, row = target
    if button == 1:
        if game.board.cell_at(col, row).is_revealed:
            game.chord(col, row)
        else:
            game.reveal(col, row)
    elif button == 2:
        game.chord(col, row)
    elif button == 3:
        game.toggle_flag(col, row)


def run_menu(screen: pygame.Surface, clock: pygame.time.Clock, selected: Difficulty) -> Difficulty | None:
    """Runs the difficulty selector. Returns the chosen difficulty, or None on quit."""
    menu = Menu(selected)
    while True:
        chosen = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            result = menu.handle_event(event)
            if result is not None:
                chosen = result

        menu.draw(screen)
        pygame.display.flip()
        clock.tick(config.FPS)

        if chosen is not None:
            return chosen


def run_game(screen: pygame.Surface, clock: pygame.time.Clock, difficulty: Difficulty) -> str:
    """Runs the game loop. Returns 'menu' to return to the selector, or 'quit'."""
    renderer = Renderer(screen)
    game = Game(difficulty)

    while True:
        offset_x = layout.board_offset_x(game.difficulty, game.cell_size, screen.get_width())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.restart()
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and layout.face_rect(screen.get_width()).collidepoint(event.pos):
                    game.restart()
                else:
                    target = layout.cell_at_pos(event.pos, game.difficulty, game.cell_size, offset_x)
                    if target is not None:
                        handle_click(game, event.button, target)

        game.tick()
        mouse_target = layout.cell_at_pos(pygame.mouse.get_pos(), game.difficulty, game.cell_size, offset_x)
        renderer.draw(game, mouse_target)
        pygame.display.flip()
        clock.tick(config.FPS)


def main():
    pygame.init()
    pygame.display.set_caption(config.TITLE)
    clock = pygame.time.Clock()

    difficulty = config.BEGINNER
    screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

    while True:
        difficulty = run_menu(screen, clock, difficulty)
        if difficulty is None:
            break

        screen = pygame.display.set_mode(layout.window_size(difficulty, config.cell_size_for(difficulty)))
        result = run_game(screen, clock, difficulty)
        if result == "quit":
            break

        screen = pygame.display.set_mode(MENU_WINDOW_SIZE)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
