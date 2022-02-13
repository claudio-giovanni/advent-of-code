import re
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int


data = open("06.txt").readlines()


def grid_generator(start: Coordinate, end: Coordinate):
    for x in range(start.x, end.x + 1):
        for y in range(start.y, end.y + 1):
            yield x, y


class LightGrid:
    def __init__(self):
        self.lights = [[0] * 1000 for _ in range(1000)]

    @property
    def on_lights(self) -> int:
        return sum(light for row in self.lights for light in row)

    def switch(self, start: Coordinate, end: Coordinate, is_on: bool):
        for x, y in grid_generator(start=start, end=end):
            self.lights[x][y] = is_on

    def toggle(self, start: Coordinate, end: Coordinate):
        for x, y in grid_generator(start=start, end=end):
            self.lights[x][y] = not (self.lights[x][y])


class ElvishLightGrid(LightGrid):
    def switch(self, start: Coordinate, end: Coordinate, is_on: bool):
        for x, y in grid_generator(start=start, end=end):
            if is_on:
                self.lights[x][y] += 1
            elif self.lights[x][y]:
                self.lights[x][y] -= 1

    def toggle(self, start: Coordinate, end: Coordinate):
        for x, y in grid_generator(start=start, end=end):
            self.lights[x][y] += 2


grid = LightGrid()
elvish_grid = ElvishLightGrid()
for instruction in data:
    coordinates = re.findall(r"\d+,\d+", instruction)
    start_coordinate = Coordinate(*list(map(int, coordinates[0].split(","))))
    end_coordinate = Coordinate(*list(map(int, coordinates[1].split(","))))

    if instruction.startswith("toggle"):
        grid.toggle(start=start_coordinate, end=end_coordinate)
        elvish_grid.toggle(start=start_coordinate, end=end_coordinate)
    elif instruction.startswith("turn on"):
        grid.switch(start=start_coordinate, end=end_coordinate, is_on=True)
        elvish_grid.switch(start=start_coordinate, end=end_coordinate, is_on=True)
    elif instruction.startswith("turn off"):
        grid.switch(start=start_coordinate, end=end_coordinate, is_on=False)
        elvish_grid.switch(start=start_coordinate, end=end_coordinate, is_on=False)

print(f"PART ONE: {grid.on_lights}")
print(f"PART TWO: {elvish_grid.on_lights}")
