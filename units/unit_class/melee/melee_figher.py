from random import randint
from constants.basic_colors import *


class MeleeFighter:
    HIT = ' Hit! '
    CRITICAL_HIT = ' Critical Hit ! '
    MISS = ' Miss ! '

    @staticmethod
    def critical_hit(base_damage, multiplier=2):
        return base_damage * multiplier

    @staticmethod
    def critical_chance(hit_change, dexterity):
        if hit_change < dexterity:
            return True
        return False

    @staticmethod
    def miss_chance(hit_change, dexterity):
        if hit_change > (80 + dexterity):
            return True
        return False

    @staticmethod
    def hit_chance():
        return randint(0, 99)

    def cast_attack(self, caster):
        # Calculate Basic Damage: Based on Strength
        base_damage = caster.strength + randint(0, 6)

        # Calculate Hit Change: Based on Random Integer
        hit_chance = self.hit_chance()

        # Calculate Miss, Basic Damage & Critical Hit
        if not self.miss_chance(hit_chance, caster.dexterity):
            if self.critical_chance(hit_chance, caster.dexterity):
                return self.critical_hit(base_damage), self.CRITICAL_HIT, RED_COLOR
            return base_damage, self.HIT, RED_COLOR
        return 0, self.MISS, WHITE_COLOR