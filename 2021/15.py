import itertools
from collections import namedtuple

data = open("15.txt").read().split()
data_numbers: list[list[int]] = [list(map(int, number)) for number in data]

SURROUNDING_POINTS = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
SURROUNDING_POINTS.remove((0, 0))
Point = namedtuple("Point", "x y")


class Grid:
    def __init__(self, number_rows: list[list[int]]):
        self.number_rows = number_rows

    def navigate_to_end(self):
        viable_path: list[list] = []
        frozen_points = None
        for v_index, row in enumerate(self.number_rows):
            for h_index, number in enumerate(row):
                for h, v in SURROUNDING_POINTS:
                    self._get_available_moves(h_index=h_index + h, v_index=v_index + v, frozen_points=frozen_points)

    def _get_available_moves(self, h_index, v_index):
        frozen_points = None
        if h_index < 0 or v_index < 0:
            return
        try:
            self._increment_point(
                h_index=h_index, v_index=v_index, value=self.grid_points[v_index][h_index], frozen_points=frozen_points
            )
        except IndexError:
            return

    def __repr__(self):
        return f"Grid({self.number_rows})"


grid = Grid(data_numbers)
print(grid)
