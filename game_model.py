import os
from best_score import BestScore
from tile import Tile


def rect_position(i):
    width = 64
    height = 64
    x = width * (i % 4)
    y = height * (i // 4)
    return x, y


class GameModel:
    def __init__(self):
        self.disabled = False
        self.is_solved = False
        self.moves = 0
        self.history = []
        self.start = []
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.tiles = []
        for i in range(0, 16):
            image = os.path.join("imgs", "tile_" + str(i + 1) + ".png")
            x, y = rect_position(i)
            self.tiles.append(Tile(i + 1, image, x, y))
        self.blank = self.tiles[15]
        self.best_score = BestScore()

    def idx_blank(self):
        return self.tiles.index(self.blank)

    def get_best_score(self):
        return self.best_score.best_score
