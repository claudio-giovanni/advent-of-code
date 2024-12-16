from collections import Counter

data = open("01.txt").read().splitlines()

data = [list(map(int, datum.split())) for datum in data]


list_one, list_two = map(list, zip(*data))  # noqa
list_one.sort(), list_two.sort()
list_diff = sum(abs(item_one - item_two) for item_one, item_two in zip(list_one, list_two))

list_two_counter = Counter(list_two)
similarity_score = sum(list_two_counter.get(item_one, 0) * item_one for item_one in list_one)


print(f"PART ONE: {list_diff}")
print(f"PART TWO: {similarity_score}")
