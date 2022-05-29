from itertools import count
from math import inf, sqrt

data = int(open("20.txt").readline())


def get_valid_factors(number: int, factor: int, factor_limit: int) -> set[int]:
    valid_factors = set()
    if number % factor != 0:
        return set()
    factor_pair = number / factor
    if factor_pair <= factor_limit:
        valid_factors.add(factor)
    if factor <= factor_limit:
        valid_factors.add(factor_pair)
    return valid_factors


def get_house_by_target_gift_count(expected_presents: int, gift_multiplier: int, factor_limit: int = inf) -> int:
    for house_id in count(2, 2):
        factors = set()
        potential_factors = range(1, int(sqrt(house_id)) + 1)
        for potential_factor in potential_factors:
            valid_factors = get_valid_factors(number=house_id, factor=potential_factor, factor_limit=factor_limit)
            factors |= valid_factors
        if sum(factors) * gift_multiplier >= expected_presents:
            return house_id


print(f"PART ONE: {get_house_by_target_gift_count(expected_presents=data, gift_multiplier=10)}")
print(f"PART TWO: {get_house_by_target_gift_count(expected_presents=data, gift_multiplier=11, factor_limit=50)}")
