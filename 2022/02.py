from __future__ import annotations

from enum import Enum
from itertools import cycle

data = [datum.split() for datum in open("02.txt").read().splitlines()]


class Result(int, Enum):
    LOSS: int = 0
    DRAW: int = 3
    WIN: int = 6

    def determine_weapon(self, other: Weapon) -> Weapon:
        for weapon in Weapon:
            if weapon.duel(other=other) == self:
                return weapon


class Weapon(int, Enum):
    ROCK: int = 1
    PAPER: int = 2
    SCISSOR: int = 3

    def duel(self, other: Weapon) -> Result:
        if self == other:
            return Result.DRAW
        return Result.WIN if VICTORY_RULES[self] == other else Result.LOSS


def score_duel(my_weapon: Weapon, enemy_weapon: Weapon) -> int:
    return my_weapon.duel(other=enemy_weapon) + my_weapon.value


PLAYER_CYPHER: dict[str, Weapon] = dict(zip("ABCXYZ", cycle(Weapon)))
VICTORY_RULES = {Weapon.ROCK: Weapon.SCISSOR, Weapon.PAPER: Weapon.ROCK, Weapon.SCISSOR: Weapon.PAPER}

total_scores = sum(score_duel(PLAYER_CYPHER[player], PLAYER_CYPHER[enemy]) for enemy, player in data)
print(f"PART ONE: {total_scores}")

RESULT_CYPHER: dict[str, Result] = dict(zip("XYZ", Result))
total_scores = 0
for enemy, result in data:
    enemy = PLAYER_CYPHER[enemy]
    player_weapon = RESULT_CYPHER[result].determine_weapon(other=enemy)
    total_scores += score_duel(player_weapon, enemy)
print(f"PART TWO: {total_scores}")
