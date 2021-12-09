import math
from typing import Optional

data_grid = [list(map(int, row)) for row in open("09.txt").read().splitlines()]


class Grid:
    def __init__(self, grid_points: list[list[int]]):
        self.grid_points = grid_points
        self.width = len(self.grid_points[0])
        self.height = len(self.grid_points)
        self.basin_size_map: dict[tuple[int, int], int] = {}
        self.basin_points = self.get_low_points()

    def get_low_points(self) -> list[Optional[int]]:
        low_points = []
        for v_index, row in enumerate(self.grid_points):
            for h_index, number in enumerate(row):
                is_horizontal_divot = self._is_horizontal_divot(number=number, row=row, index=h_index)
                is_vertical_divot = self._is_vertical_divot(number=number, h_index=h_index, v_index=v_index)
                if is_horizontal_divot and is_vertical_divot:
                    low_points.append(number)
                    low_point_basin_points = []
                    self._get_basin_points(h_index=h_index, v_index=v_index, basin_points=low_point_basin_points)
                    self.basin_size_map[(v_index, h_index)] = len(low_point_basin_points)
        return low_points

    def _get_basin_points(self, h_index: int, v_index: int, basin_points: list[tuple[int, int]]):
        basin_points.append((v_index, h_index))
        # check point to the left
        if h_index != 0:
            new_v_index, new_h_index = v_index, h_index - 1
            if self.grid_points[new_v_index][new_h_index] != 9 and (new_v_index, new_h_index) not in basin_points:
                self._get_basin_points(v_index=new_v_index, h_index=new_h_index, basin_points=basin_points)
        # check point to the right
        if h_index != (self.width - 1):
            new_v_index, new_h_index = v_index, h_index + 1
            if self.grid_points[new_v_index][new_h_index] != 9 and (new_v_index, new_h_index) not in basin_points:
                self._get_basin_points(v_index=new_v_index, h_index=new_h_index, basin_points=basin_points)
        # check point below
        if v_index != 0:
            new_v_index, new_h_index = v_index - 1, h_index
            if self.grid_points[new_v_index][new_h_index] != 9 and (new_v_index, new_h_index) not in basin_points:
                self._get_basin_points(v_index=new_v_index, h_index=new_h_index, basin_points=basin_points)
        # check point above
        if v_index != (self.height - 1):
            new_v_index, new_h_index = v_index + 1, h_index
            if self.grid_points[new_v_index][new_h_index] != 9 and (new_v_index, new_h_index) not in basin_points:
                self._get_basin_points(v_index=new_v_index, h_index=new_h_index, basin_points=basin_points)

    def _is_horizontal_divot(self, number: int, row: list[int], index: int) -> bool:
        if index == 0:
            return row[index + 1] > number
        elif index == (self.width - 1):
            return row[index - 1] > number
        else:
            return row[index + 1] > number < row[index - 1]

    def _is_vertical_divot(self, number: int, h_index: int, v_index: int) -> bool:
        if v_index == 0:
            return self.grid_points[v_index + 1][h_index] > number
        elif v_index == self.height - 1:
            return self.grid_points[v_index - 1][h_index] > number
        else:
            return self.grid_points[v_index + 1][h_index] > number < self.grid_points[v_index - 1][h_index]


grid = Grid(grid_points=data_grid)
risk_level = sum(grid.basin_points) + len(grid.basin_points)
print("PART ONE: ", risk_level)

basin_sizes = sorted(list(grid.basin_size_map.values()), reverse=True)
largest_basins_multiple = math.prod(basin_sizes[:3])
print("PART TWO: ", largest_basins_multiple)
