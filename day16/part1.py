import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
# @formatter:off
INPUT_S = \
r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''
# @formatter:on
EXPECTED = 46

deflectors = {
    '\\': {
        support.Direction4.DOWN : support.Direction4.RIGHT,
        support.Direction4.LEFT : support.Direction4.UP,
        support.Direction4.RIGHT: support.Direction4.DOWN,
        support.Direction4.UP   : support.Direction4.LEFT,
    },
    '/' : {
        support.Direction4.DOWN : support.Direction4.LEFT,
        support.Direction4.LEFT : support.Direction4.DOWN,
        support.Direction4.RIGHT: support.Direction4.UP,
        support.Direction4.UP   : support.Direction4.RIGHT,
    }
}


def compute(s: str) -> int:
    grid = support.Grid.from_string(s)
    grid.energized = collections.Counter()
    grid.add_pointers(support.Pointer(0, 0, support.Direction4.RIGHT))

    visited = set()

    while grid.pointers:

        # actual pointer
        pointer = grid.pointers.pop()

        new_pointers = {pointer, }
        value = pointer.value

        # hit deflector
        if value in deflectors:
            # change direction
            pointer.direction = deflectors[value][pointer.direction]

        horizontal = pointer.direction in (support.Direction4.LEFT, support.Direction4.RIGHT)
        vertical = pointer.direction in (support.Direction4.UP, support.Direction4.DOWN)

        # splitter hit, spawn two new and delete this one
        if horizontal and value == '|':
            new_pointers.update({
                support.Pointer(*pointer.coords, direction=support.Direction4.UP),
                support.Pointer(*pointer.coords, direction=support.Direction4.DOWN),
            })
            new_pointers.remove(pointer)
        elif vertical and value == '-':
            new_pointers.update({
                support.Pointer(*pointer.coords, direction=support.Direction4.LEFT),
                support.Pointer(*pointer.coords, direction=support.Direction4.RIGHT),
            })
            new_pointers.remove(pointer)

        for pointer in new_pointers:
            phash = pointer.coords + pointer.direction.value
            if phash not in visited and pointer.coords in grid:
                visited.add(phash)
                grid.energized[pointer.coords] += 1
                grid.add_pointers(pointer)
                pointer.move()

    return len(grid.energized)


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
