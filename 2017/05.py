from dataclasses import dataclass, field
from math import inf

data = list(map(int, open("05.txt").read().splitlines()))


@dataclass
class Register:
    instructions: list[int] = field(init=True, repr=False)
    counter: int = field(init=False, default=0)

    def __post_init__(self):
        self.instructions = self.instructions.copy()

    def execute_instructions(self, offset_limit: int = inf) -> None:
        instruction_pointer = 0
        instructions_length = len(self.instructions)
        while instruction_pointer < instructions_length:
            offset = self.instructions[instruction_pointer]
            self.counter += 1
            self.instructions[instruction_pointer] = offset + 1 if offset < offset_limit else offset - 1
            instruction_pointer += offset


register = Register(instructions=data)
register.execute_instructions()
print(f"PART ONE: {register.counter}")

register2 = Register(instructions=data)
register2.execute_instructions(offset_limit=3)
print(f"PART TWO: {register2.counter}")
