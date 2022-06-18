import math
from dataclasses import dataclass
from itertools import combinations

data = list(map(int, (open("24.txt").read().splitlines())))


@dataclass
class SlayCalculator:
    packages: list[int]

    @staticmethod
    def _filter_arrangements_by_weight(packages: list[int], weight: int) -> list[tuple[int, ...]]:
        for package_count in range(1, len(packages)):
            valid_packages = [package for package in combinations(packages, r=package_count) if sum(package) == weight]
            if valid_packages:
                return valid_packages

    @staticmethod
    def _find_optimal_arrangement_qe(package_arrangements: list[tuple[int, ...]]) -> int:
        return min(math.prod(package) for package in package_arrangements)

    def get_front_compartment_configuration(self, compartments: int) -> int:
        compartment_weight = sum(self.packages) // compartments
        arrangements = self._filter_arrangements_by_weight(packages=self.packages, weight=compartment_weight)
        return self._find_optimal_arrangement_qe(package_arrangements=arrangements)


calculator = SlayCalculator(packages=data)

print(f"PART ONE: {calculator.get_front_compartment_configuration(compartments=3)}")
print(f"PART TWO: {calculator.get_front_compartment_configuration(compartments=4)}")
