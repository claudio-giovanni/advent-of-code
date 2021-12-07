from __future__ import annotations

from collections import Counter
from typing import Optional


class LanternFish:
    _LIFE_SPAN_NEW = 8
    _LIFE_SPAN_REBORN = 6

    def __init__(self, life_span: int):
        self.life_span = life_span

    def grow(self, days=1) -> Optional[LanternFish]:
        if self.life_span == 0:
            self.life_span = LanternFish._LIFE_SPAN_REBORN
            return LanternFish(life_span=LanternFish._LIFE_SPAN_NEW)
        self.life_span -= days

    def __repr__(self):
        return f"LanternFish({self.life_span})"


class School:
    def __init__(self, fishes: list[LanternFish]):
        self.fishes = fishes

    def increment_days(self, days: int):
        for _ in range(days):
            new_fishes = [new_fish for fish in self.fishes if bool(new_fish := fish.grow())]
            self.fishes += new_fishes

    def __repr__(self):
        return f"School({self.fishes})"


data = [int(number) for number in open("06.txt").read().split(",")]
lantern_fishes = [LanternFish(life_span=age) for age in data]
fish_school = School(fishes=lantern_fishes)
fish_school.increment_days(days=80)
print("PART ONE: ", len(fish_school.fishes))


# memory efficient approach to solving DAY 6


def calculate_school_size(ages: list[int], days: int, life_span_new: int = 8, life_span_renew: int = 6) -> int:
    fish_life_map = Counter(ages)
    for _ in range(days):
        reborn_fish = fish_life_map.get(0, 0)
        for i in range(life_span_new):
            fish_life_map[i] = fish_life_map.get(i + 1, 0)
        fish_life_map[life_span_new] = reborn_fish
        fish_life_map[life_span_renew] = fish_life_map.get(life_span_renew, 0) + reborn_fish
    return sum(fish_life_map.values())


fish_ages = [age for age in data]
print("PART TWO: ", calculate_school_size(ages=fish_ages, days=256))
