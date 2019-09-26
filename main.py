import pygame
import sys

from settings import Settings
from game import Game

canvas = pygame.display.set_mode((Settings.canvas_width, Settings.canvas_height))

game = Game(canvas)

clock = pygame.time.Clock()
while True:
    game.draw()
    game.tick()
    clock.tick(Settings.clock_speed)

    # Events could be placed on the pygame-queue by either pygame itself, or by
    # one of our in-game entities. Process all currently available events.
    if pygame.event.peek():

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
                    for tower in game.towers:
                        tower.handle_mouse_event(event)
                elif event.type == pygame.USEREVENT:
                    print(event)
