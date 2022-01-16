from collections import Counter
from itertools import groupby

data = open("05.txt").readlines()
VOWELS = "aeiou"
NAUGHTY_STRINGS = ["ab", "cd", "pq", "xy"]


class Kid:

    def __init__(self, name: str):
        self.name = name

    def is_nice_old(self) -> bool:
        return self._check_nice_rules() and not self._check_naughty_rules()

    def is_nice_new(self) -> bool:
        duplicate_pair_check = any(self.name.count(self.name[i:i + 2]) > 1 for i in range(len(self.name) - 1))
        letter_sandwich_check = any(self.name[i] == self.name[i + 2] for i in range(len(self.name) - 2))
        return duplicate_pair_check and letter_sandwich_check

    def _check_nice_rules(self) -> bool:
        name = Counter(self.name)
        vowel_check = sum(name.get(vowel, 0) for vowel in VOWELS) >= 3
        consecutive_check = any(len(list(count)) > 1 for _, count in groupby(self.name))
        return vowel_check and consecutive_check

    def _check_naughty_rules(self) -> bool:
        return any(naughty_string in self.name for naughty_string in NAUGHTY_STRINGS)


print(f"PART ONE: {sum(Kid(datum).is_nice_old() for datum in data)}")
print(f"PART TWO: {sum(Kid(datum).is_nice_new() for datum in data)}")

