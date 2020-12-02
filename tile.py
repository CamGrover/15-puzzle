import pygame


class Tile:
    def __init__(self, number, sprite, x, y):
        self.number = number
        self.box = pygame.Rect(x, y, 64, 64)
        self.image = pygame.image.load(sprite)

    def draw(self, window):
        window.blit(self.image, self.box)