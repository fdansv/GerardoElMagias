from core.units.spells.melee_skills import MeleeFighter
from core.units.unit_mechanic.loot_pool import LootPool
from core.units.basic_unit import BasicUnit
from core.units.resources.health_bar import HealthBar
from floating_text import CombatTextResolver
from core.text.damage_text import DamageText

from core.units.combat.mage_formulas import MageFighter

# Init: Damage Text, CombatTextResolver
damage_text = DamageText()
combat_text_resolver = CombatTextResolver()

class FireMage(BasicUnit, MageFighter, MeleeFighter):
    def __init__(self, x, y, name, level, max_hp, max_mp, strength, dexterity, magic, health_bar_x, health_bar_y):
        BasicUnit.__init__(self, x, y, name, level, max_hp, max_mp, strength, dexterity, magic)
        MeleeFighter.__init__(self)
        self.health_bar = HealthBar(health_bar_x, health_bar_y, self.current_hp, self.max_hp)
        # Bandit Loot
        self.looted_status = False
        self.loot_pool = LootPool()

        self.damage_spells = DamageSpells()

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

        if 'Miss' in output_message:
            # Todo: Get miss animation
            target.block()

        # Activates Hurt/Death Animation on Target
        else:
            if output_damage != 0:
                # Updates current Target Health
                target.reduce_health(output_damage)

                # Updates current Target Fury
                target.gain_fury(output_damage)

                # Activates Hurt Animation: Target
                target.hurt()

                # Evaluate Death: Target
                if target.is_dead():
                    target.death()

        combat_text_resolver.resolve(target, str(output_damage) + output_message, damage_text_group)
        return True
