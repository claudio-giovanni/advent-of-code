import math
from itertools import combinations

data = open("02.txt").read().splitlines()


class Gift:
    def __init__(self, box_line: str):
        self.box: list[int] = sorted(map(int, box_line.split("x")))

    def get_wrapping_paper_length(self) -> int:
        smallest_side_surface_are = self.box[0] * self.box[1]
        total_surface_area = 2 * sum(map(math.prod, combinations(self.box, 2)))
        return smallest_side_surface_are + total_surface_area

    def get_ribbon_length(self) -> int:
        box_ribbon = 2 * sum(self.box[:-1])
        bow_ribbon = math.prod(self.box)
        return bow_ribbon + box_ribbon


total_wrapping_paper_needed = sum(Gift(datum).get_wrapping_paper_length() for datum in data)
print(f"PART ONE: {total_wrapping_paper_needed}")

total_ribbon_needed = sum(Gift(datum).get_ribbon_length() for datum in data)
print(f"PART TWO: {total_ribbon_needed}")
