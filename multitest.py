#!/usr/bin/env python

import pygame

def main(width: int, height: int):
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game Test")

    # clock for FPS control
    clock = pygame.time.Clock()

    # loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # get current mouse position
        x, y = pygame.mouse.get_pos()


        # --- Drawing ---
        # Fill screen with dark grey
        screen.fill((30,30,30))
        # Draw circle as cyan circle
        pygame.draw.circle(screen, (0, 200, 255),  (x, y), 10)



        # Update display
        pygame.display.flip()

        # Limit to 60 frames per second
        # clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main(800, 600)
