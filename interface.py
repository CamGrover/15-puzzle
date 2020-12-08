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

    def draw(self, game_board):
        # Define colors
        black = pygame.color.Color(0, 0, 0)
        white = pygame.color.Color(255, 255, 255)
        # Generate text
        moves = self.font_24.render(
            f"Moves: {game_board.moves}", True, white, black)
        best_score = self.font_24.render(
            f"Best: {game_board.get_best_score()}", True, white, black)
        instructions_1 = self.font_24.render(
            "Show Instructions",
            True, black, white
        )
        # Draw window
        self.window.blit(moves, self.moves_used_box)
        self.window.blit(best_score, self.best_score)
        self.window.blit(instructions_1, self.instructions_btn)
        game_board.draw(self.window)
        if game_board.is_solved:
            self.draw_solved(game_board.best_score.best_score,
                             game_board.moves)

    def draw_instructions(self):
        instructions = \
            "Slide tiles until they are in increasing order with the blank " \
            "in the last space.\nPress (space) to restart." \
            "\n\n(Press any key or click to return)"
        blit_text(self.window, instructions, (20, 20), self.font_24,
                  color=pygame.color.Color(255, 255, 255))

    def instructions(self, window):
        run = True
        while run:
            pygame.time.Clock().tick(60)
            window.fill((0, 0, 0))
            self.draw_instructions()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    run = False
                elif event.type == pygame.KEYUP:
                    run = False
            pygame.display.update()

    def draw_solved(self, best: int, moves: int):
        rect = pygame.Rect(0, 64, 256, 128)
        if moves < best:
            text = f"Congratulations!!! You beat the best score of {best}. " \
                   f"New best solution is {moves}."
        else:
            text = f"Nice try! Solution took {moves} moves. Current best is " \
                   f"{best}."
        text += "\nPress (space) to play again."
        self.window.fill((0, 0, 0), rect=rect)
        blit_text(self.window, text, (20, 70), self.font_24,
                  color=pygame.Color('white'))
        pygame.display.update()
