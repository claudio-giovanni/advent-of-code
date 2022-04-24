data = open("03.txt").read().splitlines()
data_length = len(data)
data_width = len(data[0])
data_rate_keys = [2**key for key in reversed(range(data_width))]


def get_rate_map(binaries: [str]) -> {int, int}:
    rate_map = {key: 0 for key in data_rate_keys}
    for binary in binaries:
        decimal = int(binary, base=2)
        for key in data_rate_keys:
            if decimal >= key:
                decimal -= key
                rate_map[key] += 1
    return rate_map


data_rate_map = get_rate_map(data)
data_rate_binary = [value > (data_length / 2) for value in data_rate_map.values()]
gamma_rate = int("".join(str(int(number)) for number in data_rate_binary), base=2)
epsilon_rate = int("".join(str(int(not number)) for number in data_rate_binary), base=2)
power_consumption = gamma_rate * epsilon_rate

print("PART ONE: ", power_consumption)


def filter_numbers_by_bit(binaries: [str], index: int, value: int) -> [str]:
    return [binary for binary in binaries if int(binary[index]) == value]


def get_oxygen_rating(binaries: [str]):
    for i, key in enumerate(data_rate_keys):
        key_rate = get_rate_map(binaries)[key]
        oxygen_data_length = len(binaries)
        if key_rate == oxygen_data_length / 2:
            binaries = filter_numbers_by_bit(binaries=binaries, index=i, value=1)
        else:
            binaries = filter_numbers_by_bit(binaries=binaries, index=i, value=key_rate > oxygen_data_length / 2)
    return int(binaries[0], base=2)


def get_co2_scrubber_rating(binaries: [str]):
    for i, key in enumerate(data_rate_keys):
        key_rate = get_rate_map(binaries)[key]
        oxygen_data_length = len(binaries)
        if key_rate == oxygen_data_length / 2:
            binaries = filter_numbers_by_bit(binaries=binaries, index=i, value=0)
        else:
            result = filter_numbers_by_bit(binaries=binaries, index=i, value=key_rate < oxygen_data_length / 2)
            if len(result) <= 1:
                break
            binaries = result
    return int(binaries[0], base=2)


oxygen_rating = get_oxygen_rating(data)
co2_scrubber_rating = get_co2_scrubber_rating(data)

print("PART TWO: ", oxygen_rating * co2_scrubber_rating)
