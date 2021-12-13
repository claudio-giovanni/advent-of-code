from collections import namedtuple

data = open("12.txt").read().splitlines()

Step = namedtuple("Step", "start end")

steps_data: set[Step] = set()
for row in data:
    a, b = row.split("-")
    steps_data.update({Step(a, b), Step(b, a)})
    steps_data = {step for step in steps_data if step.start != "end" and step.end != "start"}


class Map:
    def __init__(self, steps: set[Step]):
        self.steps: set[Step] = steps
        self.viable_routes: list[list[Step]] = []
        self._get_viable_routes()

    def _get_viable_routes(self):
        starting_steps: set[Step] = {step for step in self.steps if step.start == "start"}
        for step in starting_steps:
            self._find_end_step(step=step, steps_available={s for s in self.steps if s.start != "start"}, step_trail=[])

    def _find_end_step(self, step: Step, steps_available: set[Step], step_trail: list[Step]) -> None:
        if step.end == "end":
            step_trail.append(step)
            self.viable_routes.append(step_trail)
        elif next_steps := [next_step for next_step in steps_available if next_step.start == step.end]:
            step_trail.append(step)
            if step.end.islower():
                steps_available = {next_step for next_step in steps_available if step.end != next_step.end}
            for next_step in next_steps:
                self._find_end_step(step=next_step, steps_available=steps_available, step_trail=step_trail[::])

    def __repr__(self):
        return f"Map(steps={self.steps})"


m = Map(steps=steps_data)
print("PART ONE: ", len(m.viable_routes))
