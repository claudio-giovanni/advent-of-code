from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto

data = open("23.txt").read().splitlines()


# noinspection PyArgumentList
class Command(Enum):
    HLF = auto()
    TPL = auto()
    INC = auto()
    JMP = auto()
    JIE = auto()
    JIO = auto()

    def execute(self, register: Register) -> bool:
        if self == Command.HLF:
            register.value //= 2
            return True
        elif self == Command.TPL:
            register.value *= 3
            return True
        elif self == Command.INC:
            register.value += 1
            return True
        elif self == Command.JMP:
            return True
        elif self == Command.JIE and register.value % 2 == 0:
            return True
        elif self == Command.JIO and register.value == 1:
            return True
        return False


@dataclass
class Register:
    value: int = field(init=False, default=0)


@dataclass
class Computer:
    registers: dict[str, Register] = field(init=False, default_factory=dict)

    def execute_instructions(self, instructions: list[Instruction], pointer: int = 0):
        for i, instruction in enumerate(instructions[pointer:], start=pointer):
            register = self.registers.setdefault(instruction.register_name, Register())
            if instruction.command.execute(register=register) and instruction.offset:
                return self.execute_instructions(instructions=instructions, pointer=i + instruction.offset)


@dataclass
class Instruction:
    command: Command
    register_name: str
    offset: int = None

    @classmethod
    def get_instructions_from_data(cls, instruction_data: list[str]) -> list[Instruction]:
        instructions = []
        for instruction in instruction_data:
            command, register_name, offset = re.findall(r"([a-z]{3}) ([a-z])?(?:, )?([+\-]\d+)?$", instruction)[0]
            command = Command[command.upper()]
            if offset:
                offset = int(offset[1:]) if offset[0] == "+" else -int(offset[1:])
            instructions.append(cls(command=command, register_name=register_name, offset=offset or None))
        return instructions


data_instructions = Instruction.get_instructions_from_data(instruction_data=data)
computer = Computer()
computer.execute_instructions(instructions=data_instructions)
print(f"PART ONE: {computer.registers['b'].value}")

computer2 = Computer()
setup_instructions = [Instruction(command=Command.INC, register_name="a")]
computer2.execute_instructions(instructions=setup_instructions)
computer2.execute_instructions(data_instructions)
print(f"PART TWO: {computer2.registers['b'].value}")
