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

    def get_value_by_coordinates(self, row: int, column: int) -> int:
        target_row = row + column - 1
        target_row_as_step = sum(range(2, target_row))
        self._step(step_size=target_row_as_step)
        self._step(step_size=column)
        return self.initial_code


def get_coordinates_from_data(coordinate_data: str) -> tuple[int, int]:
    row, column = re.findall(r"\D*(\d*)\D*(\d*)\.$", coordinate_data)[0]
    return int(row), int(column)


data_row, data_column = get_coordinates_from_data(coordinate_data=data)

coder = Coder(initial_code=20151125)
part_one_code = coder.get_value_by_coordinates(row=data_row, column=data_column)

print(f"PART ONE: {part_one_code}")
print(f"PART TWO: {None}")
