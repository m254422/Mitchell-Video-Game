from random import randint

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/hole.png')
        self.rect = self.image.get_rect()

        alien_top_max = self.settings.screen_height - self.rect.height
        self.rect.midtop = self.screen_rect.midtop

        self.x = float(self.rect.x)

    def update(self):
        """Move the alien steadily to the left."""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x
