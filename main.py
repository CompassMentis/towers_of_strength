import pygame
import time

from settings import Settings
from game import Game

canvas = pygame.display.set_mode((Settings.canvas_width, Settings.canvas_height))

print(Settings.cell_width, Settings.cell_height)

game = Game(canvas)
while True:
    game.draw()
    time.sleep(1)
    game.tick()
