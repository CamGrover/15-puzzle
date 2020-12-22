from events import TickEvent, QuitEvent
import pygame


class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def notify(self, event, event_manager):
        if isinstance(event, TickEvent):
            # Handle input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_manager.post(QuitEvent())
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    moves = self.model.get_viable_moves()
                    pos = pygame.mouse.get_pos()
                    if self.view.instructions_btn.collidepoint(pos):
                        self.view.instructions()
                        break
                    for tile in moves:
                        if tile.box.collidepoint(pos):
                            self.model.move(self.model.tiles.index(tile))
                            break
                    if self.model.check_solved():
                        self.model.update_best()
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        self.model.restart()
                self.view.draw(self.model)
                pygame.display.update()
