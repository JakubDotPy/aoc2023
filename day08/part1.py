import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''
EXPECTED = 6


def compute(s: str) -> int:
    directions, nodes_paragraph = s.split('\n\n')

    directions = itertools.cycle(directions)

    nodes = {}
    for line in nodes_paragraph.splitlines():
        name, left, right = re.findall(r'(\w+)', line)
        nodes[name] = (left, right)

    name = 'AAA'
    for step_num, direction in enumerate(directions, start=1):
        L, R = nodes[name]
        name = L if direction == 'L' else R
        if name == 'ZZZ':
            return step_num

    raise RuntimeError('not possible state')


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
