import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''
EXPECTED = 8


def compute(s: str) -> int:
    cubes_max = {
        'red'  : 12,
        'green': 13,
        'blue' : 14,
    }

    ok_games_ids = []

    lines = s.splitlines()
    for line in lines:
        game_s, rest = line.split(': ')
        game_id = int(re.findall(r'\d+', game_s)[0])

        reds = map(int, re.findall(r'(\d+) red', rest))
        greens = map(int, re.findall(r'(\d+) green', rest))
        blues = map(int, re.findall(r'(\d+) blue', rest))

        if all((
                max(reds) <= cubes_max['red'],
                max(greens) <= cubes_max['green'],
                max(blues) <= cubes_max['blue'],
        )):
            ok_games_ids.append(game_id)

    return sum(ok_games_ids)


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
