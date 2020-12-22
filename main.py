import pygame
from game_board import GameBoard
from game_view import GameView
from game_controller import GameController
from constants import WIN_WIDTH, WIN_HEIGHT
from events import TickEvent, EventManager, QuitEvent


class CPUSpinnerController:
    def __init__(self, ev_manager, clock):
        self.ev_manager = ev_manager
        self.clock = clock
        self.keepGoing = True

    def run(self):
        while self.keepGoing:
            self.clock.tick(60)
            event = TickEvent()
            self.ev_manager.post(event)

    def notify(self, event, event_manager=None):
        if isinstance(event, QuitEvent):
            self.keepGoing = False


def main():
    pygame.init()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("The 15 Puzzle")
    clock = pygame.time.Clock()
    event_manager = EventManager()
    game_board = GameBoard()
    game_view = GameView(win)
    spinner = CPUSpinnerController(event_manager, clock)
    game_board.restart()
    game_controller = GameController(game_board, game_view)

    event_manager.registerListener(TickEvent(), game_controller)
    event_manager.registerListener(QuitEvent(), spinner)

    spinner.run()

    pygame.quit()


if __name__ == "__main__":
    main()
