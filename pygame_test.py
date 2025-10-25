#!/usr/bin/env python

import pygame
import time

def main(width: int, height: int):
    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game Test")
    font = pygame.font.SysFont(None, 30)

    # clock for FPS control
    clock = pygame.time.Clock()

    # loop
    fps = 0
    frames = 0
    last = time.time()
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
        # fps counter
        frames += 1
        if (time.time() - last >= 1.0):
            fps = frames
            frames = 0
            last = time.time()
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        # Limit fps
        # clock.tick(60)

        # Update display
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main(800, 600)
