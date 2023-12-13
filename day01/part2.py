import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281

words = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
w_to_n = {w: str(n) for n, w in enumerate(words, start=1)}

pat = re.compile(fr'(?=(\d|{"|".join(words)}))')


def compute(s: str) -> int:
    total = 0
    for line in s.splitlines():
        # search
        found = pat.findall(line)
        first, last = found[0], found[-1]

        # transform
        first = w_to_n.get(first, first)
        last = w_to_n.get(last, last)

        # add
        total += int(first + last)
    return total


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
