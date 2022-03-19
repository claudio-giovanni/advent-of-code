import re
from dataclasses import dataclass


@dataclass
class Reindeer:
    name: str
    speed: int
    stamina: int
    rest: int
    points: int = 0
    position: int = 0

    def get_distance_traveled(self, seconds: int) -> int:
        complete_laps = seconds // (self.stamina + self.rest)
        remaining_seconds = seconds % (self.stamina + self.rest)
        remaining_seconds = min([remaining_seconds, self.stamina])
        self.position = (complete_laps * self.speed * self.stamina) + (remaining_seconds * self.speed)
        return self.position


def calculate_place_points(coral: list[Reindeer], seconds: int) -> int:
    for second in range(1, seconds + 1):
        max_position = max(reindeer.get_distance_traveled(second) for reindeer in coral)
        for reindeer in coral:
            if reindeer.position == max_position:
                reindeer.points += 1
    return max(reindeer.points for reindeer in coral)


data = open("14.txt").readlines()
reindeer_coral: [Reindeer] = []
for datum in data:
    name = datum.split()[0]
    speed, stamina, rest = re.findall(r"\d+", datum)
    reindeer_coral.append(Reindeer(name=name, speed=int(speed), stamina=int(stamina), rest=int(rest)))

fastest_reindeer_time = max([reindeer.get_distance_traveled(seconds=2503) for reindeer in reindeer_coral])

print(f"PART ONE: {fastest_reindeer_time}")
print(f"PART TWO: {calculate_place_points(coral=reindeer_coral, seconds=2503)}")
