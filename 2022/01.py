from dataclasses import dataclass

data = open("01.txt").read().splitlines()
data = [[int(i) for i in datum.split("\n") if i] for datum in data]


@dataclass
class Elf:
    inventory: list[int]


elves = [Elf(datum) for datum in data]

sorted_elves = list(sorted((sum(elf.inventory) for elf in elves), reverse=True))

print(f"PART ONE: {sorted_elves[0]}")
print(f"PART TWO: {sum(sorted_elves[:3])}")
