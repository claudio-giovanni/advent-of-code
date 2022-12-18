from collections import Counter
from dataclasses import dataclass
from string import ascii_letters

data = open("03.txt").read().splitlines()


@dataclass
class Item:
    name: str
    priority: int = None

    def __post_init__(self):
        self.priority = ascii_letters.index(self.name) + 1


class RuckSack:
    def __init__(self, items_string: str):
        items_length = len(items_string) // 2
        items_compartments = items_string[:items_length], items_string[items_length:]
        self.compartment_one = Counter(items_compartments[0])
        self.compartment_two = Counter(items_compartments[1])

    def get_duplicate_item(self) -> Item:
        item_name = (self.compartment_one.keys() & self.compartment_two.keys()).pop()
        return Item(name=item_name)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.compartment_one}, {self.compartment_two})"


class RuckSackGroup:
    def __init__(self, sacks: tuple[str]):
        self.sacks = sacks

    def get_duplicate_item(self) -> Item:
        item_name = set(self.sacks[0]).intersection(*self.sacks[1:]).pop()
        return Item(name=item_name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.sacks})"


ruck_sacks = [RuckSack(items_string=datum) for datum in data]
duplicates_total = sum(sack.get_duplicate_item().priority for sack in ruck_sacks)
print(f"PART ONE: {duplicates_total}")

ruck_groups = [RuckSackGroup(sacks=sacks) for sacks in zip(*(iter(data),) * 3)]
duplicates_total = sum(group.get_duplicate_item().priority for group in ruck_groups)
print(f"PART TWO: {duplicates_total}")
