from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterable

data = open("01.txt").read().strip().split(", ")


# noinspection PyArgumentList
class CardinalDirection(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


# noinspection PyArgumentList
class Face(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Movement:
    face: Face
    steps: int


@dataclass
class CityMap:
    location: list[int, int] = field(init=False, default_factory=lambda: [0, 0])
    cardinal_direction: CardinalDirection = field(init=False, default=CardinalDirection.NORTH)
    location_bread_crumbs: list[tuple[int, int]] = field(init=False, default_factory=list)

    @property
    def distance(self) -> int:
        return abs(self.location[0]) + abs(self.location[1])

    def _turn_towards_direction(self, movement: Movement):
        cardinal_shift = 1 if movement.face == Face.RIGHT else 3
        self.cardinal_direction = CardinalDirection(abs(self.cardinal_direction.value + cardinal_shift) % 4)

    def _step(self, movement: Movement):
        if self.cardinal_direction == CardinalDirection.NORTH:
            for y in range(movement.steps):
                self.location_bread_crumbs.append((self.location[0], self.location[1] + y))
            self.location[1] += movement.steps
        elif self.cardinal_direction == CardinalDirection.SOUTH:
            for y in range(movement.steps):
                self.location_bread_crumbs.append((self.location[0], self.location[1] - y))
            self.location[1] -= movement.steps
        elif self.cardinal_direction == CardinalDirection.WEST:
            for x in range(movement.steps):
                self.location_bread_crumbs.append((self.location[0] - x, self.location[1]))
            self.location[0] -= movement.steps
        elif self.cardinal_direction == CardinalDirection.EAST:
            for x in range(movement.steps):
                self.location_bread_crumbs.append((self.location[0] + x, self.location[1]))
            self.location[0] += movement.steps

    def move(self, movements: list[Movement], stop_at_revisit=False):
        for movement in movements:
            self._turn_towards_direction(movement=movement)
            self._step(movement=movement)
            if stop_at_revisit and len(self.location_bread_crumbs) != len(set(self.location_bread_crumbs)):
                self.location = [list(k) for k, v in Counter(self.location_bread_crumbs).items() if v > 1][0]
                return


def get_movements_from_data(movement_data: list[str]) -> list[Movement]:
    movements = []
    for datum in movement_data:
        face = Face.RIGHT if datum[0] == "R" else Face.LEFT
        steps = int(datum[1:])
        movements.append(Movement(face=face, steps=steps))
    return movements


movements_from_data = get_movements_from_data(movement_data=data)

city_map = CityMap()
city_map.move(movements=movements_from_data)
print(f"PART ONE: {city_map.distance}")

city_map = CityMap()
city_map.move(movements=movements_from_data, stop_at_revisit=True)
print(f"PART TWO: {city_map.distance}")
