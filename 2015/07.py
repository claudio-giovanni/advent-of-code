from typing import Union
from functools import lru_cache

data = open("07.txt").readlines()


class Circuit:
    def __init__(self, signals: list[str]):
        self.MAX_VALUE = 65535
        self.signal_map = {split[1]: split[0] for signal in signals if (split := signal.strip().split(" -> "))}

    @lru_cache(maxsize=None)
    def get_signal_value(self, signal_name: str) -> Union[int, str]:
        if signal_name.isnumeric():
            return int(signal_name)

        desired_signal: str = self.signal_map[signal_name]
        if " AND " in desired_signal:
            a, b = desired_signal.split(" AND ")
            return self.get_signal_value(a) & self.get_signal_value(b)
        elif " OR " in desired_signal:
            a, b = desired_signal.split(" OR ")
            return self.get_signal_value(a) | self.get_signal_value(b)
        elif " LSHIFT " in desired_signal:
            a, b = desired_signal.split(" LSHIFT ")
            return self.get_signal_value(a) << self.get_signal_value(b)
        elif " RSHIFT " in desired_signal:
            a, b = desired_signal.split(" RSHIFT ")
            return self.get_signal_value(a) >> self.get_signal_value(b)
        elif "NOT " in desired_signal:
            a = desired_signal[4::]
            return self.MAX_VALUE - self.get_signal_value(a)
        else:
            return self.get_signal_value(desired_signal)


c = Circuit(signals=data)
print(f"PART ONE: {(part_one := c.get_signal_value('a'))}")

c2 = Circuit(signals=data)
c2.signal_map["b"] = str(part_one)
print(f"PART TWO: {c2.get_signal_value('a')}")
