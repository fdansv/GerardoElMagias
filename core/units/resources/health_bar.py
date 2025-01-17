from pygame import draw
from constants.basic_colors import *


class HealthBar:
    def __init__(self, x, y, current_hp, max_hp):
        self.x = x
        self.y = y

        self.max_hp = max_hp
        self.current_hp = current_hp

    def draw(self, hp, max_hp, screen):
        # Update: HealthBar Status
        self.max_hp = max_hp
        self.current_hp = hp
        ratio = self.current_hp / self.max_hp
        draw.rect(screen, GRAY_COLOR, (self.x, self.y, 130, 10))
        draw.rect(screen, GREEN_COLOR, (self.x, self.y, 130 * ratio, 10))

