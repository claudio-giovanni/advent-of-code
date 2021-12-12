import itertools

data_grid = [list(map(int, row)) for row in open("11.txt").read().splitlines()]

SURROUNDING_POINTS = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
SURROUNDING_POINTS.remove((0, 0))


class Grid:
    def __init__(self, grid_points: list[list[int]]):
        self.grid_points = grid_points
        width = len(self.grid_points[0])
        height = len(self.grid_points)
        self.area = width * height
        self.zero_current = 0
        self.zero_counter = 0

    def increment_grid(self):
        frozen_points: list[tuple[int, int]] = []
        for v_index, row in enumerate(self.grid_points):
            for h_index, number in enumerate(row):
                self._increment_point(h_index=h_index, v_index=v_index, value=number, frozen_points=frozen_points)
        self.zero_current = sum(point.count(0) for point in self.grid_points)

    def _increment_point(self, h_index: int, v_index: int, value: int, frozen_points: list[tuple[int, int]]):
        coordinate = (h_index, v_index)
        if coordinate in frozen_points:
            return
        elif value < 9:
            self.grid_points[v_index][h_index] += 1
        else:
            self.grid_points[v_index][h_index] = 0
            self.zero_counter += 1
            frozen_points.append(coordinate)
            for h, v in SURROUNDING_POINTS:
                self._try_increment(h_index=h_index + h, v_index=v_index + v, frozen_points=frozen_points)

    def _try_increment(self, h_index: int, v_index: int, frozen_points: list[tuple[int, int]]):
        if h_index < 0 or v_index < 0:
            return
        try:
            self._increment_point(
                h_index=h_index, v_index=v_index, value=self.grid_points[v_index][h_index], frozen_points=frozen_points
            )
        except IndexError:
            return

    def __repr__(self):
        return "\n".join(str(row) for row in self.grid_points)


grid = Grid(grid_points=data_grid)
for i in itertools.count(start=1):
    grid.increment_grid()
    if i == 100:
        print("PART ONE: ", grid.zero_counter)
    if grid.zero_current == grid.area:
        print("PART TWO: ", i)
        break
