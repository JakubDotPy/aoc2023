import argparse
import math
import os.path
import re
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''
EXPECTED = 145


@dataclass
class Lens:
    text: str
    label: str = field(init=False)
    operation: str = field(init=False)
    focal_length: int | None = field(init=False, default=None)

    def __hash__(self):
        val = 0
        for c in self.label:
            val += ord(c)
            val *= 17
            val %= 256
        return val

    def __post_init__(self):
        match re.split(r'(\W)', self.text):
            case [label, '=', focal_length]:
                self.operation = '='
                self.focal_length = int(focal_length)
            case [label, '-', '']:
                self.operation = '-'
            case _:
                raise ValueError('cannot parse Lens')
        self.label = label

    def __str__(self):
        return f'Lens({self.text})'

    __repr__ = __str__


class Boxes(defaultdict):

    def process(self, lens):
        h = hash(lens)

        def remove(lens):
            keep = lambda l: l.label != lens.label
            self[h] = list(filter(keep, self[h]))
            if not self[h]:
                self.pop(h)

        def insert(lens):
            current_lenses = self[h]
            if any(l.label == lens.label for l in current_lenses):
                # replace
                for i, l in enumerate(current_lenses):
                    if l.label == lens.label:
                        current_lenses[i] = lens
                        break
            else:
                # append
                current_lenses.append(lens)

        actions = {
            '-': remove,
            '=': insert,
        }
        return actions[lens.operation](lens)


def compute(s: str) -> int:
    boxes = Boxes(list)
    lenses = (Lens(lens_str) for lens_str in s.strip().split(','))

    for lens in lenses:
        boxes.process(lens)

    total = 0
    for box_n, lenses in boxes.items():
        for lens_index, lens in enumerate(lenses):
            total += math.prod((
                box_n + 1,
                lens_index + 1,
                lens.focal_length,
            ))

    return total


@pytest.mark.solved
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
