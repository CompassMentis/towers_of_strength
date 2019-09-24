# Testing out pyGame's SCALED property
import pygame
from spritesheet import SpriteSheet, Origin
import time

canvas = pygame.display.set_mode((1020, 700))

# Test animation
sprites = SpriteSheet('images/runners/heroine_animated.png', columns=32, rows=8, colour_key=pygame.Color(127, 127, 127))

for i in range(32 * 8):
    canvas.fill((255, 255, 255))
    sprites.blit(canvas, i, position=(50, 50), origin=Origin.TopLeft)
    pygame.display.flip()
    time.sleep(0.2)

while True:
    pass
