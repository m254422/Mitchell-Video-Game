import sys
import pygame
import sys

import pygame

from settings import Settings
from ship2 import Ship
from bullet import Bullet
from alien import Hole


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((400, 600))#, pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.holes = pygame.sprite.Group()
        self._create_holes()
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update(self.ship)

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
            if bullet.rect.left <= 0:
                 self.bullets.remove(bullet)
            if bullet.rect.right >= self.screen.get_rect().right:
                 self.bullets.remove(bullet)

    def _create_holes(self):
        """Create a sky full of stars."""

        hole = Hole(self)
        hole_width, hole_height = hole.rect.size
        available_space_x = self.settings.screen_width - hole_width
        number_holes_x = number_holes_x = available_space_x // (2 * hole_width)


        available_space_y = (self.settings.screen_height -
                             (2 * hole_height))
        number_rows = available_space_y // (2 * hole_height)

        for row_number in range(number_rows):
            for hole_number in range(number_holes_x):
                self._create_hole(hole_number, row_number)

    def _create_hole(self, hole_number, row_number):
        """Create an star and place it in the row."""
        hole = Hole(self)
        hole_width, hole_height = hole.rect.size
        hole.rect.x = hole_width + 2 * hole_width * hole_number
        hole.rect.y = hole.rect.height + 2 * hole.rect.height * row_number


        hole.rect.x += randint(-5, 5)
        hole.rect.y += randint(-5, 5)

        self.holes.add(hole)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.holes.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()