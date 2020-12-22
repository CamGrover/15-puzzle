import pygame
from game_model import GameModel
from game_view import GameView
from game_controller import GameController
from constants import WIN_WIDTH, WIN_HEIGHT
from events import TickEvent, EventManager, QuitEvent
from cpu_spinner_controller import CPUSpinnerController
import os

os.environ['SDL_AUDIODRIVER'] = 'dsp'


# Source: MVC and Observer/Mediator in Pygame
# Title: sjbrown's Writing Games Tutorial
# URL: http://ezide.com/games/writing-games.html
def main():
    pygame.init()

    pygame.display.set_caption("The 15 Puzzle")
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    event_manager = EventManager()
    game_board = GameModel()
    game_view = GameView(win)
    spinner = CPUSpinnerController(event_manager, clock)
    game_controller = GameController(game_board, game_view)

    event_manager.registerListener(TickEvent(), game_controller)
    event_manager.registerListener(QuitEvent(), spinner)

    spinner.run()

    pygame.quit()


if __name__ == "__main__":
    main()
