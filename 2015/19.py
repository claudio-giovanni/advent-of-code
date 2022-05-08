import re
import random

data = open("19.txt").read().splitlines()
conversion_data = data[:-2]
conversion_data = list((c[0], c[1]) for conversion in conversion_data if (c := conversion.split(" => ")))

molecule_data = data[-1]


class FusionPlant:
    def __init__(self, conversion: list[tuple[str, str]]):
        self.conversions = conversion

    def calibrate(self, molecule: str) -> set[str]:
        mutations: set[str] = set()
        for reactant, product in self.conversions:
            for match in re.finditer(reactant, molecule):
                mutations.add(f"{molecule[:match.start()]}{product}{molecule[match.end():]}")
        return mutations

    # Forgive them for they know not what they do
    def fabricate(self, start_molecule: str, end_molecule: str) -> int:
        count = 0
        while end_molecule != start_molecule:
            reactant, product = random.choice(self.conversions)
            if product in end_molecule:
                end_molecule = end_molecule.replace(product, reactant, 1)
                count += 1
        return count


fusion_plant = FusionPlant(conversion=conversion_data)
print(f"PART ONE: {len(fusion_plant.calibrate(molecule_data))}")
print(f"PART TWO: {fusion_plant.fabricate(start_molecule='e', end_molecule=molecule_data)}")
