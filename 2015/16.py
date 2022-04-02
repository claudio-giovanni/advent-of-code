import re
from typing import TypedDict


class Aunt(TypedDict, total=False):
    id: int
    children: int
    cats: int
    samoyeds: int
    pomeranians: int
    akitas: int
    vizslas: int
    goldfish: int
    trees: int
    cars: int
    perfumes: int


def create_aunt(aunt_string: str) -> Aunt:
    keys = re.findall(r"[A-z]+", aunt_string)[1::]
    values = list(map(int, re.findall(r"\d+", aunt_string)))
    aunt_id = values.pop(0)
    aunt_properties = dict(zip(keys, values))
    aunt_properties["id"] = aunt_id
    return Aunt(**aunt_properties)


class AuntIdentifier:
    def __init__(self, aunt_definitions: list[str]):
        self.aunts: list[Aunt] = [create_aunt(aunt_string=datum) for datum in aunt_definitions]

    def find_aunt(self, target_aunt: Aunt) -> Aunt:
        for aunt in self.aunts:
            if all(feature in aunt.items() for feature in target_aunt.items() if feature[0] in aunt):
                return aunt

    def find_aunt_v2(self, target_aunt: Aunt) -> Aunt:
        greater_keys = ["cats", "trees"]
        lesser_keys = ["pomeranians", "goldfish"]
        equal_keys = ["children", "samoyeds", "akitas", "vizslas", "cars", "perfumes"]
        for aunt in self.aunts:
            if all(aunt[key] <= target_aunt[key] for key in greater_keys if key in aunt):
                continue
            if all(aunt[key] >= target_aunt[key] for key in lesser_keys if key in aunt):
                continue
            if all(aunt[key] != target_aunt[key] for key in equal_keys if key in aunt):
                continue
            return aunt


aunt_data = open("16.txt").read().splitlines()
identifier = AuntIdentifier(aunt_definitions=aunt_data)
sue = Aunt(children=3, cats=7, samoyeds=2, pomeranians=3, akitas=0, vizslas=0, goldfish=5, trees=3, cars=2, perfumes=1)

print(f"PART ONE: {identifier.find_aunt(target_aunt=sue)['id']}")
print(f"PART TWO: {identifier.find_aunt_v2(target_aunt=sue)['id']}")
