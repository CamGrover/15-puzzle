import pygame
from blit_text import blit_text


class Interface:
    def __init__(self, window):
        self.window = window
        self.moves_used_box = pygame.Rect(4, 260, 64, 32)
        self.best_score = pygame.Rect(164, 260, 64, 32)
        self.instructions_btn = pygame.Rect(0, 288, 256, 32)
        self.row_3 = pygame.Rect(0, 300, 256, 32)
        self.show_completed = False
        self.font_24 = pygame.font.SysFont("Monaco", 28, bold=False,
                                           italic=False)
        self.font_16 = pygame.font.SysFont("Monaco", 16, bold=False,
                                           italic=False)

    def draw(self, window, game_board):
        black = pygame.color.Color(0, 0, 0)
        white = pygame.color.Color(255, 255, 255)
        moves = self.font_24.render(
            f"Moves: {game_board.moves}", True, white, black)
        best_score = self.font_24.render(
            f"Best: {game_board.get_best_score()}", True, white, black)
        instructions_1 = self.font_24.render(
            "Show Instructions",
            True, black, white
        )
        window.blit(moves, self.moves_used_box)
        window.blit(best_score, self.best_score)
        window.blit(instructions_1, self.instructions_btn)
        game_board.draw(window)

    def draw_instructions(self, window):
        instructions = \
            "Slide tiles until they are in increasing order with the blank " \
            "in the last space.\nPress space to restart." \
            "\n\n(Press any key or click to return)"
        blit_text(window, instructions, (20, 20), self.font_24,
                  color=pygame.color.Color(255, 255, 255))

    def instructions(self, window):
        run = True
        while run:
            pygame.time.Clock().tick(60)
            window.fill((0, 0, 0))
            self.draw_instructions(window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    run = False
                elif event.type == pygame.KEYUP:
                    run = False
            pygame.display.update()

    def draw_solved(self, window):
        pass

    def solved(self, game_board):
        game_board.update_best()
        self.draw_solved(self.window)
