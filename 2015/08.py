import re

data = open("08.txt").readlines()
data = [line.strip() for line in data]


class Line:
    def __init__(self, chars: str):
        self.chars = chars

    @property
    def literal_value(self) -> str:
        return self.chars.strip()

    @property
    def memory_value(self) -> str:
        temp = self.chars[1:-1]
        temp = temp.replace("\\\\", "/")
        temp = temp.replace('\\"', '"')
        temp = re.sub(r"\\x..", "$", temp)
        return temp

    @staticmethod
    def to_literal(chars: str):
        temp = chars.replace("\\", "\\\\")
        temp = temp.replace('"', '\\"')
        return f'"{temp}"'


if __name__ == "__main__":
    part_one = sum(len(l.literal_value) - len(l.memory_value) for datum in data if (l := Line(datum)))
    print(f"PART ONE: {part_one}")

    part_two = sum(len(l.to_literal(l.literal_value)) - len(l.literal_value) for datum in data if (l := Line(datum)))
    print(f"PART TWO: {part_two}")
