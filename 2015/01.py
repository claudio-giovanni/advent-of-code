from collections import Counter

data = list(open("01.txt").read())


class Elevator:
    def __init__(self, instructions: list[str]):
        self.instructions = instructions

    @property
    def last_floor(self) -> int:
        counter = Counter(self.instructions)
        return counter.get("(", 0) - counter.get(")", 0)

    def get_first_basement_step(self) -> int:
        floor = 0
        for i, instruction in enumerate(self.instructions, 1):
            floor += 1 if instruction == "(" else -1
            if floor == -1:
                return i


elevator = Elevator(instructions=data)
print(f"PART ONE: {elevator.last_floor}")
print(f"PART TWO: {elevator.get_first_basement_step()}")
