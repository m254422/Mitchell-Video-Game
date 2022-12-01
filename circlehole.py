import pygame
from random import randint

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TEXTCOLOR = (0, 0, 0)
(width, height) = (200, 300)

running = True


def main():
    global running, screen

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("TUFF")
    screen.fill(GREEN)
    pygame.display.update()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                _update_screen(screen)  # clear screen to the original screen
                w, h = pygame.display.get_surface().get_size()  # get screen width and height
                pos_x, pos_y = randint(0, w), randint(0, h)  # generate random x and y position
                print(f"pos_x={pos_x}, pos_y={pos_y}")
                my_circle = pygame.draw.circle(screen, (0, 0, 255), (pos_x, pos_y), 20)  # draw circle
                pygame.display.update()

            if event.type == pygame.QUIT:
                running = False


def _update_screen(screen):
    """Update images on the screen, and flip to the new screen."""
    screen.fill(GREEN)

    pygame.display.flip()


if __name__ == '__main__':
    main()