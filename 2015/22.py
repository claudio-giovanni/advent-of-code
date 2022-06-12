from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from math import inf
from typing import Callable, Iterable

data = open("22.txt").read().splitlines()


class SpellFailedException(Exception):
    pass


class CharacterDiedException(Exception):
    pass


@dataclass
class Spell:
    name: str
    mana_cost: int
    cast: Callable[[Character, Character], None] = field(repr=False)
    duration: int = field(repr=False)

    def __bool__(self):
        return self.duration > 0

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: Spell):
        return hash(self) == hash(other)


class Effect:
    @staticmethod
    def curse(self: Character, _: Character):
        self.hit_points -= 1

    @staticmethod
    def magic_missile(_: Character, other: Character):
        other.hit_points -= 4

    @staticmethod
    def drain(self: Character, other: Character):
        other.hit_points -= 2
        self.hit_points += 2

    @staticmethod
    def shield(self: Character, _: Character):
        self.armor = 7

    @staticmethod
    def poison(_: Character, other: Character):
        other.hit_points -= 3

    @staticmethod
    def recharge(self: Character, _: Character):
        self.mana += 101


curse = Spell(name="curse", mana_cost=0, cast=Effect.curse, duration=0)
magic_missile = Spell(name="magic_missile", mana_cost=53, cast=Effect.magic_missile, duration=0)
drain = Spell(name="drain", mana_cost=73, cast=Effect.drain, duration=0)
shield = Spell(name="shield", mana_cost=113, cast=Effect.shield, duration=6)
poison = Spell(name="poison", mana_cost=173, cast=Effect.poison, duration=6)
recharge = Spell(name="recharge", mana_cost=229, cast=Effect.recharge, duration=5)


@dataclass
class Character:
    hit_points: int
    damage: int
    armor: int
    mana: int
    eot: list[Spell] = field(init=False, repr=False, default_factory=list)

    @property
    def is_dead(self):
        return self.hit_points <= 0

    def attack_with_weapon(self, other: Character):
        other.hit_points -= max(self.damage - other.armor, 1)
        if other.is_dead:
            raise CharacterDiedException

    def cast_spell(self, other: Character, spell: Spell):
        if spell.mana_cost > self.mana:
            raise SpellFailedException("INSUFFICIENT MANA")
        if spell in self.eot:
            raise SpellFailedException("SPELL ALREADY IN EOT")
        self.mana -= spell.mana_cost
        self.eot.append(deepcopy(spell)) if spell.duration else spell.cast(self, other)
        if self.is_dead or other.is_dead:
            raise CharacterDiedException

    def resolve_eot(self, other: Character):
        for spell in self.eot:
            spell.cast(self, other)
            spell.duration -= 1
            if spell == shield and spell.duration == 0:
                self.armor = 0
        if self.is_dead or other.is_dead:
            raise CharacterDiedException

        self.eot = list(filter(None, self.eot))

    @staticmethod
    def from_file(character_data: list[str]) -> Character:
        hit_points, damage = map(int, (value.split(" ")[-1] for value in character_data))
        return Character(hit_points=hit_points, damage=damage, armor=0, mana=0)


def get_spell_permutations() -> Iterable[tuple[Spell], int]:
    spell_mutations: tuple[tuple[Spell], ...] = ((magic_missile,), (drain,), (shield,), (poison,), (recharge,))
    spells_cast = ((),)
    while True:
        valid_permutation = set()
        for spells in spells_cast:
            for new_spell in spell_mutations:
                spell_permutation = spells + new_spell
                permutation_cost = sum(spell.mana_cost for spell in spell_permutation)
                yield spell_permutation, permutation_cost
                valid_permutation.add(spell_permutation)
        spells_cast = tuple(valid_permutation)


def efficiency_battle_magic_beats_melee(wizard: Character, warrior: Character, limit: int | float, hard: bool) -> int:
    for spells, spells_cost in get_spell_permutations():
        temp_wizard, temp_warrior = deepcopy(wizard), deepcopy(warrior)
        for spell in spells:
            try:
                if hard:
                    temp_wizard.cast_spell(other=temp_warrior, spell=curse)
                temp_wizard.resolve_eot(other=temp_warrior)
                temp_wizard.cast_spell(other=temp_warrior, spell=spell)
                if hard:
                    temp_wizard.cast_spell(other=temp_warrior, spell=curse)
                temp_wizard.resolve_eot(other=temp_warrior)
                temp_warrior.attack_with_weapon(temp_wizard)
            except SpellFailedException:
                break
            except CharacterDiedException:
                if temp_warrior.is_dead and spells_cost < limit:
                    return spells_cost
                break


adventurer = Character(hit_points=50, damage=0, armor=0, mana=500)
boss = Character.from_file(data)

print(f"PART ONE: {efficiency_battle_magic_beats_melee(wizard=adventurer, warrior=boss, limit=1280, hard=False)}")
print(f"PART TWO: {efficiency_battle_magic_beats_melee(wizard=adventurer, warrior=boss, limit=inf, hard=True)}")
