data = open("03.txt").read()


class Slay:
    def __init__(self):
        self.location = (0, 0)
        self.delivered = [self.location]

    def move(self, direction: str):
        if direction == ">":
            self.location = self.location[0], self.location[1] + 1
        elif direction == "<":
            self.location = self.location[0], self.location[1] - 1
        elif direction == "v":
            self.location = self.location[0] - 1, self.location[1]
        elif direction == "^":
            self.location = self.location[0] + 1, self.location[1]
        self.delivered.append(self.location)

    def get_unique_deliveries(self) -> set:
        return set(self.delivered)


s = Slay()
for datum in data:
    s.move(direction=datum)

print(f"PART ONE: {len(s.get_unique_deliveries())}")

santa_slay, robot_slay = Slay(), Slay()
for i, datum in enumerate(data):
    if i % 2:
        robot_slay.move(direction=datum)
    else:
        santa_slay.move(direction=datum)
unique_houses_delivered = set(santa_slay.delivered + robot_slay.delivered)

print(f"PART TWO: {len(unique_houses_delivered)}")
