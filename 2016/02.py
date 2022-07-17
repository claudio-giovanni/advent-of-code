from dataclasses import dataclass, field
from enum import Enum
from typing import Any

data = open("02.txt").read().splitlines()


class Direction(Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)


class Keypad:
    def __init__(self, grid: tuple[tuple[Any, ...], ...], row: int, column: int):
        self.grid = grid
        self.row = row
        self.column = column
        self.max_row = len(self.grid)
        self.max_column = len(self.grid[0])

    @property
    def value(self) -> str:
        return str(self.grid[self.row][self.column])

    def is_valid_move(self, row: int, column: int) -> bool:
        return (0 <= row < self.max_row) and (0 <= column < self.max_column)

    def move(self, directions: list[Direction]):
        for direction in directions:
            row_delta, column_delta = direction.value
            row = self.row + row_delta
            column = self.column + column_delta
            if self.is_valid_move(row=row, column=column):
                self.row = row
                self.column = column


class BasicKeypad(Keypad):
    grid = ((1, 2, 3), (4, 5, 6), (7, 8, 9))

    def __init__(self, row=1, column=1):
        super(BasicKeypad, self).__init__(grid=self.grid, row=row, column=column)


class AdvancedKeypad(Keypad):
    grid = (
        (None, None, 1, None, None),
        (None, 2, 3, 4, None),
        (5, 6, 7, 8, 9),
        (None, "A", "B", "C", None),
        (None, None, "D", None, None),
    )

    def __init__(self, row=2, column=0):
        super(AdvancedKeypad, self).__init__(self.grid, row=row, column=column)

    def is_valid_move(self, row: int, column: int) -> bool:
        return super().is_valid_move(row=row, column=column) and self.grid[row][column]


@dataclass
class BathroomLock:
    keypad: Keypad
    combination: str = field(init=False, repr=True, default="")

    def resolve_combination(self, combination_directions: list[list[Direction]]):
        for directions in combination_directions:
            self.keypad.move(directions=directions)
            self.combination += self.keypad.value


def get_direction_lines_from_string(direction_data: list[str]) -> list[list[Direction]]:
    return [[Direction[char] for char in datum] for datum in direction_data]


combinations_data = get_direction_lines_from_string(direction_data=data)
basic_lock = BathroomLock(keypad=BasicKeypad())
basic_lock.resolve_combination(combination_directions=combinations_data)
print(f"PART ONE: {basic_lock.combination}")

advanced_lock = BathroomLock(keypad=AdvancedKeypad())
advanced_lock.resolve_combination(combination_directions=combinations_data)
print(f"PART TWO: {advanced_lock.combination}")
