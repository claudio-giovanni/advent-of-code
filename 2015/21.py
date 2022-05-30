from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations, product
from typing import Iterable, Optional, Union

data = open("21.txt").read().splitlines()
data2 = list(filter(bool, open("21_2.txt").read().splitlines()))


class ItemType(Enum):
    WEAPON = "Weapons"
    ARMOR = "Armor"
    RING = "Rings"


@dataclass
class Item:
    name: str
    damage: int
    armor: int
    cost: int = field(repr=False)


@dataclass
class Character:
    hit_points: int
    damage: int
    armor: int
    gold: int = 0

    def __bool__(self):
        return self.hit_points > 0

    def can_beat(self, other: Character) -> bool:
        self_hit_point, other_hit_points = self.hit_points, other.hit_points
        while True:
            self.attack(other)
            if not other:
                break
            other.attack(self)
            if not self:
                break
        has_won = bool(self)
        self.hit_points, other.hit_points = self_hit_point, other_hit_points
        return has_won

    def attack(self, other: Character):
        other.hit_points = other.hit_points - max(self.damage - other.armor, 1)

    def equip_item(self, item: Union[Item, list[Item]]):
        if isinstance(item, Iterable):
            for individual_item in item:
                return self.equip_item(item=individual_item)
        self.damage += item.damage
        self.armor += item.armor
        self.gold -= item.cost

    def unequip_item(self, item: Union[Item, Iterable[Item]]):
        if isinstance(item, Iterable):
            for individual_item in item:
                return self.unequip_item(item=individual_item)
        self.damage -= item.damage
        self.armor -= item.armor
        self.gold += item.cost


@dataclass
class Shop:
    weapons: list[Item]
    armor: list[Item]
    rings: list[Item]

    @property
    def armor_combinations(self) -> list[Optional[Item]]:
        valid_combinations = [None]
        for armor in self.armor:
            valid_combinations.append(armor)
        return valid_combinations

    @property
    def ring_combinations(self) -> list[tuple[Optional[Item]]]:
        valid_combinations = [tuple()]
        for ring in self.rings:
            valid_combinations.append((ring,))
        for ring in combinations(self.rings, 2):
            valid_combinations.append(ring)
        return valid_combinations

    def try_on_gear(self, character: Character):
        for items in product(self.weapons, self.armor_combinations, self.ring_combinations):
            for item in filter(bool, items):
                character.equip_item(item=item)
            yield
            for item in filter(bool, items):
                character.unequip_item(item=item)


class DataParser:
    @staticmethod
    def parse_character(character_data: list[str]) -> Character:
        hit_points, damage, armor = map(int, (value.split(" ")[-1] for value in character_data))
        return Character(hit_points=hit_points, damage=damage, armor=armor)

    @staticmethod
    def parse_shop_items(item_data: list[str]) -> Shop:
        items = {item_type.value: [] for item_type in ItemType}
        current_item_type = None
        for datum in item_data:
            if declared_item_type := [item_type for item_type in ItemType if datum.startswith(item_type.value)]:
                current_item_type = declared_item_type[0].value
                continue
            else:
                name = re.findall(r".*?(?=\s\d)", datum)[0].strip()
                cost, damage, armor = map(int, re.findall(r"\d+", datum)[-3:])
                item = Item(name=name, cost=cost, damage=damage, armor=armor)
                items[current_item_type].append(item)
        return Shop(
            weapons=items[ItemType.WEAPON.value], armor=items[ItemType.ARMOR.value], rings=items[ItemType.RING.value]
        )


adventurer = Character(hit_points=100, damage=0, armor=0)
boss = DataParser.parse_character(character_data=data)
shop = DataParser.parse_shop_items(item_data=data2)

successful_build_costs = []
for _ in shop.try_on_gear(character=adventurer):
    if adventurer.can_beat(boss):
        successful_build_costs.append(abs(adventurer.gold))

print(f"PART ONE: {min(successful_build_costs)}")
print(f"PART TWO: {None}")
