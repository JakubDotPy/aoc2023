import argparse
import itertools
import math
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''
EXPECTED = 6


def get_path_len(name, directions, nodes):
    for step_num, direction in enumerate(directions, start=1):
        L, R = nodes[name]
        name = L if direction == 'L' else R
        if name.endswith('Z'):
            return step_num


def compute(s: str) -> int:
    directions, nodes_paragraph = s.split('\n\n')

    directions = itertools.cycle(directions)

    nodes = {}
    for line in nodes_paragraph.splitlines():
        name, left, right = re.findall(r'(\w+)', line)
        nodes[name] = (left, right)

    names = {name for name in nodes if name.endswith('A')}
    path_lens = tuple(get_path_len(name, directions, nodes) for name in names)
    return math.lcm(*path_lens)


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
