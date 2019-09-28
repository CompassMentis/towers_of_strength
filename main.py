import pygame
import sys
import time

from settings import Settings
from game import Game

pygame.init()
canvas = pygame.display.set_mode((Settings.canvas_width, Settings.canvas_height))

game = Game(canvas)

# game.draw()
# while True:
#     time.sleep(1)

clock = pygame.time.Clock()
while True:
    game.draw()
    game.tick()
    clock.tick(Settings.clock_speed)

    # Events could be placed on the pygame-queue by either pygame itself, or by
    # one of our in-game entities. Process all currently available events.
    # if pygame.event.peek():
    #
        # Does the user want to pack up and leave?
    if pygame.event.get(eventtype=pygame.QUIT):
        sys.exit(0)

    else:
        events = pygame.event.get()
        for event in events:
            # Mouse Interactions
            if event.type in [
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION,
            ]:
                game.handle_mouse_event(event)
                # pass
                # for tower in game.towers:
                #     tower.handle_mouse_event(event)

            elif event.type == pygame.USEREVENT:
                print(event)

            else:
                pass
