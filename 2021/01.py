numbers = open("01.txt").read().splitlines()
numbers = [int(number) for number in numbers]


def count_increases(data: list[int]) -> int:
    return sum(data[i + 1] > data[i] for i in range(len(data) - 1))


part_one = count_increases(numbers)
print("PART ONE: ", part_one)

three_window_numbers = []
for i in range(len(numbers) - 2):
    three_window_numbers.append(sum((numbers[i], numbers[i + 1], numbers[i + 2])))

part_two = count_increases(three_window_numbers)

print("PART TWO: ", part_two)
