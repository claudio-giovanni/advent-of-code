from __future__ import annotations

import contextlib

data = open("04.txt").read().splitlines()


class Crossword:
    def __init__(self, string: list[str]):
        self.rows = data

    def get_all_x_chunks(self) -> list[str]:
        """GARBAGE SOLUTION FOR A GARBAGE PROBLEM"""
        chunks = []
        for row_index, row in enumerate(self.rows):
            for column_index, letter in enumerate(row):
                if letter != "X":
                    continue
                chunks.append(row[column_index : column_index + 4])  # horizontal_forward
                if column_index >= 3:
                    chunks.append(row[column_index - 3 : column_index + 1])  # horizontal_backward
                with contextlib.suppress(IndexError):  # vertical_down
                    chunks.append("".join([self.rows[row_index + i][column_index] for i in range(4)]))
                with contextlib.suppress(IndexError):  # vertical_up
                    if row_index >= 3:
                        chunks.append("".join([self.rows[row_index - i][column_index] for i in range(4)]))
                with contextlib.suppress(IndexError):  # diag_down_right
                    chunks.append("".join([self.rows[row_index + i][column_index + i] for i in range(4)]))
                with contextlib.suppress(IndexError):  # diag_down_left
                    if column_index >= 3:
                        chunks.append("".join([self.rows[row_index + i][column_index - i] for i in range(4)]))
                with contextlib.suppress(IndexError):  # diag_up_right
                    if row_index >= 3:
                        chunks.append("".join([self.rows[row_index - i][column_index + i] for i in range(4)]))
                with contextlib.suppress(IndexError):  # diag_up_left
                    if row_index >= 3 and column_index >= 3:
                        chunks.append("".join([self.rows[row_index - i][column_index - i] for i in range(4)]))
        return chunks

    def get_all_a_chunks(self) -> list[set]:
        """GARBAGE PROBLEM PART 2, GARBAGE SOLUTION PART 2"""
        chunks = []
        for row_index, row in enumerate(self.rows):
            for column_index, letter in enumerate(row):
                if column_index < 1 or row_index < 1:
                    continue
                if letter != "A":
                    continue
                with contextlib.suppress(IndexError):
                    forward_slash = "".join([self.rows[row_index + i][column_index + i] for i in range(-1, 2)])
                    back_slash = "".join([self.rows[row_index + i][column_index - i] for i in range(-1, 2)])
                    chunks.append({forward_slash, back_slash})
        return chunks


crossword = Crossword(string=data)
x_chunks = crossword.get_all_x_chunks()
total_xmas_chunks = sum(1 for chunk in x_chunks if chunk == "XMAS" or (chunk == "SAMX"))

a_chunks = crossword.get_all_a_chunks()
total_x_mas_chunks = sum(1 for chunk in a_chunks if chunk.issubset({"MAS", "SAM"}))


print(f"PART ONE: {total_xmas_chunks}")
print(f"PART TWO: {total_x_mas_chunks}")
