import re
from dataclasses import dataclass
from typing import Iterator

data = open("02.txt").read().splitlines()


@dataclass
class Password:
    key: str
    key_lower: int
    key_upper: int
    password: str

    @property
    def is_valid_at_sled_rental(self) -> bool:
        return self.key_upper >= self.password.count(self.key) >= self.key_lower

    @property
    def is_valid_at_tcp(self) -> bool:
        match_count = (self.password[self.key_lower - 1] == self.key) + (self.password[self.key_upper - 1] == self.key)
        return match_count == 1


def parse_password_from_file(password_data: list[str]) -> Iterator[Password]:
    for password_datum in password_data:
        key_lower, key_upper, key, password = re.findall(r"(\d+)-(\d+)\s([a-zA-Z]):\s(.*)", password_datum)[0]
        yield Password(key=key, key_lower=int(key_lower), key_upper=int(key_upper), password=password)


valid_passwords = sum(pwd.is_valid_at_sled_rental for pwd in parse_password_from_file(password_data=data))

print(f"PART ONE: {valid_passwords}")

valid_passwords = sum(pwd.is_valid_at_tcp for pwd in parse_password_from_file(password_data=data))

print(f"PART TWO: {valid_passwords}")
