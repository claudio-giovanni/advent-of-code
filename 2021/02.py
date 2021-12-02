data = open("02.txt").read().splitlines()
data = [command.split() for command in data]

directions = {"forward": 0, "down": 0, "up": 0}
for direction, value in data:
    directions[direction] += int(value)
part_one = directions["forward"] * (directions["up"] - directions["down"])
print("PART ONE: ", part_one)

aim = 0
depth = 0
for direction, value in data:
    value = int(value)
    if direction == "down":
        aim += value
    elif direction == "up":
        aim -= value
    elif direction == "forward":
        depth += aim * value
part_two = depth * directions["forward"]
print("PART TWO: ", part_two)
