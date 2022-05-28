from itertools import count
from math import sqrt

data = int(open("20.txt").readline())


def get_house_by_target_gift_count(target_gift_count: int) -> int:
    for house_id in count(1):
        factors = []
        for i in range(1, int(sqrt(house_id)) + 1):
            if house_id % i == 0:
                factors.append(i)
                factors.append(house_id / i)
        if sum(factors) * 10 >= target_gift_count:
            return house_id


print(get_house_by_target_gift_count(target_gift_count=data))
