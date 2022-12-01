# settings class code
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 400
        self.screen_height = 600
        self.bg_color = (0, 230, 0)

        # Ship settings
        self.ship_speed = 0 #1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 0.2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 100

        self.alien_frequency = 0.015
        self.alien_speed = 0