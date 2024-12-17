from __future__ import annotations

from itertools import pairwise

data = open("02.txt").read().splitlines()


class Report:
    def __init__(self, levels: list[int]):
        self.levels = levels

    @staticmethod
    def from_string(levels: str) -> Report:
        return Report(levels=[int(level) for level in levels.split()])

    def _is_sorted(self) -> bool:
        ordered_levels = sorted(self.levels)
        return self.levels == ordered_levels or self.levels == ordered_levels[::-1]

    def _is_adjacent(self):
        for i, j in pairwise(self.levels):
            level_diff = abs(i - j)
            if 3 < level_diff or level_diff < 1:
                return False
        return True

    def is_safe(self) -> bool:
        return self._is_adjacent() and self._is_sorted()

    def is_safe_with_tolerance(self):
        if self.is_safe():
            return True
        for i in range(len(self.levels)):
            partial_report = self.levels.copy()
            partial_report.pop(i)
            if Report(levels=partial_report).is_safe():
                return True
        return False


safe_reports_count = 0
safe_reports_with_tolerance_count = 0
for datum in data:
    report = Report.from_string(levels=datum)
    safe_reports_count += report.is_safe()
    safe_reports_with_tolerance_count += report.is_safe_with_tolerance()


print(f"PART ONE: {safe_reports_count}")
print(f"PART TWO: {safe_reports_with_tolerance_count}")
