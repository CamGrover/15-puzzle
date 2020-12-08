from my_game import win, interface, pygame, game_board, clock


def redraw_game_window():
    win.fill((0, 0, 0))
    interface.draw(game_board)
    pygame.display.update()


def main():
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
                if interface.instructions_btn.collidepoint(pos):
                    interface.instructions(win)
                    break
                for tile in moves:
                    if tile.box.collidepoint(pos):
                        game_board.move(game_board.tiles.index(tile))
                        break
                if game_board.check_solved():
                    game_board.update_best()
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    game_board.restart()
        redraw_game_window()
    pygame.quit()


if __name__ == "__main__":
    main()
