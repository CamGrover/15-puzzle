import os
import json
from tile import Tile
from verify_solution import verify
from constants import FILENAME


def rect_position(i):
    width = 64
    height = 64
    x = width * (i % 4)
    y = height * (i // 4)
    return x, y


class BestScore:
    def __init__(self, best_score=0, history=None, start=None, goal=None):
        if goal is None:
            goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.best_score = best_score
        self.history = history
        self.start = start
        self.goal = goal

    # Source:
    # Visha. Make a Python Class JSON Serializable. PYnative
    # https://pynative.com/make-python-class-json-serializable/
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


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
        self.init_best_score()

    def idx_blank(self):
        return self.tiles.index(self.blank)
        # return self.tiles.index(next(filter(
        #     lambda a: a.number == 16, self.tiles)))

    def get_viable_moves(self) -> []:
        if self.disabled:
            return []
        blank_idx = self.idx_blank()
        moves = []
        if blank_idx % 4 > 0:
            moves.append(self.tiles[blank_idx - 1])
        if blank_idx % 4 < 3:
            moves.append(self.tiles[blank_idx + 1])
        if blank_idx > 3:
            moves.append(self.tiles[blank_idx - 4])
        if blank_idx < 12:
            moves.append(self.tiles[blank_idx + 4])
        return moves

    def swap(self, a, b):
        # Swap pygame.Rect box for placement
        self.tiles[a].box, self.tiles[b].box = \
            self.tiles[b].box, self.tiles[a].box
        # Swap tiles to change list indexes
        self.tiles[a], self.tiles[b] = \
            self.tiles[b], self.tiles[a]

    def move(self, tile_idx):
        self.history.append(self.tiles[tile_idx].number)
        self.swap(self.idx_blank(), tile_idx)
        # Update game counters
        self.moves += 1

    def check_solved(self):
        solved = True
        for i in range(0, 16):
            if self.goal[i] != self.tiles[i].number:
                solved = False
                break
        self.is_solved = solved
        if solved:
            self.disabled = True
        return solved

    def mix_up(self, mix_order):
        self.start = mix_order
        try:
            for i in range(0, 16):
                j = self.tiles.index(next(filter(
                    lambda a: a.number == mix_order[i], self.tiles)))
                self.swap(i, j)
        except StopIteration:
            print(StopIteration)

    def restart(self):
        self.mix_up(
            [7, 15, 6, 2, 1, 9, 11, 4, 5, 13, 12, 3, 14, 10, 8, 16])
        self.is_solved = False
        self.moves = 0
        self.disabled = False
        self.history = []

    def update_best(self):
        if self.is_solved and self.moves < self.best_score.best_score:
            self.best_score = BestScore(
                self.moves, self.history, self.start, self.goal)
        try:
            with open(FILENAME, 'w') as file:
                file.write(self.best_score.toJson())
        except FileNotFoundError:
            print("Cannot write to score file")

    def get_best_score(self):
        return self.best_score.best_score

    def set_default_best_score(self):
        self.best_score = BestScore(
            106,
            [
                8, 10, 13, 9, 15, 7, 1, 15, 11, 6, 2, 4, 6, 12, 3, 6, 12, 3,
                9, 11, 7, 2, 3, 7, 15, 5, 11, 15, 7, 12, 6, 9, 12, 6, 9, 8,
                10, 13, 15, 7, 6, 12, 7, 15, 13, 10, 8, 7, 12, 9, 7, 8, 10,
                12, 9, 7, 8, 10, 12, 13, 15, 11, 14, 15, 13, 9, 11, 13, 9,
                11, 11, 9, 15, 14, 13, 15, 9, 11, 15, 9, 14, 13, 9, 15, 10,
                12, 11, 14, 15, 10, 14, 11, 12, 14, 11, 15, 10, 11, 14, 12,
                15, 14, 11, 10, 14, 15
            ],
            [7, 15, 6, 2, 1, 9, 11, 4, 5, 13, 12, 3, 14, 10, 8, 16],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        )

    def init_best_score(self):
        try:
            # Attempt ot create new file
            with open(FILENAME, 'x') as file:
                self.set_default_best_score()
                file.write(self.best_score.toJson())
                file.close()

        except FileExistsError:
            try:
                with open(FILENAME, 'r') as file:
                    score_json = file.readline()
                    self.best_score = BestScore()
                    # self.best_score.__dict__ = json.loads(score_json)
                    best_score = BestScore()
                    best_score.__dict__ = json.loads(score_json)
                    if verify(best_score.best_score, best_score.history,
                              best_score.start, best_score.goal):
                        self.best_score = best_score
                        print("Verified")
                    else:
                        self.set_default_best_score()
                        print("Score import failed")
            except FileNotFoundError:
                pass
