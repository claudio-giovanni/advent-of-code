from itertools import combinations


class Refrigerator:
    def __init__(self, size: int, containers: list[int]):
        self.size = size
        self.containers = containers
        self.container_combinations = self._get_combination_count()

    def _get_combination_count(self) -> list[tuple]:
        return [comb for i in range(self.size) for comb in combinations(self.containers, i) if sum(comb) == self.size]


data = list(map(int, open("17.txt").read().splitlines()))
refrigerator = Refrigerator(size=150, containers=data)

print(f"PART ONE: {len(refrigerator.container_combinations)}")
min_combination = min(len(comb) for comb in refrigerator.container_combinations)
print(f"PART TWO: {len([comb for comb in refrigerator.container_combinations if len(comb) == min_combination])}")
