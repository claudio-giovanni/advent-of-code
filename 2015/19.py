import re

data = open("19.txt").read().splitlines()
conversion_data = data[:-2]
conversion_data = tuple((c[0], c[1]) for conversion in conversion_data if (c := conversion.split(" => ")))

molecule_data = data[-1]


class FusionPlant:
    def __init__(self, molecule: str, conversion: tuple[tuple[str, str]]):
        self.molecule = molecule
        self.conversions = conversion
        self.mutations: set[str] = set()

    def calibrate(self) -> int:
        for partial, replacement in self.conversions:
            for match in re.finditer(partial, self.molecule):
                self.mutations.add(f"{self.molecule[:match.start()]}{replacement}{self.molecule[match.end():]}")
        return len(self.mutations)


fusion_plant = FusionPlant(molecule=molecule_data, conversion=conversion_data)
print(f"PART ONE: {fusion_plant.calibrate()}")
