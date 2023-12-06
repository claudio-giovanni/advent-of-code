import re
from typing import Iterator

data = open("01.txt").read().splitlines()

NUMERIC_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
NUMERIC_WORDS_PIPE = "|".join(NUMERIC_WORDS)
WORDS_VALUES = {word: str(i) for i, word in enumerate(NUMERIC_WORDS, start=1)}


class Calibrator:
    def __init__(self, instructions: list[str]):
        self.instructions = instructions

    def get_numeric_values(self) -> Iterator[int]:
        for instruction in self.instructions:
            digits = re.findall(r"\d", instruction)
            yield int(digits[0] + digits[-1])

    def get_alpha_numeric_values(self) -> Iterator[str]:
        for instruction in self.instructions:
            result = re.findall(rf"(?=(\d|{NUMERIC_WORDS_PIPE}))", instruction)
            first, last = result[0], result[-1]
            yield int(WORDS_VALUES.get(first, first) + WORDS_VALUES.get(last, last))


calibrator = Calibrator(instructions=data)

calibrator_numeric = sum(calibrator.get_numeric_values())
print(f"PART ONE: {calibrator_numeric}")

calibrator_alpha_numeric = sum(calibrator.get_alpha_numeric_values())
print(f"PART TWO: {calibrator_alpha_numeric}")
