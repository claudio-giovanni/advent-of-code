import matplotlib.pyplot as plt

data_points, data_fold_line = open("13.txt").read().split("\n\n")
data_points: list[tuple[int, ...]] = [tuple(map(int, point.split(","))) for point in data_points.split("\n")]
data_fold_line = data_fold_line.split("\n")
data_folds: list[tuple[str, int]] = []
for line in data_fold_line:
    data_axis, data_value = line.split("=")
    data_folds.append((data_axis[-1], int(data_value)))


class Grid:
    def __init__(self, points: list[tuple[int, ...]]):
        self.points = points

    @property
    def point_count(self) -> int:
        return len(set(self.points))

    def fold(self, folds: list[tuple[str, int]]):
        for fold in folds:
            axis, value = fold
            if axis == "y":
                self._fold_horizontally(fold_value=value)
            elif axis == "x":
                self._fold_vertically(fold_value=value)

    def _fold_horizontally(self, fold_value: int):
        folded_points = [(x, y) for x, y in self.points if y > fold_value]
        self.points = [point for point in self.points if point[1] < fold_value]
        self.points.extend([(x, fold_value - (y - fold_value)) for x, y in folded_points])

    def _fold_vertically(self, fold_value: int):
        folded_points = [(x, y) for x, y in self.points if x > fold_value]
        self.points = [point for point in self.points if point[0] < fold_value]
        self.points.extend([(fold_value - (x - fold_value), y) for x, y in folded_points])

    def __repr__(self):
        return f"Grid(points={self.points})"

    def __str__(self):
        plt.scatter(x=[p[0] for p in self.points], y=[p[1] for p in self.points], marker="8")
        plt.gca().set_ylim(15, -10)
        plt.show()
        return "**SEE IMAGE**"


grid = Grid(points=data_points)
grid.fold(folds=[data_folds[0]])
print("PART ONE: ", grid.point_count)

grid.fold(folds=data_folds[1:])
print("PART TWO: ", grid)
