from __future__ import annotations

import re
from dataclasses import dataclass

data = open("02.txt").read().splitlines()


@dataclass
class CubeRoll:
    red: int
    green: int
    blue: int

    def __ge__(self, other):
        return self.red >= other.red and self.green >= other.green and self.blue >= other.blue

    @staticmethod
    def from_string(string: str) -> CubeRoll:
        cubes = re.findall(r"(\d+)\s(blue|red|green)", string)
        cubes_map = {color: int(amount) for amount, color in cubes}
        red, green, blue = cubes_map.get("red", 0), cubes_map.get("green", 0), cubes_map.get("blue", 0)
        return CubeRoll(red=red, green=green, blue=blue)


def game_is_playable(start: CubeRoll, roll: CubeRoll) -> bool:
    return start >= roll


def get_game_power(game: list[CubeRoll]) -> int:
    minimum_roll = CubeRoll(
        red=max(roll.red for roll in game),
        green=max(roll.green for roll in game),
        blue=max(roll.blue for roll in game),
    )
    return minimum_roll.red * minimum_roll.green * minimum_roll.blue


if __name__ == "__main__":
    starting_cube = CubeRoll(red=12, green=13, blue=14)
    games: list[list[CubeRoll]] = []
    for datum in data:
        game = [CubeRoll.from_string(string=string) for string in datum.split(";")]
        games.append(game)

    playable_id_totals = 0
    for _id, game in enumerate(games, start=1):
        is_playable = all((game_is_playable(start=starting_cube, roll=roll) for roll in game))
        if is_playable:
            playable_id_totals += _id
    print(f"PART ONE: {playable_id_totals}")

    game_power_totals = 0
    for game in games:
        game_power = get_game_power(game=game)
        game_power_totals += game_power
    print(f"PART TWO: {game_power_totals}")
