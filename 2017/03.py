from itertools import count

data = int(open("03.txt").read().splitlines()[0])


def get_offset_straight_spiral(offset_value: int):
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


# Father, forgive them, for they know not what they do
def get_offset_proximity_spiral(offset_value: int):
    spiral = [1, 1, 2, 4, 5, 10, 11, 23, 25]
    previous_perimeter = 8
    filler_counter = 6
    post_counter = 8
    counter = 8

    for odd in range(5, 16, 2):
        perimeter = odd * 4 - 4
        before_corner_counter = 1
        corner_counter = 2
        for step in range(1, perimeter + 1):
            counter += 1
            side_length = perimeter // 4
            # index = previous_perimeter + step
            index = counter
            minus_perimeter = index - previous_perimeter
            if step == 1:  # breakout
                spiral.append(spiral[index - 1] + spiral[minus_perimeter])
                filler_counter += 2
            elif step == 2 or (index % side_length) == 1:  # post-breakout & post-corner
                spiral.append(
                    spiral[index - 1]
                    + spiral[index - 2]
                    + spiral[index - post_counter]
                    + spiral[index - post_counter - 1]
                )
                post_counter += 2
            # before_corner but not final corner & last_corner
            elif ((index % side_length) == (side_length - 1) and step != perimeter - 1) or step == perimeter:
                spiral.append(
                    spiral[index - 1]
                    + spiral[index - previous_perimeter - before_corner_counter]
                    + spiral[index - previous_perimeter - (before_corner_counter + 1)]
                )
                before_corner_counter += 2
            elif (index % side_length) == 0:  # corner
                spiral.append(spiral[index - 1] + spiral[minus_perimeter - corner_counter])
                corner_counter += 2
                filler_counter += 2
            else:  # filler
                spiral.append(
                    spiral[index - 1]
                    + spiral[index - filler_counter]
                    + spiral[index - filler_counter - 1]
                    + spiral[index - filler_counter - 2]
                )
            if spiral[-1] > offset_value:
                return spiral[-1]
        previous_perimeter = perimeter


print(f"PART ONE: {get_offset_straight_spiral(offset_value=289326)}")
print(f"PART TWO: {get_offset_proximity_spiral(offset_value=289326)}")
