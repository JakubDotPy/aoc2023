import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''
EXPAND_1 = 9
EXPECTED_1 = 1030
EXPAND_2 = 99
EXPECTED_2 = 8410


def compute(s: str, expand: int) -> int:
    empty_rows = set()
    empty_cols = set()
    galaxies = set()

    for y, line in enumerate(s.splitlines()):
        if '#' not in line:
            empty_rows.add(y)
        for x, char in enumerate(line):
            if char == '#':
                galaxies.add((x, y))

    for x, col in enumerate(zip(*s.splitlines())):
        if '#' not in col:
            empty_cols.add(x)

    dx = dy = expand
    total_distance = 0
    for (ax, ay), (bx, by) in itertools.combinations(galaxies, 2):
        ax, bx = sorted((ax, bx))
        ay, by = sorted((ay, by))
        num_extend_x = len(empty_cols.intersection(set(range(ax, bx))))
        num_extend_y = len(empty_rows.intersection(set(range(ay, by))))
        len_x = bx - ax + num_extend_x * dx
        len_y = by - ay + num_extend_y * dy
        total_distance += (len_x + len_y)

    return total_distance


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expand', 'expected'),
    (
            (INPUT_S, EXPAND_1, EXPECTED_1),
            (INPUT_S, EXPAND_2, EXPECTED_2),
    ),
)
def test(input_s: str, expand: int, expected: int) -> None:
    assert compute(input_s, expand) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 999_999))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
