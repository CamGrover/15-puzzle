import pygame
from game_board import GameBoard
from interface import Interface
from constants import WIN_WIDTH, WIN_HEIGHT

pygame.init()

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("The 15 Puzzle")
clock = pygame.time.Clock()
game_board = GameBoard()
interface = Interface(win)
