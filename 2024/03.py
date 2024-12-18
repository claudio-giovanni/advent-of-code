import re

data = open("03.txt").read().replace("\n", "")


def sum_valid_mul_instructions(instruction: str) -> int:
    valid_instructions = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", instruction)
    return sum(int(a) * int(b) for a, b in valid_instructions)


total_valid_instructions = sum_valid_mul_instructions(instruction=data)

do_instructions = re.findall(r"do\(\)(.*?)don't\(\)", f"do(){data}don't()")
do_instructions = "".join(do_instructions)
total_do_instructions = sum_valid_mul_instructions(instruction=do_instructions)


print(f"PART ONE: {total_valid_instructions}")
print(f"PART TWO: {total_do_instructions}")
