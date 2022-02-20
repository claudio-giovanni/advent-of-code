from itertools import groupby, chain

data = open("10.txt").readline()


class Sequence:
    def __init__(self, numbers: str):
        self.numbers = numbers

    def look_and_say(self):
        new_numbers = [(str(len(list(glob))), number) for number, glob in groupby(self.numbers)]
        self.numbers = "".join(chain.from_iterable(new_numbers))


sequence = Sequence(numbers=data)

for _ in range(40):
    sequence.look_and_say()

print(f"PART ONE: {len(sequence.numbers)}")

for _ in range(10):
    sequence.look_and_say()

print(f"PART TWO: {len(sequence.numbers)}")
