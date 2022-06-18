from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

data = open("04.txt").read().split("\n\n")


class Validation:
    _required_tags = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}
    _valid_ecl_values = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")

    @staticmethod
    def easy_validation(tags: dict[str, str]) -> bool:
        return Validation._required_tags <= tags.keys()

    @staticmethod
    def advanced_validation(tags: dict[str, str]) -> bool:
        if not Validation.easy_validation(tags=tags):
            return False
        valid_byr = 1920 <= int(tags["byr"]) <= 2002
        valid_iyr = 2010 <= int(tags["iyr"]) <= 2020
        valid_eyr = 2020 <= int(tags["eyr"]) <= 2030
        valid_hgt = Validation._is_valid_hgt(hgt=tags["hgt"])
        valid_hcl = bool(re.findall(r"#[\da-f]{6}$", tags["hcl"]))
        valid_ecl = tags["ecl"] in Validation._valid_ecl_values
        valid_pid = tags["pid"].isdigit() and len(tags["pid"]) == 9
        return all((valid_byr, valid_iyr, valid_eyr, valid_hgt, valid_hcl, valid_ecl, valid_pid))

    @staticmethod
    def _is_valid_hgt(hgt: str) -> bool:
        if hgt.endswith("cm"):
            return 150 <= int(hgt[:-2]) <= 193
        if hgt.endswith("in"):
            return 59 <= int(hgt[:-2]) <= 76
        return False


@dataclass
class Passport:
    tags: dict[str, str]

    def is_valid(self, validation: Callable[[dict[str, str]], bool]) -> bool:
        return validation(self.tags)

    @staticmethod
    def get_passport_from_string(passport_data: str) -> Passport:
        tags = re.findall(r"([a-zA-Z]{3}):([^\s\n]+)", passport_data)
        return Passport(tags={tag[0]: tag[1] for tag in tags})


passports = [Passport.get_passport_from_string(passport_data=datum) for datum in data]

print(f"PART ONE: {sum(p.is_valid(validation=Validation.easy_validation) for p in passports)}")
print(f"PART TWO: {sum(p.is_valid(validation=Validation.advanced_validation) for p in passports)}")
