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
EXPECTED = 4361


def coords_around(pxs, pys, pxe, pye):
    """generate coords around the number"""
    coords = set()
    coords.update((c, pys - 1) for c in range(pxs - 1, pxe + 1))  # top
    coords.update((c, pys + 1) for c in range(pxs - 1, pxe + 1))  # bottom
    coords.update({(pxs - 1, pys), (pxe, pys)})  # l r
    return coords


part_ids = itertools.count()


def compute(s: str) -> int:
    parts = {}
    symbols = set()

    # find everything
    lines = s.splitlines()
    for y, line in enumerate(lines):

        # numbers
        for m in re.finditer(r'\d+', line):
            parts[next(part_ids), m.group(0)] = coords_around(m.start(), y, m.end(), y)

        # symbols
        for ms in re.finditer(r'[^\d\.]', line):
            symbols.add((ms.start(), y))

    ok_parts = []
    for (part_id, part_n), bound in parts.items():
        if bound.intersection(symbols):
            ok_parts.append(int(part_n))

    return sum(ok_parts)


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
