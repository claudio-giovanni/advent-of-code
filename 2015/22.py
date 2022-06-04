from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from itertools import count, product

data = open("22.txt").read().splitlines()


@dataclass
class Spell:
    name: str
    mana_cost: int
    damage: int
    armor: int
    hp_regen: int
    mana_regen: int
    target_self: bool
    duration: int

    def __eq__(self, other: Spell):
        return self.name == other.name


magic_missile = Spell(
    name="magic_missile", mana_cost=49, damage=4, armor=0, hp_regen=0, mana_regen=0, target_self=False, duration=0
)
drain = Spell(name="drain", mana_cost=73, damage=2, armor=0, hp_regen=2, mana_regen=0, target_self=False, duration=0)
shield = Spell(name="shield", mana_cost=113, damage=0, armor=7, hp_regen=0, mana_regen=0, target_self=True, duration=6)
poison = Spell(name="poison", mana_cost=173, damage=3, armor=0, hp_regen=0, mana_regen=0, target_self=False, duration=6)
recharge = Spell(
    name="recharge", mana_cost=229, damage=0, armor=0, hp_regen=0, mana_regen=101, target_self=True, duration=5
)


@dataclass
class Character:
    hit_points: int
    damage: int
    armor: int
    mana: int
    dot: list[Spell] = field(init=False, repr=False, default_factory=dict)

    def __bool__(self):
        return self.hit_points > 0

    def attack_with_weapon(self, other: Character):
        other.hit_points = other.hit_points - max(self.damage - other.armor, 1)

    def attack_with_spell(self, other: Character, spell: Spell):
        if spell.name == drain.name:
            self._resolve_spell(spell=spell)
        if spell.target_self:
            if spell.duration:
                self.dot.append(deepcopy(spell))
            else:
                self._resolve_spell(spell=spell)
        if spell.target_self is False:
            if spell.duration:
                other.dot.append(deepcopy(spell))
            else:
                other._resolve_spell(spell=spell)

    def _resolve_spell(self, spell: Spell):
        self.mana -= spell.mana_cost
        self.hit_points -= spell.damage
        self.armor += spell.armor
        self.hit_points += spell.hp_regen
        self.mana += spell.mana_regen

    @staticmethod
    def from_file(character_data: list[str]) -> Character:
        hit_points, damage = map(int, (value.split(" ")[-1] for value in character_data))
        return Character(hit_points=hit_points, damage=damage, armor=0, mana=0)


spell_chain: list[list[Spell]] = [[magic_missile], [drain], [shield], [poison], [recharge]]


def get_spell_permutations_by_mana(mana: int, spells_cast: list[list[Spell]] = None):
    spells_cast = spells_cast or []
    permutations = (cast + flat for cast, flat in product(spells_cast, spell_chain)) if spells_cast else spell_chain
    for spells in permutations:
        spells_mana_cost = sum(spell.mana_cost for spell in spells)
        if spells_mana_cost < mana:
            spells_cast.append(spells)
            get_spell_permutations_by_mana(mana=mana, spells_cast=spells_cast)
    return permutations


print(get_spell_permutations_by_mana(100))


def efficiency_battle_magic_beats_melee(wizard: Character, warrior: Character) -> int:
    # successful_mana_spent = []
    # while True:
    #     for mana in count(1, 1):
    #         for spell in spell_chain:
    #             wizard.attack_with_spell(other=warrior, spell=spell)
    #             if not warrior:
    #                 successful_mana_spent =

    pass


adventurer = Character(hit_points=50, damage=0, armor=0, mana=500)
boss = Character.from_file(data)

# print(adventurer)
# print(boss)
efficiency_battle_magic_beats_melee(wizard=adventurer, warrior=boss)
# print(f"PART ONE: {None}")
# print(f"PART TWO: {None}")
