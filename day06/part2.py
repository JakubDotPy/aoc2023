import argparse
import math
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 71503


def compute(s: str) -> int:
    n = re.findall(r'\d+', s)
    times = [int(''.join(n[:len(n) // 2]))]
    dists = [int(''.join(n[len(n) // 2:]))]

    ok_ways = []
    for t, d in zip(times, dists):
        tot_ways = 0
        for c in range(t):
            run = t - c
            dist = run * c
            if dist > d:
                tot_ways += 1
        ok_ways.append(tot_ways)

    return math.prod(ok_ways)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
