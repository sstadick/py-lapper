from py_lapper import Interval, Lapper, Cursor
import random
from typing import Sequence


def make_random(
    n: int, range_max: int, max_length_power: int
) -> Sequence[Interval[int]]:
    size_max = 10 ** max_length_power
    size_min = int(size_max / 3)
    result = []
    for i in range(0, n):
        start = random.randint(0, range_max)
        end = start + random.randint(size_min, size_max)
        result.append(Interval(start, end, 0))
    return result


def main():
    ivs = make_random(200_000, 50_000_000, 3)
    ivs_sorted = sorted(ivs, key=lambda x: x.start)
    lapper = Lapper(ivs)
    print("Lapper find:")
    total = 0
    for iv in ivs:
        found = sum(1 for f in lapper.find(iv.start, iv.stop))
        total += found
    print(total)
    print("Lapper seek")
    total = 0
    cursor = Cursor(0)
    for iv in lapper.intervals:
        total += sum(1 for f in lapper.seek(iv.start, iv.stop, cursor))
    print(total)


if __name__ == "__main__":
    main()

