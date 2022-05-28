import pprint
from typing import Optional


class BingoBoard:
    def __init__(self, numbers: list[str]):
        self.numbers = numbers
        self.table: list[list[str]] = []
        for i in range(5):
            self.table.append([number for number in numbers[i * 5 : (i + 1) * 5]])

    def check_bingo(self, draw: str) -> Optional[int]:
        for i, row in enumerate(self.table):
            self.table[i] = [number if number != draw else None for number in row]
        if self._is_row_bingo() or self._is_column_bingo():
            return self._sum_remaining_numbers() * int(draw)

    def _is_row_bingo(self) -> bool:
        for row in self.table:
            if all(number is None for number in row):
                return True

    def _is_column_bingo(self) -> bool:
        for i in range(5):
            if all(row[i] is None for row in self.table):
                return True

    def _sum_remaining_numbers(self) -> int:
        return sum(int(number) for row in self.table for number in row if number is not None)

    def __str__(self):
        return f"BingoBoard(\n{pprint.pformat(self.table, indent=2)})"


board_numbers = open("04.txt").read().split("\n\n")
bingo_numbers = open("04_2.txt").read().split(",")
board_numbers = [number.strip() for table in board_numbers for number in table.replace("\n", " ").split()]
boards = [BingoBoard(board_numbers[i * 25 : (i + 1) * 25]) for i in range(len(board_numbers) // 25)]

bingo_map = dict()
for bingo_number in bingo_numbers:
    for board in boards[::]:
        if score := board.check_bingo(bingo_number):
            bingo_map[bingo_number] = score
            boards.remove(board)

print("PART ONE: ", list(bingo_map.values())[0])
print("PART TWO: ", list(bingo_map.values())[-1])
