from collections import Counter
from itertools import count

data_start, data_overrides = open("14.txt").read().split("\n\n")
char_counter = Counter(data_start)
data_start = [data_start[i] + data_start[i + 1] for i in range(len(data_start) - 1)]
data_start = Counter(data_start)
data_overrides = {row.split(" -> ")[0]: row.split(" -> ")[1] for row in data_overrides.split("\n")}
data_overrides: dict[str, list[str, str]] = {k: [k[0] + v, v + k[1]] for k, v in data_overrides.items()}


def map_override(counter: Counter) -> Counter:
    counter_copy = counter.copy()
    for key, value in counter.items():
        if value > 0:
            for override in data_overrides[key]:
                counter_copy[override] = counter_copy.get(override, 0) + value
            counter_copy[key] = counter_copy[key] - value
            char_counter[data_overrides[key][0][1]] = char_counter.get(data_overrides[key][0][1], 0) + value
    return counter_copy


working_counter = data_start
for step in count(start=1):
    working_counter = map_override(counter=working_counter)
    if step == 10:
        print("PART ONE: ", char_counter.most_common()[0][1] - char_counter.most_common()[-1][1])
    if step == 40:
        print("PART ONE: ", char_counter.most_common()[0][1] - char_counter.most_common()[-1][1])
        break
