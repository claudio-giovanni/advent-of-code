from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

data = open("23.txt").read().splitlines()


# noinspection PyArgumentList
class Command(Enum):
    HLF = auto()
    TPL = auto()
    INC = auto()
    JMP = auto()
    JIE = auto()
    JIO = auto()

    def execute(self, register: Register) -> None:
        if self == Command.HLF:
            register.value //= 2
            register.offset = None
        elif self == Command.TPL:
            register.value *= 3
            register.offset = None
        elif self == Command.INC:
            register.value += 1
            register.offset = None
        elif self == Command.JMP:
            return
        elif self == Command.JIE:
            register.offset = register.offset if register.value % 2 == 0 else None
        elif self == Command.JIO:
            register.offset = register.offset if register.value == 1 else None


@dataclass
class Register:
    value: int = field(init=False, default=0)
    offset: Optional[int] = field(init=False, default=None)

    def execute_command(self, command: Command, offset: int) -> None:
        self.offset = offset
        command.execute(register=self)


@dataclass
class Computer:
    registers: dict[str, Register] = field(init=False, default_factory=dict)

    def execute_instructions(self, instructions: list[Instruction], pointer: int = 0):
        for i, instruction in enumerate(instructions[pointer:], start=pointer):
            register = self.registers.setdefault(instruction.register_name, Register())
            register.execute_command(command=instruction.command, offset=instruction.offset)
            if offset := register.offset:
                return self.execute_instructions(instructions=instructions, pointer=i + offset)


@dataclass
class Instruction:
    command: Command
    register_name: str
    offset: int = None

    @staticmethod
    def get_instructions_from_data(instruction_data: list[str]) -> list[Instruction]:
        instructions = []
        for instruction in instruction_data:
            command, register_name, offset = re.findall(r"([a-z]{3}) ([a-z])?(?:, )?([+\-]\d+)?$", instruction)[0]
            command = Command[command.upper()]
            if offset:
                offset = int(offset[1:]) if offset[0] == "+" else -int(offset[1:])
            instructions.append(Instruction(command=command, register_name=register_name, offset=offset or None))
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
