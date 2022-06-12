from dataclasses import dataclass
from itertools import permutations

data = map(lambda row: row.split(), open("02.txt").read().splitlines())
data = [list(map(int, datum)) for datum in data]


@dataclass
class Row:
    values: list[int]

    @property
    def checksum(self) -> int:
        return max(self.values) - min(self.values)

    @property
    def paired_checksum(self) -> int:
        for a, b in permutations(self.values, 2):
            if a % b == 0:
                return a // b


@dataclass
class Spreadsheet:
    rows: list[Row]

    @property
    def checksum(self) -> int:
        return sum([row.checksum for row in self.rows])

    @property
    def paired_checksum(self) -> int:
        return sum([row.paired_checksum for row in self.rows])


spreadsheet = Spreadsheet([Row(datum) for datum in data])

print(f"PART ONE: {spreadsheet.checksum}")
print(f"PART TWO: {spreadsheet.paired_checksum}")
