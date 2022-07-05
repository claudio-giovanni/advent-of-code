from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import Enum, auto

data = open("01.txt").read().strip().split(", ")


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

    @classmethod
    def get_movements_from_data(cls, movement_data: list[str]) -> list[Movement]:
        movements = []
        for datum in movement_data:
            face = Face.RIGHT if datum[0] == "R" else Face.LEFT
            steps = int(datum[1:])
            movements.append(cls(face=face, steps=steps))
        return movements


@dataclass
class CityMap:
    location: list[int, int] = field(init=False, default_factory=lambda: [0, 0])
    cardinal_direction: CardinalDirection = field(init=False, default=CardinalDirection.NORTH)
    location_bread_crumbs: list[tuple[int, int]] = field(init=False, default_factory=list)

    @property
    def displacement(self) -> int:
        return abs(self.location[0]) + abs(self.location[1])

    def _turn_towards_direction(self, face: Face):
        cardinal_shift = 1 if face == Face.RIGHT else 3
        self.cardinal_direction = CardinalDirection(abs(self.cardinal_direction.value + cardinal_shift) % 4)

    def _step(self, steps: int):
        if self.cardinal_direction == CardinalDirection.NORTH:
            for y in range(steps):
                self.location_bread_crumbs.append((self.location[0], self.location[1] + y))
            self.location[1] += steps
        elif self.cardinal_direction == CardinalDirection.SOUTH:
            for y in range(steps):
                self.location_bread_crumbs.append((self.location[0], self.location[1] - y))
            self.location[1] -= steps
        elif self.cardinal_direction == CardinalDirection.WEST:
            for x in range(steps):
                self.location_bread_crumbs.append((self.location[0] - x, self.location[1]))
            self.location[0] -= steps
        elif self.cardinal_direction == CardinalDirection.EAST:
            for x in range(steps):
                self.location_bread_crumbs.append((self.location[0] + x, self.location[1]))
            self.location[0] += steps

    def move(self, movements: list[Movement], stop_at_revisit=False):
        for movement in movements:
            self._turn_towards_direction(face=movement.face)
            self._step(steps=movement.steps)
            if stop_at_revisit and len(self.location_bread_crumbs) != len(set(self.location_bread_crumbs)):
                self.location = [list(k) for k, v in Counter(self.location_bread_crumbs).items() if v > 1][0]
                return


movements_from_data = Movement.get_movements_from_data(movement_data=data)

city_map = CityMap()
city_map.move(movements=movements_from_data)
print(f"PART ONE: {city_map.displacement}")

city_map = CityMap()
city_map.move(movements=movements_from_data, stop_at_revisit=True)
print(f"PART TWO: {city_map.displacement}")
