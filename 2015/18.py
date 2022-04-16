import itertools
from copy import deepcopy

data = open("18.txt").read().splitlines()
COORDINATE_DISPLACEMENT = list(itertools.product([-1, 0, 1], repeat=2))
COORDINATE_DISPLACEMENT.remove((0, 0))
CORNER_COORDINATES = list(itertools.product([-1, 0], repeat=2))


class LightGrid:
    def __init__(self, grid_data: [str], corners_always_on: bool = False):
        grid_data = [list(row) for row in grid_data]
        self.grid = [[1 if value == "#" else 0 for value in row] for row in grid_data]
        self.corners_always_on = corners_always_on
        x_len, y_len = len(self.grid[0]) - 1, len(self.grid) - 1
        self.corner_coordinates = [(abs(x * x_len), abs(y * y_len)) for x, y in CORNER_COORDINATES]
        if corners_always_on:
            for x, y in self.corner_coordinates:
                self.grid[y][x] = 1

    @property
    def on_lights(self) -> int:
        return sum(sum(row) for row in self.grid)

    def animate(self):
        grid = deepcopy(self.grid)
        for y, row in enumerate(self.grid):
            for x, light in enumerate(row):
                if self.corners_always_on and (x, y) in self.corner_coordinates:
                    continue
                on_neighbors = self.get_on_neighbors(x=x, y=y, grid=grid)
                if light and on_neighbors not in [2, 3]:
                    self.grid[y][x] = 0
                elif not light and on_neighbors == 3:
                    self.grid[y][x] = 1

    def __repr__(self):
        return "\n".join(str(row) for row in self.grid)

    @staticmethod
    def get_on_neighbors(x: int, y: int, grid: [[int]]) -> int:
        on_neighbors = 0
        for dx, dy in COORDINATE_DISPLACEMENT:
            dx, dy = x + dx, y + dy
            if dx < 0 or dy < 0:
                continue
            try:
                on_neighbors += grid[dy][dx]
            except IndexError:
                pass
        return on_neighbors


light_grid = LightGrid(grid_data=data, corners_always_on=False)
for _ in range(100):
    light_grid.animate()
print(f"PART ONE: {light_grid.on_lights}")
light_grid = LightGrid(grid_data=data, corners_always_on=True)
for _ in range(100):
    light_grid.animate()
print(f"PART TWO: {light_grid.on_lights}")
