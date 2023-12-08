import re
from dataclasses import dataclass
from typing import Iterator

data = open("03.txt").read().splitlines()


@dataclass
class EnginePart:
    value: int
    location: tuple[int, int]
    row: int


class EngineSchematic:
    def __init__(self, lines: list[str]) -> None:
        self.lines = lines
        self.length = len(lines)

    def _valid_line(self, line_number: int, start_index: int, end_index: int) -> bool:
        searchable = self.lines[line_number][start_index:end_index]
        return re.search(r"[^\d.]", searchable) is not None

    def _check_part_is_valid(self, part: EnginePart) -> bool:
        start_index = (part.location[0] or 1) - 1
        end_index = part.location[1] + 1
        if part.row > 0 and self._valid_line(line_number=part.row - 1, start_index=start_index, end_index=end_index):
            return True
        if self._valid_line(line_number=part.row, start_index=start_index, end_index=end_index):
            return True
        if part.row < self.length - 1 and self._valid_line(
            line_number=part.row + 1, start_index=start_index, end_index=end_index
        ):
            return True

    @staticmethod
    def _get_parts_from_line(line: str, row: int) -> list[EnginePart]:
        parts = []
        for match in re.finditer(r"\d+", line):
            part = EnginePart(value=int(match.group()), location=(match.start(), match.end()), row=row)
            parts.append(part)
        return parts

    def get_parts(self) -> Iterator[EnginePart]:
        for i, line in enumerate(self.lines):
            parts = self._get_parts_from_line(line=line, row=i)
            for part in parts:
                if self._check_part_is_valid(part=part):
                    yield part


schematic = EngineSchematic(data)

valid_parts = list(schematic.get_parts())
valid_parts_total = sum(part.value for part in valid_parts)
print(f"PART ONE: {valid_parts_total}")

print(f"PART TWO: {None}")
