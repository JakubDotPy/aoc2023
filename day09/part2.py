import argparse
import os.path
from itertools import pairwise

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 2


def diffs(seq):
    return tuple(b - a for a, b in pairwise(seq))


def make_sequences(sequence):
    sequences = []
    while not all(d == 0 for d in sequence):
        sequences.append(sequence)
        sequence = diffs(sequence)
    return sequences


def get_prev(sequences):
    add = 0
    for sequence in sequences[::-1]:
        add = sequence[0] - add
    return add


def compute(s: str) -> int:
    lines = s.splitlines()
    to_sum = []

    for line in lines:
        nums = tuple(map(int, line.split()))
        sequences = make_sequences(nums)
        to_sum.append(get_prev(sequences))

    return sum(to_sum)


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
