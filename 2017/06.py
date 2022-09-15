from __future__ import annotations

import re
from itertools import chain, count, cycle

data = open("06.txt").read().strip()


class Memory:
    def __init__(self, banks: list[int]):
        self.banks = banks
        self.reallocation_count = 0

    @property
    def banks_hash(self) -> int:
        return hash("".join([str(bank) for bank in self.banks]))

    def _get_highest_bank_index(self) -> int:
        target_bank = max(self.banks)
        return self.banks.index(target_bank)

    def reallocate(self) -> None:
        target_index = self._get_highest_bank_index()
        target_value = self.banks[target_index]
        self.banks[target_index] = 0
        revolving_indexes = chain(range(target_index + 1, len(self.banks)), range(0, target_index + 1))
        for index, _ in zip(cycle(revolving_indexes), range(target_value)):
            self.banks[index] += 1

    def reallocate_to_repetition(self) -> None:
        hash_cash = {self.banks_hash}
        for i in count(1):
            self.reallocate()
            self.reallocation_count = i
            if self.banks_hash in hash_cash:
                return
            hash_cash.add(self.banks_hash)

    @classmethod
    def from_string(cls, bank_data: str) -> Memory:
        numbers = re.findall(r"\d+", bank_data)
        banks = [int(number) for number in numbers]
        return cls(banks=banks)


memory = Memory.from_string(bank_data=data)
memory.reallocate_to_repetition()

print(f"PART ONE: {memory.reallocation_count}")
print(f"PART TWO: {None}")
