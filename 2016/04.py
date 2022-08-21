from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from string import ascii_lowercase

data = open("04.txt").read().splitlines()


@dataclass
class EncryptedWord:
    value: str
    sector_id: int
    checksum: str

    @property
    def is_valid(self) -> bool:
        counter = Counter(self.value.replace("-", ""))
        _, lowest_count = counter.most_common(n=5)[-1]
        sorted_items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:5]
        valid_checksum = {char for char, count in sorted_items if count >= lowest_count}
        return set(self.checksum) == valid_checksum

    def decrypt(self) -> str:
        char_shift = self.sector_id % 26
        words = []
        for word in self.value.split("-"):
            words.append("".join(map(lambda char: ascii_lowercase[(ord(char) - ord("a") + char_shift) % 26], word)))
        return " ".join(words)

    @classmethod
    def from_string(cls, encrypted_word_data: str) -> EncryptedWord:
        value, sector_id, checksum = re.findall(r"([a-z,-]+)-(\d+)\[([a-z]+)", encrypted_word_data)[0]
        return cls(value=value, sector_id=int(sector_id), checksum=checksum)


valid_words = [encrypted_word for datum in data if (encrypted_word := EncryptedWord.from_string(datum)).is_valid]

valid_sector_id_sum = sum(word.sector_id for word in valid_words)
print(f"PART ONE: {valid_sector_id_sum}")

north_sector_id = [word.sector_id for word in valid_words if "north" in word.decrypt()][0]
print(f"PART TWO: {north_sector_id}")
