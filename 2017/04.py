from collections import Counter
from dataclasses import dataclass
from typing import Callable

data = open("04.txt").read().splitlines()


class Validator:
    @staticmethod
    def check_duplicates(text: str) -> bool:
        return set(Counter(text.split()).values()) == {1}

    @staticmethod
    def check_anagrams(text: str) -> bool:
        ordered_text = " ".join("".join(sorted(word)) for word in text.split())
        return Validator.check_duplicates(text=ordered_text)


@dataclass
class Passphrase:
    text: str

    def is_valid(self, validator: Callable[[str], bool]) -> bool:
        return validator(self.text)


passphrases = [Passphrase(text=datum) for datum in data]

print(f"PART ONE: {sum(passphrase.is_valid(validator=Validator.check_duplicates) for passphrase in passphrases)}")
print(f"PART TWO: {sum(pass_phrase.is_valid(validator=Validator.check_anagrams) for pass_phrase in passphrases)}")
