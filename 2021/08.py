data = [data.strip().split(" | ") for data in open("08.txt").read().splitlines()]
data_input: list[list[str]] = [key[0].split() for key in data]
data_outputs: list[list[str]] = [value[1].split() for value in data]

output_segments = [segment for segment_group in data_outputs for segment in segment_group]
unique_segment_lengths = [2, 3, 4, 7]
unique_segment_count = sum(len(segment) in unique_segment_lengths for segment in output_segments)

print("PART ONE: ", unique_segment_count)


class DisplaySegment:
    def __init__(self, input_data: list[str], output_data: list[str]):
        self.input_data = input_data
        self.output_data = output_data
        self.character_map: dict[int, str] = self._map_unique_char_segments()
        self.character_map.update(self._map_common_char_segments())

    def _map_unique_char_segments(self) -> dict[int, str]:
        """Segment map for numbers with unique lengths (1, 4, 7, 8)"""
        character_map = {}
        for chars in self.input_data:
            if len(chars) == 2:
                character_map[1] = chars
            elif len(chars) == 4:
                character_map[4] = chars
            elif len(chars) == 3:
                character_map[7] = chars
            elif len(chars) == 7:
                character_map[8] = chars
        return character_map

    def _map_common_char_segments(self) -> dict[int, str]:
        """Segment map for numbers with shared lengths (6, 0, 9, 3, 2, 5)"""
        character_map = self.character_map
        for chars in self.input_data:
            if len(chars) == 6:
                if not set(character_map[1]).issubset(chars):
                    character_map[6] = chars
                elif not set(character_map[4]).issubset(chars):
                    character_map[0] = chars
                else:
                    character_map[9] = chars
            if len(chars) == 5:
                if set(character_map[1]).issubset(chars):
                    character_map[3] = chars
                elif len(set(character_map[4] + chars)) == 7:
                    character_map[2] = chars
                else:
                    character_map[5] = chars
        return character_map

    def decode_output(self) -> str:
        output = []
        for chars in self.output_data:
            output += [str(key) for key, value in self.character_map.items() if set(value) == set(chars)]
        return "".join(output)


data_grids = [DisplaySegment(input_data=ins, output_data=outs) for ins, outs in zip(data_input, data_outputs)]
decoded_outputs = sum([int(grid.decode_output()) for grid in data_grids])

print("PART TWO: ", decoded_outputs)
