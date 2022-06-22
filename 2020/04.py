from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TypedDict

data = open("04.txt").read().split("\n\n")


class Passport(TypedDict, total=False):
    byr: str
    iyr: str
    eyr: str
    hgt: str
    hcl: str
    ecl: str
    pid: str


def get_passport_from_string(passport_data: str) -> Passport:
    tags = re.findall(r"([a-zA-Z]{3}):([^\s\n]+)", passport_data)
    return {tag[0]: tag[1] for tag in tags}


@dataclass
class EasyValidator:
    _required_tags = {"ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"}

    @classmethod
    def validate(cls, passport: Passport) -> bool:
        return cls._required_tags <= passport.keys()


@dataclass
class AdvancedValidator:
    _valid_ecl_values = ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
    _easy_validation = EasyValidator.validate

    @classmethod
    def validate(cls, passport: Passport) -> bool:
        if not cls._easy_validation(passport=passport):
            return False
        valid_byr = 1920 <= int(passport["byr"]) <= 2002
        valid_iyr = 2010 <= int(passport["iyr"]) <= 2020
        valid_eyr = 2020 <= int(passport["eyr"]) <= 2030
        valid_hgt = cls._is_valid_hgt(hgt=passport["hgt"])
        valid_hcl = bool(re.findall(r"#[\da-f]{6}$", passport["hcl"]))
        valid_ecl = passport["ecl"] in cls._valid_ecl_values
        valid_pid = passport["pid"].isdigit() and len(passport["pid"]) == 9
        return all((valid_byr, valid_iyr, valid_eyr, valid_hgt, valid_hcl, valid_ecl, valid_pid))

    @staticmethod
    def _is_valid_hgt(hgt: str) -> bool:
        if hgt.endswith("cm"):
            return 150 <= int(hgt[:-2]) <= 193
        if hgt.endswith("in"):
            return 59 <= int(hgt[:-2]) <= 76
        return False


passports = [get_passport_from_string(passport_data=datum) for datum in data]

validated_passports = [EasyValidator.validate(passport=passport) for passport in passports]
print(f"PART ONE: {sum(validated_passports)}")

validated_passports = [AdvancedValidator.validate(passport=passport) for passport in passports]
print(f"PART TWO: {sum(validated_passports)}")
