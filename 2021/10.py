import statistics
from typing import Optional

chunk_lines = open("10.txt").read().splitlines()
CHUNK_RELATION_MAP = {"(": ")", "[": "]", "<": ">", "{": "}"}
CORRUPT_CHUNK_POINT_MAP = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_CHUNK_POINT_MAP = {")": 1, "]": 2, "}": 3, ">": 4}


def find_corrupt_char(line: str) -> Optional[str]:
    """Get the first corrupt char in a line"""
    expected_closers = []
    for char in line:
        if char in CHUNK_RELATION_MAP:  # opener found
            expected_closers.append(CHUNK_RELATION_MAP[char])
        elif not expected_closers:  # closer found, when none expected
            return char
        elif char != expected_closers.pop():  # closer found, when other expected
            return char


corrupt_chars = [corrupt_char for line in chunk_lines if (corrupt_char := find_corrupt_char(line))]
print("PART ONE: ", sum(CORRUPT_CHUNK_POINT_MAP[char] for char in corrupt_chars))


def find_line_closers(line: str) -> list[str]:
    """Get the closing chunk for an incomplete line"""
    expected_closers = []
    for char in line:
        if char in CHUNK_RELATION_MAP:  # opener found
            expected_closers.append(CHUNK_RELATION_MAP[char])
        else:
            expected_closers.pop()
    return expected_closers[::-1]


def calculate_autocomplete_points(line: list[str], points=0) -> int:
    """Calculate point value for a closing chunk"""
    if line:
        points *= 5
        points += AUTOCOMPLETE_CHUNK_POINT_MAP[line.pop(0)]
        return calculate_autocomplete_points(line=line, points=points)
    return points


incomplete_lines = [line for line in chunk_lines if not find_corrupt_char(line)]
incomplete_line_closers = [find_line_closers(line) for line in incomplete_lines]
line_closer_points = sorted([calculate_autocomplete_points(line) for line in incomplete_line_closers])
median_closer_point = statistics.median(line_closer_points)

print("PART TWO: ", median_closer_point)
