import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 136


def slide(grid: support.Grid, direction: support.Direction4):
    # assign direction
    for pointer in grid.pointers:
        pointer.direction = direction

    # choose the correct order
    sorting_fns = {
        support.Direction4.UP   : lambda p: p.y,
        support.Direction4.RIGHT: lambda p: -p.x,
        support.Direction4.DOWN : lambda p: -p.y,
        support.Direction4.LEFT : lambda p: p.x,
    }
    grid.pointers.sort(key=sorting_fns[direction])

    for pointer in grid.pointers:
        # look above, if it is empty, move there
        while True:
            try:
                val_in_dir = pointer.look(direction)
                if val_in_dir == '.':
                    grid[pointer.coords] = '.'  # free the space
                    pointer.move()
                else:
                    break
            except support.OutOfBounds:
                break
        # done moving update grid value
        grid[pointer.coords] = 'O'


def strain_on_north(grid: support.Grid) -> int:
    return sum(
        grid.height + 1 - pointer.y
        for pointer in grid.pointers
    )


def compute(s: str) -> int:
    grid = support.Grid.from_string(s)
    for coord, val in grid.items():
        if val == 'O':
            grid.add_pointer(support.Pointer(*coord))

    slide(grid, support.Direction4.UP)

    north_strain = strain_on_north(grid)

    return north_strain


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
