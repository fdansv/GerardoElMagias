from core.game_units.unit_class.melee.melee_figher import MeleeFighter
from core.game_units.unit_mechanic.loot_pool import LootPool
from core.game_units.basic_unit import BasicUnit
from core.game_units.unit_mechanic.health_bar import HealthBar

from core.game_text.combat_text_resolver import CombatTextResolver
from core.game_text.damage_text import DamageText
from constants.sound import *

# Init: Damage Text, CombatTextResolver
damage_text = DamageText()
combat_text_resolver = CombatTextResolver()


class Bandit(BasicUnit, MeleeFighter):
    def __init__(self, x, y, name, level, max_hp, max_mp, strength, dexterity, magic, health_bar_x, health_bar_y):
        BasicUnit.__init__(self, x, y, name, level, max_hp, max_mp, strength, dexterity, magic)
        MeleeFighter.__init__(self)
        self.health_bar = HealthBar(health_bar_x, health_bar_y, self.current_hp, self.max_hp)
        # Bandit Loot
        self.looted_status = False
        self.loot_pool = LootPool()

    def is_looted(self):
        if self.looted_status:
            return True
        return False

    def update_looted_status(self):
        self.looted_status = True

    def attack(self, target, damage_text_group):
        # Get Damage, Message, Color for current Attack
        output_damage, output_message = self.cast_attack(self)

        # Activates Attack Animation: Bandit -> MeleeFighter
        self.melee_attack()

        # Activates Blocked Animation on Target
        if 'Blocked' in output_message:
            target.block()
            block_sound.play()

        if 'Miss' in output_message:
            # Todo: Get miss animation
            target.miss()
            miss_sound.play()

        # Activates Hurt/Death Animation on Target
        else:
            # Activates Critical Hit Sound
            if 'Critical' in output_message:
                critical_hit_sound.play()

            if output_damage != 0:
                # Updates current Target Health
                target.reduce_health(output_damage)

                # Updates current Target Fury
                target.gain_fury(output_damage)

                # Activates Hurt Animation: Target
                target.hurt()
                hit_cut_sound.play()

                #Activates hurt sound

                # Evaluate Death: Target
                if target.is_dead():
                    target.death()

        combat_text_resolver.resolve(target, str(output_damage) + output_message, damage_text_group)
        return True
