import argparse
import os.path
from collections import Counter
from dataclasses import dataclass
from functools import total_ordering
from typing import ClassVar

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 6440


@total_ordering
@dataclass
class Card:
    symbol: str
    value_map: ClassVar[dict[str, int]] = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
    }

    @property
    def rel_strength(self):
        return self.value_map[self.symbol]

    def __eq__(self, other: 'Card'):
        return self.rel_strength == other.rel_strength

    def __lt__(self, other: 'Card'):
        return self.rel_strength < other.rel_strength


@total_ordering
@dataclass
class Hand:
    cards: list[Card]
    hand_patterns: ClassVar[dict[str, set[int]]] = {
        'Five of a kind' : [5],
        'Four of a kind' : [4, 1],
        'Full house'     : [3, 2],
        'Three of a kind': [3, 1, 1],
        'Two pair'       : [2, 2, 1],
        'One pair'       : [2, 1, 1, 1],
        'High card'      : [1, 1, 1, 1, 1]
    }

    @property
    def _cards_str(self):
        return ''.join(c.symbol for c in self.cards)

    @property
    def kind(self) -> str:
        c = Counter(self._cards_str)
        for kind, counts in self.hand_patterns.items():
            if counts == sorted(c.values(), reverse=True):
                return kind
        raise ValueError('unknown hand')

    @property
    def rel_rank(self):
        return list(self.hand_patterns).index(self.kind)

    def __eq__(self, other):
        return self.kind == other.kind

    def __lt__(self, other: 'Hand'):
        """first compare the kind of the hand, then compare the strings"""
        if self.rel_rank == other.rel_rank:
            for my_card, other_card in zip(self.cards, other.cards):
                if my_card.rel_strength == other_card.rel_strength:
                    continue
                return my_card.rel_strength > other_card.rel_strength
        return self.rel_rank < other.rel_rank

    def __str__(self):
        return f'Hand({self._cards_str}, {self.kind})'

    __repr__ = __str__


def compute(s: str) -> int:
    hands = []
    for line in s.splitlines():
        cards_s, bet = line.split()
        hands.append((Hand([Card(s) for s in cards_s]), int(bet)))

    hands.sort(key=lambda t: t[0], reverse=True)

    wins = list(rank * bet for rank, (hand, bet) in enumerate(hands, start=1))

    return sum(wins)


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
