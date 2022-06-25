import re
from dataclasses import dataclass
from itertools import count

data = open("25.txt").read().splitlines()[0]


@dataclass
class Coder:
    initial_code: int

    def _step(self, step_size: int = 1) -> None:
        for step in range(step_size):
            self.initial_code = (self.initial_code * 252533) % 33554393

    def get_value_by_coordinates(self, y: int, x: int) -> int:
        target_row = y + x - 1
        for row in count(2, 1):
            if target_row != row:
                self._step(step_size=row)
                continue
            for column in range(1, row):
                self._step()
                if column == x:
                    return self.initial_code


def get_coordinates_from_data(coordinate_data: str) -> tuple[int, int]:
    row, column = re.findall(r"\D*(\d*)\D*(\d*)\.$", coordinate_data)[0]
    return int(row), int(column)


data_row, data_column = get_coordinates_from_data(coordinate_data=data)

coder = Coder(initial_code=20151125)
part_one_code = coder.get_value_by_coordinates(y=data_row, x=data_column)

print(f"PART ONE: {part_one_code}")
print(f"PART TWO: {None}")
