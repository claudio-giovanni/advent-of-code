import math
from dataclasses import dataclass
from typing import Iterable

data = open("03.txt").read().splitlines()


@dataclass
class Location:
    x: int
    y: int


@dataclass
class TobogganMap:
    location: Location
    terrain: list[list[bool]]

    def __post_init__(self):
        self._terrain_height = len(self.terrain)
        self._terrain_width = len(self.terrain[0])

    @property
    def at_tree(self) -> bool:
        return self.terrain[self.location.y][self.location.x]

    def sled(self, right: int, down: int) -> Iterable:
        while self.location.y < self._terrain_height:
            yield
            self.location.x = (self.location.x + right) % self._terrain_width
            self.location.y = self.location.y + down


def get_toboggan_map_from_data(map_data: list[str]) -> TobogganMap:
    terrain_lines = [list(map(lambda c: c == "#", map_datum)) for map_datum in map_data]
    return TobogganMap(location=Location(0, 0), terrain=terrain_lines)


toboggan_map = get_toboggan_map_from_data(map_data=data)
trees_hit = [toboggan_map.at_tree for _ in toboggan_map.sled(right=3, down=1)]
print(f"PART ONE: {sum(trees_hit)}")

slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
trees_hit_sum = []
for slope_right, slope_down in slopes:
    toboggan_map.location = Location(0, 0)
    trees_hit_sum.append(sum(toboggan_map.at_tree for _ in toboggan_map.sled(right=slope_right, down=slope_down)))
print(f"PART TWO: {math.prod(trees_hit_sum)}")
