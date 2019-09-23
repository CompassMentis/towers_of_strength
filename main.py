import pygame
import time

from settings import Settings
from game import Game

canvas = pygame.display.set_mode((Settings.canvas_width, Settings.canvas_height))

game = Game(canvas)
game.draw()
while True:
    time.sleep(1)
