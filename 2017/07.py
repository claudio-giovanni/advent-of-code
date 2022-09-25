from __future__ import annotations

import re
from collections import Counter
from typing import Optional

data = open("07.txt").read().splitlines()


class Disc:
    def __init__(self, name: str):
        self.name = name
        self.weight: int = 0
        self.children: list[Disc] = []
        self.parent: Optional[Disc] = None

    @property
    def tree_weight(self) -> int:
        return self.weight + sum(child.tree_weight for child in self.children)


class DiscTree:
    def __init__(self, disc_map: dict[str, Disc]):
        self.disc_map = disc_map

    def get_head(self) -> Disc:
        temp_disc = next(iter(self.disc_map.values()))
        while temp_disc.parent:
            temp_disc = temp_disc.parent
        return temp_disc

    def get_disc_imbalance(self, head: Disc = None, delta: int = 0) -> int:
        head = head or self.get_head()
        unique_weights = Counter(child.tree_weight for child in head.children).most_common(2)
        if len(unique_weights) != 2:
            return head.weight + delta
        common_tree_weight, imbalanced_tree_weight = unique_weights[0][0], unique_weights[1][0]
        head = [child for child in head.children if child.tree_weight == imbalanced_tree_weight][0]
        weight_delta = common_tree_weight - imbalanced_tree_weight
        return self.get_disc_imbalance(head=head, delta=weight_delta)

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
                child_disc.parent = parent_disc
                parent_disc.children.append(child_disc)
        return cls(disc_map=disc_map)


disc_tree = DiscTree.from_string(disc_data=data)
print(f"PART ONE: {disc_tree.get_head().name}")
print(f"PART TWO: {disc_tree.get_disc_imbalance()}")
