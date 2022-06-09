from dataclasses import dataclass

data = list(map(int, (open("01.txt").read().strip())))


@dataclass
class Captcha:
    numbers: list[int]

    def __post_init__(self):
        self.width = len(self.numbers)

    def get_paired_values(self, pair_distance: int) -> list[int]:
        values = []
        for i, number in enumerate(self.numbers):
            pair_index = (i + pair_distance) % self.width
            if number == self.numbers[pair_index]:
                values.append(number)
        return values


captcha = Captcha(numbers=data)
paired_values = captcha.get_paired_values(pair_distance=1)
print(f"PART ONE: {sum(paired_values)}")
paired_values = captcha.get_paired_values(pair_distance=captcha.width // 2)
print(f"PART TWO: {sum(paired_values)}")
