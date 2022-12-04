import re
from dataclasses import dataclass
from typing import Iterable

data = open("01.txt").read()
data = [map(int, i.split()) for i in re.findall(r"((?:\d+\n)+)", data)]


@dataclass
class Elf:
    inventory: Iterable[int]

    @property
    def calories(self) -> int:
        return sum(self.inventory)


elves = [Elf(datum) for datum in data]

sorted_elves = list(sorted((elf.calories for elf in elves), reverse=True))

print(f"PART ONE: {sorted_elves[0]}")
print(f"PART TWO: {sum(sorted_elves[:3])}")
