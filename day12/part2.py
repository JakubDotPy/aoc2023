import argparse
import functools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
EXPECTED = 525152


@functools.cache
def line_combinations(line: str, nums: tuple[int]):
    if not nums:
        return 0 if "#" in line else 1
    if not line:
        return 1 if not nums else 0

    possibilities = 0

    first_char = line[0]

    if first_char == '.':
        # point at start is pointless
        possibilities += line_combinations(line[1:], nums)

    if first_char == '?':
        possibilities += line_combinations('.' + line[1:], nums)
        possibilities += line_combinations('#' + line[1:], nums)

    if first_char == '#':
        # check the length of leading hashes
        if (
                nums[0] <= len(line)
                and "." not in line[:nums[0]]
                and (nums[0] == len(line) or line[nums[0]] != "#")
        ):
            possibilities += line_combinations(line[nums[0] + 1:], nums[1:])

    return possibilities


def compute(s: str) -> int:
    total_possibilities = 0

    for line in s.splitlines():
        spring_str, nums = line.split()
        spring_str = '?'.join([spring_str] * 5)
        nums = eval(nums)  # converts to a tuple of ints
        nums = nums * 5
        line_possibilities = line_combinations(spring_str, nums)
        total_possibilities += line_possibilities

    return total_possibilities


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
