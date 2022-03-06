import json

data = open("12.txt").readline()


class NumberParser:
    def __init__(self, storage_blob: str):
        self.number_map = json.loads(storage_blob)
        self.sum = 0

    def parse_number_sum(self, number_map: int | list | dict | str):
        map_type = type(number_map)
        if map_type == int:
            self.sum += number_map
        elif map_type == list:
            for nested_object in number_map:
                self.parse_number_sum(number_map=nested_object)
        elif map_type == dict:
            for nested_object in number_map.values():
                self.parse_number_sum(number_map=nested_object)


class NumberParserV2(NumberParser):
    def parse_number_sum(self, number_map: int | list | dict | str):
        if type(number_map) == dict and "red" in number_map.values():
            return
        else:
            super().parse_number_sum(number_map=number_map)


n = NumberParser(storage_blob=data)
n.parse_number_sum(number_map=n.number_map)
print(f"PART ONE: {n.sum}")

n2 = NumberParserV2(storage_blob=data)
n2.parse_number_sum(number_map=n.number_map)
print(f"PART TWO: {n2.sum}")
