import argparse
import os.path
from dataclasses import dataclass

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 35


@dataclass(frozen=True)
class Range:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length

    @property
    def _print_end(self) -> int:
        """end when used in range"""
        return self.end - 1

    def __repr__(self):
        return f'{self.__class__.__name__}({self.start}, {self._print_end})'


@dataclass(frozen=True, repr=False)
class Source(Range):
    pass


@dataclass(frozen=True, repr=False)
class Destination(Range):
    pass


@dataclass
class Mapping:
    source: Source
    dest: Destination

    def map_(self, num: int) -> int:
        delta = num - self.source.start
        mapped = self.dest.start + delta
        return mapped

    def can_map(self, num):
        return self.source.start <= num < self.source.end


@dataclass
class Conversion:
    from_: str
    to_: str
    mappings: list[Mapping]

    @classmethod
    def from_paragraph(cls, paragraph):
        from_ = to_ = ''
        mappings = []
        for line in paragraph.splitlines():
            match line.split():
                case [from_to, "map:"]:
                    from_, _, to_ = from_to.split('-')
                case [*numbers]:
                    dest_start, source_start, length = list(map(int, numbers))
                    mappings.append(
                        Mapping(
                            Source(source_start, length),
                            Destination(dest_start, length)
                        )
                    )
                case _:
                    # raise ValueError('unknown line')
                    print('unknown line')
        return cls(from_, to_, mappings)

    def do_mapping(self, num):
        for mapping in self.mappings:
            if mapping.can_map(num):
                return mapping.map_(num)
        return num

    def process(self, nums: list[int]) -> list[int]:
        return [self.do_mapping(num) for num in nums]


def compute(s: str) -> int:
    seeds_line, *mapping_paragraphs = s.split('\n\n')

    seeds = list(map(int, seeds_line.split()[1:]))

    conversion = [
        Conversion.from_paragraph(mapping_paragraph)
        for mapping_paragraph in mapping_paragraphs
    ]

    nums = seeds
    for conversion in conversion:
        nums = conversion.process(nums)

    return min(nums)


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
