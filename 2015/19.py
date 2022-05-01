import re

data = open("19.txt").read().splitlines()
conversion_data = data[:-2]
conversion_data = tuple((c[0], c[1]) for conversion in conversion_data if (c := conversion.split(" => ")))

molecule_data = data[-1]


class FusionPlant:
    def __init__(self, conversion: tuple[tuple[str, str]]):
        self.conversions = conversion
        self.successful_fabrications = []

    def calibrate(self, molecule: str) -> set[str]:
        mutations: set[str] = set()
        for partial, replacement in self.conversions:
            for match in re.finditer(partial, molecule):
                mutations.add(f"{molecule[:match.start()]}{replacement}{molecule[match.end():]}")
        return mutations

    def fabricate(self, current_molecule: str, end_molecule: str, iteration: int = 1) -> int:
        for mutation in self.calibrate(molecule=current_molecule):
            if mutation == end_molecule:
                self.successful_fabrications.append(iteration)
            if len(mutation) > len(end_molecule):
                continue
            self.fabricate(current_molecule=mutation, end_molecule=end_molecule, iteration=iteration + 1)
        return min(self.successful_fabrications, default=0)


fusion_plant = FusionPlant(conversion=conversion_data)
print(f"PART ONE: {len(fusion_plant.calibrate(molecule_data))}")
print(f"PART TWO: {fusion_plant.fabricate(current_molecule='e', end_molecule=molecule_data)}")
