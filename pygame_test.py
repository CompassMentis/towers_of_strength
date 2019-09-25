# Testing out pyGame's SCALED property
import pygame
from spritesheet import SpriteSheet, Origin
import time

canvas = pygame.display.set_mode((200, 200))

# Test animation
sprites = SpriteSheet('images/runners/heroine_animated.png', columns=32, rows=8, colour_key=pygame.Color(127, 127, 127))
# sprites = SpriteSheet('images/runners/hero_animated.png', columns=32, rows=8, colour_key=pygame.Color(127, 127, 127))

while True:
    # Direction = 0: Move W
    # Direction = 1: Move NW
    # Direction = 2: Move N
    # etc
    for direction in range(8):
        for i in range(4, 12):
            canvas.fill((255, 255, 255))
            sprites.blit(canvas, direction * 32 + i, position=(50, 50), origin=Origin.TopLeft)
            pygame.display.flip()
            time.sleep(0.2)

while True:
    pass
