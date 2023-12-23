import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''
EXPECTED = 400


xor_lines = lambda lines: tuple(a != b for a, b in zip(*lines))


def xor_fold(lines, idx: int):
    right_part = lines[idx:]
    left_part = lines[:idx][::-1]
    return list(map(xor_lines, zip(left_part, right_part)))


def find_fold_index(lines: list[str]) -> int:
    for fold_idx in range(len(lines)):
        fold = xor_fold(lines, fold_idx)
        # if there is only one symbol different, we found it
        checksum = sum(itertools.chain.from_iterable(fold))
        if checksum == 1:
            return fold_idx
    return 0


def compute(s: str) -> int:
    total = 0

    for batch in s.split('\n\n'):
        rows = batch.splitlines()
        cols = list(zip(*rows))

        column_idx = find_fold_index(cols)
        row_idx = find_fold_index(rows)

        total += column_idx + row_idx * 100

    return total


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    print()
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
