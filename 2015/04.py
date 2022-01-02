from itertools import count
import hashlib

data = open("04.txt").read()


class Miner:
    def __init__(self, key: str):
        self.key = key

    def find_low_hash(self, zero_count: int) -> int:
        for i in count(start=1):
            h = hashlib.md5(f"{self.key}{i}".encode()).hexdigest()
            if h.startswith("0" * zero_count):
                return i


miner = Miner(key=data)
print(f"PART ONE: {miner.find_low_hash(zero_count=5)}")
print(f"PART TWO: {miner.find_low_hash(zero_count=6)}")
