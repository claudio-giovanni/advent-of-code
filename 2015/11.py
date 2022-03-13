from itertools import pairwise

old_password = open("11.txt").readline()


class PasswordGenerator:
    BANNED_CHARS = {"i", "o", "l"}

    def __init__(self, password: str):
        self.password = password

    def increment_password(self) -> str:
        self.password = self.increment_character(password=self.password)
        while not self.is_valid_password:
            self.password = self.increment_character(password=self.password)
        return self.password

    @property
    def is_valid_password(self) -> bool:
        return not self.has_banned_chars() or self.has_increasing_straight() or self.has_multiple_pairs()

    def has_banned_chars(self) -> bool:
        return bool(set(self.password) & PasswordGenerator.BANNED_CHARS)

    def has_increasing_straight(self) -> bool:
        return any(
            ord(self.password[i]) + 2 == ord(self.password[i + 1]) + 1 == ord(self.password[i + 2])
            for i in range(len(self.password) - 2)
        )

    def has_multiple_pairs(self) -> bool:
        pairs = set()
        for char_a, char_b in pairwise(self.password):
            if char_a == char_b:
                pairs.add(char_a)
                if len(pairs) == 2:
                    return True
        return False

    @staticmethod
    def increment_character(password: str) -> str:
        if password[-1] == "z":
            return f"{PasswordGenerator.increment_character(password[:-1])}a"
        return password[:-1] + chr(ord(password[-1]) + 1)


pg = PasswordGenerator(password=old_password)
print(f"PART ONE: {pg.increment_password()}")
print(f"PART TWO: {pg.increment_password()}")
