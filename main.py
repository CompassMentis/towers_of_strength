import pygame

from settings import Settings
from game import Game

canvas = pygame.display.set_mode((Settings.canvas_width, Settings.canvas_height))

game = Game(canvas)

clock = pygame.time.Clock()
while True:
    game.draw()
    game.tick()
    clock.tick(Settings.clock_speed)
