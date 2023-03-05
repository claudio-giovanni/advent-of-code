from __future__ import annotations

from dataclasses import dataclass

data = open("04.txt").read().splitlines()


@dataclass
class Section:
    start: int
    end: int

    def is_subset(self, other: Section) -> bool:
        return other.start >= self.start and other.end <= self.end


class SectionPair:
    def __init__(self, section_one: Section, section_two: Section):
        self.section_one = section_one
        self.section_two = section_two

    def has_redundant_sections(self) -> bool:
        return self.section_one.is_subset(self.section_two) or self.section_two.is_subset(self.section_one)

    def has_overlapping_sections(self) -> bool:
        return self.section_one.start <= self.section_two.end and self.section_two.start <= self.section_one.end


section_pairs = []
for datum in data:
    pair = [Section(*map(int, section.split("-"))) for section in datum.split(",")]
    section_pairs.append(SectionPair(section_one=pair[0], section_two=pair[1]))

print(f"PART ONE: {sum(pair.has_redundant_sections() for pair in section_pairs)}")
print(f"PART TWO: {sum(pair.has_overlapping_sections() for pair in section_pairs)}")
