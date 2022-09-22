from __future__ import annotations

import re
from collections import Counter

data = open("07.txt").read().splitlines()


class Disc:
    def __init__(self, name: str):
        self.name = name
        self.weight: int = 0
        self.children: list[Disc] = []
        self.parents: list[Disc] = []

    @property
    def tree_weight(self) -> int:
        total_weight = self.weight
        children_lineage = self.children[:]
        for child in children_lineage:
            total_weight += child.weight
            if child.children:
                children_lineage.extend(child.children)
        return total_weight


class DiscTree:
    def __init__(self, disc_map: dict[str, Disc]):
        self.disc_map = disc_map

    def get_head(self) -> Disc:
        for disc in self.disc_map.values():
            if disc.parents:
                continue
            return disc

    def get_disc_imbalance(self) -> int:
        head = self.get_head()
        unique_disc_weights = Counter(child.tree_weight for child in head.children).most_common(2)
        if len(unique_disc_weights) == 2:
            common_tree_weight, imbalanced_tree_weight = unique_disc_weights[0][0], unique_disc_weights[1][0]
            imbalanced_disc = [child for child in head.children if child.tree_weight == imbalanced_tree_weight][0]
            weight_delta = common_tree_weight - imbalanced_tree_weight
            return imbalanced_disc.weight + weight_delta

    @classmethod
    def from_string(cls, disc_data: list[str]) -> DiscTree:
        disc_map = {}
        for datum in disc_data:
            name, weight, children = re.findall(r"(\w+) \((\d+)\)(?: -> (.*))?", datum)[0]
            parent_disc = disc_map.setdefault(name, Disc(name=name))
            parent_disc.weight = int(weight)
            if not children:
                continue
            for child_name in children.split(","):
                child_name = child_name.strip()
                child_disc = disc_map.setdefault(child_name, Disc(name=child_name))
                child_disc.parents.append(parent_disc)
                parent_disc.children.append(child_disc)
        return cls(disc_map=disc_map)


disc_tree = DiscTree.from_string(disc_data=data)
print(f"PART ONE: {disc_tree.get_head().name}")
print(f"PART TWO: {disc_tree.get_disc_imbalance()}")
