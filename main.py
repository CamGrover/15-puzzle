import os
import pygame
from game_board import GameBoard
from interface import Interface
import constants
from my_game import win, interface, pygame, game_board, clock


def redraw_game_window():
    win.fill((0, 0, 0))
    interface.draw(win, game_board)
    pygame.display.update()


def main():
    # game_board.mix_up([3, 1, 2, 5, 4, 6, 8, 7, 9, 13, 12, 11, 10, 15, 16, 14])
    game_board.restart()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                moves = game_board.get_viable_moves()
                pos = pygame.mouse.get_pos()
                for tile in moves:
                    if tile.box.collidepoint(pos):
                        # print(tile.number)
                        game_board.move(game_board.tiles.index(tile))
                        break

                if interface.instructions_btn.collidepoint(pos):
                    interface.instructions(win)

                game_board.check_solved()
                if game_board.is_solved:
                    interface.solved(game_board)

                    print(f"Congratulations!!! Completed in {game_board.moves} "
                          f"moves.")
                    print(game_board.history)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    game_board.restart()
        # keys = pygame.key.get_pressed()

        redraw_game_window()

    pygame.quit()


if __name__ == "__main__":
    main()
