from typing import Optional


class Line:
    def __init__(self, start: tuple[int], end: tuple[int]):
        self.x1, self.y1 = start[0], start[1]
        self.x2, self.y2 = end[0], end[1]
        self.min_x, self.max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        self.min_y, self.max_y = min(self.y1, self.y2), max(self.y1, self.y2)

    def get_horizontal_vertical_points(self) -> Optional[list[tuple[int, int]]]:
        """calculate all coordinates in a horizontal or vertical line"""
        if self.x1 == self.x2:
            return [(self.x1, y) for y in range(self.min_y, self.max_y + 1)]
        elif self.y1 == self.y2:
            return [(x, self.y1) for x in range(self.min_x, self.max_x + 1)]

    def get_diagonal_points(self) -> Optional[list[tuple[int, int]]]:
        """calculate all coordinates in a diagonal 45° line"""
        if self.x2 == self.x1:
            return None
        if (self.y2 - self.y1) / (self.x2 - self.x1) == 1:
            return [(x, y) for x, y in zip(range(self.min_x, self.max_x + 1), range(self.min_y, self.max_y + 1))]
        if (self.y2 - self.y1) / (self.x2 - self.x1) == -1:
            return [(x, y) for x, y in zip(range(self.min_x, self.max_x + 1), range(self.min_y, self.max_y + 1)[::-1])]

    def __repr__(self):
        return f"Line({self.x1, self.y1} -> {self.x2, self.y2})"


class Grid:
    def __init__(self, lines: list[Line]):
        self.lines = lines

    def count_overlapping_horizontal_and_vertical_points(self) -> int:
        point_counter: dict[tuple, int] = {}
        for line in self.lines:
            if bool(points := line.get_horizontal_vertical_points()):
                for x, y in points:
                    point_counter[(x, y)] = point_counter.get((x, y), 0) + 1
        return sum(point > 1 for point in point_counter.values())

    def count_overlapping_horizontal_vertical_and_diagonals_points(self) -> int:
        point_counter: dict[tuple, int] = {}
        for line in self.lines:
            points = line.get_horizontal_vertical_points() or [] + line.get_diagonal_points() or []
            if points:
                for x, y in points:
                    point_counter[(x, y)] = point_counter.get((x, y), 0) + 1
        return sum(point > 1 for point in point_counter.values())

    def __repr__(self):
        return f"Grid([{self.lines}])"


data = open("05.txt").read().splitlines()
data = [line.split(" -> ") for line in data]
data_lines = [[tuple(int(n) for n in line[0].split(",")), tuple(int(n) for n in line[1].split(","))] for line in data]

lines = [Line(start=line[0], end=line[1]) for line in data_lines]
grid = Grid(lines=lines)
horizontal_vertical_sum = grid.count_overlapping_horizontal_and_vertical_points()
horizontal_vertical_and_diagonal_sum = grid.count_overlapping_horizontal_vertical_and_diagonals_points()

print("PART ONE: ", horizontal_vertical_sum)
print("PART TWO: ", horizontal_vertical_and_diagonal_sum)
