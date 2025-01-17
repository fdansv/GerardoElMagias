from core.units.resources.mana_bar import ManaBar
from core.units.resources.stash import Stash

from core.units.skills.magic import MagicSpells
from core.units.skills.melee import MeleeSpells
from core.units.skills.fury import FurySpells

from core.units.resources.fury_bar import FuryBar
from core.units.mechanics.experience import ExperienceSystem

from core.units.combat.utils import get_alive_targets_status
from random import randint
from core.text.combat_text_resolver import CombatTextResolver
from core.text.damage_text import DamageText

from constants.sound import *
import constants.globals

from core.units.mechanics.loot import LootPool
from core.units.basic_unit import BasicUnit
from core.units.resources.health_bar import HealthBar

# Text Import
from random import randint

# Combat Imports
from core.units.combat.combat_formulas import CombatFormulas
from core.units.combat.combat_resolver import CombatResolver

# Animation Imports
from core.units.animations.animation_db import HeroSet
from core.units.animations.animation_set import AnimationSet

import constants.globals

combat_resolver = CombatResolver()
combat_formulas = CombatFormulas()


# Init: Damage Text, CombatTextResolver
damage_text = DamageText()
combat_text_resolver = CombatTextResolver()


class HeroPlayer(BasicUnit, MeleeSpells, MagicSpells, FurySpells, AnimationSet):
    def __init__(self, x, y, name, level, max_hp, max_mp, strength, dexterity, magic, healing_potion, magic_potion, gold, health_bar_x, health_bar_y, mana_bar_x, mana_bar_y, fury_bar_x, fury_bar_y):
        BasicUnit.__init__(self, x, y, name, level, max_hp, max_mp, strength, dexterity, magic)
        FurySpells.__init__(self)
        MeleeSpells.__init__(self)
        MagicSpells.__init__(self)

        self.animation_set = AnimationSet(x, y, name, HeroSet)

        self.health_bar = HealthBar(health_bar_x, health_bar_y, self.current_hp, self.max_hp)
        self.mana_bar = ManaBar(mana_bar_x, mana_bar_y, self.current_mp, self.max_mp)
        self.fury_bar = FuryBar(fury_bar_x, fury_bar_y, self.current_fury, self.max_fury)
        self.stash = Stash(healing_potion, magic_potion, gold)

        self.experience_system = ExperienceSystem()

        self.current_fury = 0
        self.experience = 0
        self.exp_level_break = 5
        self.fury_status = True
        self.experience_status = True

    def attack(self, target, damage_text_group):
        self.melee_attack_animation()
        self.cast_attack(self, target, damage_text_group)
        return True

    def loot(self, target, damage_text_group):
        target.loot_pool.get_loot(self, target, damage_text_group)

    def loot_boss(self, target, damage_text_group):
        target.loot_pool.get_loot_boss(self, target, damage_text_group)

    def use_ultimate(self, target_list, damage_text_group):
        self.cast_path_of_the_seven_strikes(self, target_list, damage_text_group)
        return True

    def use_heal(self, damage_text_group):
        # Consume Mana: Spell Casting
        if self.reduce_mana(12):
            constants.globals.action_cooldown = -30
            constants.globals.current_fighter += 1
            self.cast_heal(self, self, damage_text_group)
            return True

        damage_text.warning(self, ' No Enough Mana! ', damage_text_group)
        return False

    def use_firestorm(self, target_list, damage_text_group):
        # Consume Mana: Spell Casting
        print('Turn:', constants.globals.current_fighter)
        if self.reduce_mana(15):
            constants.globals.action_cooldown = -30
            constants.globals.current_fighter += 1

            # Pre Save State for Enemy List: target_list
            pre_target_list = get_alive_targets_status(target_list)

            # Retrieve State for Enemy List: target_list
            self.cast_firestorm(self, target_list, damage_text_group)

            # Post Save State for Enemy List: target_list
            pos_target_list = get_alive_targets_status(target_list)

            # Evaluate Kills
            self.experience_system.evaluate_group_kill(self, target_list, pre_target_list, pos_target_list,
                                                       damage_text_group)
            print('Turn:', constants.globals.current_fighter)
            return True

        damage_text.warning(self, ' No Enough Mana! ', damage_text_group)
        return False

    def use_lightning(self, target_list, damage_text_group):
        # Consume Mana: Spell Casting
        if self.reduce_mana(20):
            constants.globals.action_cooldown = -30
            constants.globals.current_fighter += 1
            # Save State for Enemy List: target_list
            pre_target_list = get_alive_targets_status(target_list)

            self.cast_lightning(self, target_list, damage_text_group)
            # Retrieve State for Enemy List: target_list
            pos_target_list = get_alive_targets_status(target_list)

            # Evaluate Kills
            self.experience_system.evaluate_group_kill(self, target_list, pre_target_list, pos_target_list,
                                                       damage_text_group)
            return True

        damage_text.warning(self, ' No Enough Mana! ', damage_text_group)
        return False

    def use_healing_potion(self, damage_text_group):
        if self.stash.has_healing_potion():
            constants.globals.action_cooldown = 0
            constants.globals.current_fighter += 1

            health_potion_sound.play()

            base_health = 40
            health_interval = randint(0, 10)
            base_health_multiplier = (self.level * 4)
            health_recover = base_health + health_interval + base_health_multiplier

            self.stash.consume_healing_potion()
            gained_health = self.gain_health(health_recover)

            damage_text.heal(self, str(gained_health), damage_text_group)
            return True

        damage_text.warning(self, 'No Healing Potions', damage_text_group)
        error_sound.play()
        return False

    def use_mana_potion(self, damage_text_group):
        if self.stash.has_mana_potion():
            constants.globals.action_cooldown = 0
            constants.globals.current_fighter += 1

            health_potion_sound.play()
            base_mana = 15
            mana_interval = randint(0, 5)
            base_mana_multiplier = (self.level * 2)
            mana_recover = base_mana + mana_interval + base_mana_multiplier

            self.stash.consume_mana_potion()
            gained_mana = self.gain_mana(mana_recover)

            damage_text.mana(self, str(gained_mana), damage_text_group)
            return True

        damage_text.warning(self, 'No Mana Potions', damage_text_group)
        error_sound.play()
        return False

    def death_animation(self):
        # Activates: Death Animation
        self.animation_set.action = 1
        self.animation_set.reset_frame_index()

    def melee_attack_animation(self):
        # Activates: Melee Attack Animation
        self.animation_set.action = 2
        self.animation_set.reset_frame_index()

    def hurt_animation(self):
        # Activates: Hurt Animation
        self.animation_set.action = 3
        self.animation_set.reset_frame_index()

    def block_animation(self):
        # Activates: Block Animation
        self.animation_set.action = 4
        self.animation_set.reset_frame_index()

    def miss_animation(self):
        # Activates: Miss Animation
        self.animation_set.action = 5
        self.animation_set.reset_frame_index()