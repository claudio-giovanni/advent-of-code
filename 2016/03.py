from __future__ import annotations

from itertools import chain

data = open("03.txt").read().splitlines()


class Triangle:
    def __init__(self, sides: tuple[int, ...]):
        self.sides = sides

    @property
    def is_valid(self):
        return (max_side := max(self.sides)) < sum(self.sides) - max_side


def get_triangles_from_data_horizontally(triangle_data: list[str]) -> list[Triangle]:
    valid_triangles = []
    for datum in triangle_data:
        sides = tuple(int(number) for number in datum.strip().split())
        if (triangle := Triangle(sides=sides)).is_valid:
            valid_triangles.append(triangle)
    return valid_triangles


def get_triangles_from_data_vertically(triangle_data: list[str]) -> list[Triangle]:
    valid_triangles = []
    columns = list(zip(*[tuple(int(number) for number in datum.strip().split()) for datum in triangle_data]))
    side_chain = list(chain(*columns))
    for i in range(0, len(side_chain), 3):
        if (triangle := Triangle(sides=tuple(side_chain[i : i + 3]))).is_valid:
            valid_triangles.append(triangle)
    return valid_triangles


horizontal_triangles = get_triangles_from_data_horizontally(triangle_data=data)
print(f"PART ONE: {len(horizontal_triangles)}")

vertical_triangles = get_triangles_from_data_vertically(triangle_data=data)
print(f"PART TWO: {len(vertical_triangles)}")
