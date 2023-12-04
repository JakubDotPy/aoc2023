from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''
EXPECTED = 30


@dataclass
class Card:
    _id: int
    winning_nums: set[int]
    given_nums: set[int]

    @classmethod
    def from_str(cls, s) -> Card:
        card, rest = s.split(':')
        card_id = int(card.split()[1])
        win_nums_s, play_nums_s = rest.split('|')
        winning_nums = set(map(int, win_nums_s.split()))
        given_nums = set(map(int, play_nums_s.split()))
        return cls(card_id, winning_nums, given_nums)

    @property
    def won_nums(self):
        return self.winning_nums.intersection(self.given_nums)

    @property
    def score(self) -> int:
        return 2 ** (len(self.won_nums) - 1) if self.won_nums else 0

    @property
    def next_ids(self):
        start = self._id + 1
        end = start + len(self.won_nums)
        return range(start, end)

    def __hash__(self):
        return self._id

    def __repr__(self):
        return f'Card({self._id})'


def compute(s: str) -> int:
    id_to_c = {}

    for line in s.splitlines():
        card = Card.from_str(line)
        id_to_c[card._id] = (card, 1)

    for c_id, (card, cnt) in id_to_c.items():
        for next_id in card.next_ids:
            c, n = id_to_c[next_id]
            id_to_c[next_id] = c, n + cnt

    return sum(count for card, count in id_to_c.values())


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

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
