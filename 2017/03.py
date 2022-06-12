from itertools import count

data = int(open("03.txt").read().splitlines()[0])


class SpiralGrid:
    @staticmethod
    def get_offset(offset_value: int):
        for odd_square in count(1, 2):
            if (upper_bound := odd_square**2) < offset_value:
                continue
            lower_bound = (odd_square - 2) ** 2
            perimeter = upper_bound - lower_bound
            perimeter_slice = perimeter // 4
            location = (offset_value - lower_bound) % perimeter_slice
            location_offset = abs(location - perimeter_slice // 2)
            min_value = odd_square // 2
            return min_value + location_offset


print(f"PART ONE: {SpiralGrid.get_offset(offset_value=289326)}")
print(f"PART TWO: {None}")
