import sys
import pygame
import sys
import pygame
import sys

import pygame

from settings3 import Settings
from ship2 import Ship
from button import Button
from background import Background1
from bullet import Bullet
from scoreboard import Scoreboard
from gamestats import GameStats
from random import randint
from hole import Hole
from pygame.locals import *
from pygame import mixer


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((400, 600))  # , pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.background1 = Background1(self)

        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.hole = Hole(self)
        self.sb = Scoreboard(self)
        self.bullets = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.play_game = False
        self.show_instructions = False
        self.show_start = True

        pos_x = randint(0, self.screen.get_rect().width - self.hole.radius)
        pos_y = randint(0, int(0.1 * self.screen.get_rect().height))
        self.pos = [pos_x, pos_y]

        self.angle = randint(88, 90)
        mixer.init()
        mixer.music.load('music/bensound-summer_mp3_music.mp3')
        mixer.music.play()

        self.play_button = Button(self, "Play")
            ##Music help from Ally Edelman

    def update_pos(self):
        pos_x = randint(0, self.screen.get_rect().width - self.hole.radius)
        pos_y = randint(0, int(0.1 * self.screen.get_rect().height))
        self.pos = [pos_x, pos_y]
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            # self._check_bullet_hole_collisions()
            if self.play_game:
                self.game()


            # self.ship.update()
            # self._update_bullets()
            elif self.show_instructions:
                self.instructions()
            elif self.show_start:
                self.start_screen()
            # self._update_screen()

    def start_screen(self):
        self.screen.fill((0, 0, 0))
        start = pygame.image.load("images/start.png")
        start = pygame.transform.scale(start, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(start,(0,0))
        pygame.display.flip()

    def instructions(self):
        self.screen.fill((0,0,0))
        instructions = pygame.image.load("images/instructions.png")
        instructions = pygame.transform.scale(instructions, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(instructions, (0,0))
        pygame.display.flip()

    def game(self):

        self._check_events()
        self.ship.update()
        self._update_bullets()
        self.hole.update()
        self._update_screen()
        self._check_bullet_hole_collisions()
        # self.show_score()
        # self.show_level()
        # self.show_high_score()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            self.settings.initialize_dynamic_settings()

                # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()

            self.holes.empty()
            self.bullets.empty()


            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_i:
            self.show_instructions = True
        elif event.key == pygame.K_p:
            self.play_game = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            # self._fire_ball()
            #pygame.K_SPACE help from Viva Mulhall

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
            mixer.music.load('music/Swing.mp3')
            mixer.music.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update(self.ship)

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                self.stats.score -= 50
                self.sb.prep_score()
                mixer.music.load('music/sad-crowd-aww-sound-effect-By-Tuna.mp3')
                mixer.music.play()
            if bullet.rect.left <= 0:
                self.bullets.remove(bullet)
                self.bullets.remove(bullet)
                self.stats.score -= 50
                self.sb.prep_score()
                mixer.music.load('music/sad-crowd-aww-sound-effect-By-Tuna.mp3')
                mixer.music.play()
            if bullet.rect.right >= self.screen.get_rect().right:
                self.bullets.remove(bullet)
                self.bullets.remove(bullet)
                self.stats.score -= 50
                self.sb.prep_score()
                mixer.music.load('music/sad-crowd-aww-sound-effect-By-Tuna.mp3')
                mixer.music.play()

    def _check_bullet_hole_collisions(self):
        """Respond to bullet-alien collisions."""
        self.holes.add(self.hole)
        # check any bullets and hole have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.holes, True, True) #(self.hole.circ_rect, self.bullets)
        if collisions:
            self.stats.score += 100
            self.sb.prep_score()
            self.sb.check_high_score()
            self.stats.level += 1
            self.update_pos()
            self.settings.bullet_speed += 0.2
            self.sb.prep_level()
            mixer.music.load('music/golfball.mp3')
            mixer.music.play()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.blit(pygame.transform.scale(self.background1.image, (self.settings.screen_width, self.settings.screen_height)), (0, 0))
        self.ship.blitme()
        self.hole.update_hole(self.pos, self.stats.level)
        self.sb.show_score()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':

    ai = AlienInvasion()
    ai.run_game()