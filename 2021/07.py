from math import inf

crab_locations = list(map(int, open("07.txt").read().split(",")))


def calculate_ideal_horizontal_at_flat_cost(locations: list[int]) -> int:
    ideal_horizontal = inf
    for i in range(max(locations)):
        if (movement_cost := sum(abs(location - i) for location in locations)) < ideal_horizontal:
            ideal_horizontal = movement_cost
    return ideal_horizontal


def calculate_ideal_horizontal_at_incrementing_cost(locations: list[int]) -> int:
    ideal_horizontal = inf
    for i in range(max(locations)):
        if (movement_cost := sum(sum(range(abs(location - i) + 1)) for location in locations)) < ideal_horizontal:
            ideal_horizontal = movement_cost
    return ideal_horizontal


print("PART ONE: ", calculate_ideal_horizontal_at_flat_cost(crab_locations))
print("PART TWO: ", calculate_ideal_horizontal_at_incrementing_cost(crab_locations))
