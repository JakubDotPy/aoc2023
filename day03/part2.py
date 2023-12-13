import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
EXPECTED = 467835


def coords_around(pxs, pys, pxe, pye):
    """generate coords around the number"""
    coords = []
    coords.extend((c, pys - 1) for c in range(pxs - 1, pxe + 1))  # top
    coords.extend((c, pys + 1) for c in range(pxs - 1, pxe + 1))  # bottom
    coords.extend([(pxs - 1, pys), (pxe, pys)])  # l r
    return coords


symb_ids = itertools.count()
part_ids = itertools.count()


def compute(s: str) -> int:
    parts = {}
    symbols = {}

    # find everything
    lines = s.splitlines()
    for y, line in enumerate(lines):

        # numbers
        for m in re.finditer(r'\d+', line):
            parts[next(part_ids), m.group(0)] = coords_around(m.start(), y, m.end(), y)

        # symbols
        for ms in re.finditer(r'[^\d\.]', line):
            symbols[next(symb_ids), ms.group(0)] = (ms.start(), y)

    ratios = []

    for (sym_id, s), coord in symbols.items():
        if s != '*':
            continue

        gears = []

        for (part_id, part_n), bound in parts.items():
            if coord in bound:
                gears.append(int(part_n))

        if len(gears) == 2:
            ratios.append(gears[0] * gears[1])

    return sum(ratios)


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
