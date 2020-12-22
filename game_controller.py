import pygame
import json
from verify_solution import verify
from constants import FILENAME
from events import TickEvent, QuitEvent
from best_score import BestScore


class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.init_best_score()
        self.restart()

    def get_viable_moves(self) -> []:
        if self.model.disabled:
            return []
        blank_idx = self.model.idx_blank()
        moves = []
        if blank_idx % 4 > 0:
            moves.append(self.model.tiles[blank_idx - 1])
        if blank_idx % 4 < 3:
            moves.append(self.model.tiles[blank_idx + 1])
        if blank_idx > 3:
            moves.append(self.model.tiles[blank_idx - 4])
        if blank_idx < 12:
            moves.append(self.model.tiles[blank_idx + 4])
        return moves

    def swap(self, a, b):
        # Swap pygame.Rect box for placement
        self.model.tiles[a].box, self.model.tiles[b].box = \
            self.model.tiles[b].box, self.model.tiles[a].box
        # Swap tiles to change list indexes
        self.model.tiles[a], self.model.tiles[b] = \
            self.model.tiles[b], self.model.tiles[a]

    def move(self, tile_idx):
        self.model.history.append(self.model.tiles[tile_idx].number)
        self.swap(self.model.idx_blank(), tile_idx)
        # Update game counters
        self.model.moves += 1

    def check_solved(self):
        solved = True
        for i in range(0, 16):
            if self.model.goal[i] != self.model.tiles[i].number:
                solved = False
                break
        self.model.is_solved = solved
        if solved:
            self.model.disabled = True
        return solved

    def mix_up(self, mix_order):
        self.model.start = mix_order
        try:
            for i in range(0, 16):
                j = self.model.tiles.index(next(filter(
                    lambda a: a.number == mix_order[i], self.model.tiles)))
                self.swap(i, j)
        except StopIteration:
            print(StopIteration)

    def restart(self):
        self.mix_up(
            [7, 15, 6, 2, 1, 9, 11, 4, 5, 13, 12, 3, 14, 10, 8, 16])
        self.model.is_solved = False
        self.model.moves = 0
        self.model.disabled = False
        self.model.history = []

    def set_default_best_score(self):
        self.model.best_score = BestScore(
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
                file.write(self.model.best_score.toJson())
                file.close()

        except FileExistsError:
            try:
                with open(FILENAME, 'r') as file:
                    score_json = file.readline()
                    # self.model.best_score = BestScore()
                    # self.best_score.__dict__ = json.loads(score_json)
                    best_score = BestScore()
                    best_score.__dict__ = json.loads(score_json)
                    if verify(best_score.best_score, best_score.history,
                              best_score.start, best_score.goal):
                        self.model.best_score = best_score
                        print("Verified")
                    else:
                        self.set_default_best_score()
                        print("Score import failed")
            except FileNotFoundError:
                pass

    def update_best(self):
        if self.model.is_solved \
                and self.model.moves < self.model.best_score.best_score:
            self.model.best_score = BestScore(
                self.model.moves,
                self.model.history,
                self.model.start,
                self.model.goal
            )
        try:
            with open(FILENAME, 'w') as file:
                file.write(self.model.best_score.toJson())
        except FileNotFoundError:
            print("Cannot write to score file")

    def notify(self, event, event_manager):
        if isinstance(event, TickEvent):
            # Handle input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    event_manager.post(QuitEvent())
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    moves = self.get_viable_moves()
                    pos = pygame.mouse.get_pos()
                    if self.view.instructions_btn.collidepoint(pos):
                        self.view.instructions()
                        break
                    for tile in moves:
                        if tile.box.collidepoint(pos):
                            self.move(self.model.tiles.index(tile))
                            break
                    if self.check_solved():
                        self.update_best()
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        self.restart()
                self.view.draw(self.model)
                pygame.display.update()
