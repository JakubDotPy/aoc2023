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
EXPECTED = 405


def find_symetry_index(lines: list[str]) -> int:
    for idx, (left, right) in enumerate(itertools.pairwise(lines), start=1):
        if left != right:
            continue
        # possible symetry, fan out and compare
        right_part = lines[idx:]
        left_part = lines[:idx]
        if all(
            left_cand == right_cand
            for left_cand, right_cand in zip(reversed(left_part), right_part)
        ):
            return idx
    return 0


def compute(s: str) -> int:

    total = 0

    for batch in s.split('\n\n'):
        rows = batch.splitlines()
        cols = list(zip(*rows))

        column_idx = find_symetry_index(cols)
        row_idx = find_symetry_index(rows)

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
