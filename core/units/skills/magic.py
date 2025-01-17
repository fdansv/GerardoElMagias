from random import randint
from core.units.combat.combat_formulas import CombatFormulas
from core.units.combat.combat_resolver import CombatResolver
from core.units.combat.utils import get_alive_targets
from core.text.combat_text_resolver import CombatTextResolver
from core.text.damage_text import DamageText

# Init: Damage Text
combat_text_resolver = CombatTextResolver()
damage_text = DamageText()


class MagicSpells(CombatFormulas, CombatResolver):
    def __init__(self):
        CombatResolver.__init__(self)
        CombatFormulas.__init__(self)

    @staticmethod
    def cast_heal(caster, target, damage_text_group):
        # Todo: Init proper 150x, 400y
        damage_text.cast(caster, "Heal", damage_text_group)

        base_heal = 1 + randint(0, 10) + (caster.magic * 5)
        if target.max_hp - target.current_hp > base_heal:
            heal_amount = base_heal
        else:
            heal_amount = target.max_hp - target.current_hp
        target.current_hp += heal_amount

        # Todo: Init proper 150x, 500y
        damage_text.heal(caster, str(heal_amount) + " Heal ", damage_text_group)

    def cast_firestorm(self, caster, target_list, damage_text_group):
        alive_enemy = get_alive_targets(target_list)

        if len(alive_enemy) > 0:
            damage_text.cast(caster, " Firestorm! ", damage_text_group)

            input_damage_list = []
            input_type_list = []
            for _ in target_list:
                # Basic Spell Attributes: minimum, maximum, multiplier
                base_damage = randint(0, 20)
                output_damage = (caster.magic * 3) + base_damage

                input_damage, input_type = self.spell_attack_resolution(caster, output_damage, self.hit_resolution())
                input_damage_list.append(input_damage)
                input_type_list.append(input_type)

            # print(input_damage_list, input_type_list)
            self.resolve_aoe_attack(caster, target_list, input_damage_list, input_type_list, damage_text_group)

    def cast_lightning(self, caster, target_list, damage_text_group):
        alive_enemy = get_alive_targets(target_list)

        if len(alive_enemy) > 0:
            damage_text.cast(caster, " Lightning Bolt! ", damage_text_group)

            input_damage_list = []
            input_type_list = []
            for _ in target_list:
                # Basic Spell Attributes: minimum, maximum, multiplier
                base_damage = randint(0, 50)
                output_damage = (caster.magic * 1) + base_damage

                input_damage, input_type = self.spell_attack_resolution(caster, output_damage, self.hit_resolution())
                input_damage_list.append(input_damage)
                input_type_list.append(input_type)

            self.resolve_aoe_attack(caster, target_list, input_damage_list, input_type_list, damage_text_group)
