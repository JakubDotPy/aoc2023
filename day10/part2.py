import argparse
import itertools
import os.path

import pytest
import shapely

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
'''
EXPECTED = 4
INPUT_S_1 = '''\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
'''
EXPECTED_1 = 8

possible_moves = {
    'F': (support.Direction4.RIGHT, support.Direction4.DOWN),
    '7': (support.Direction4.DOWN, support.Direction4.LEFT),
    'J': (support.Direction4.LEFT, support.Direction4.UP),
    'L': (support.Direction4.UP, support.Direction4.RIGHT),
    '-': (support.Direction4.RIGHT, support.Direction4.LEFT),
    '|': (support.Direction4.UP, support.Direction4.DOWN),
}


def starting_conditions(grid, start_coords):
    candidates = set(possible_moves.keys())

    options = {
        '.LJ-': 'LJ|',
        '.|FL': 'FL-',
        '.F7-': 'F7|',
        '.|7J': '7J-'
    }

    for coord, (look, remove) in zip(
            support.Pointer.adjacent_4(*start_coords),
            options.items()
    ):
        if grid.get(coord, '.') in look:
            candidates -= set(remove)

    start_symbol = candidates.pop()
    start_dir = possible_moves[start_symbol][0]

    return start_symbol, start_dir


def get_new_dir(pointer):
    return next(
        dir for dir in possible_moves[pointer.value]
        if dir != pointer.direction.opposite
    )


def compute(s: str) -> int:
    grid = support.Grid.from_string(s)
    start_coords = next(c for c, val in grid.items() if val == 'S')
    start_symbol, start_dir = starting_conditions(grid, start_coords)
    grid[start_coords] = start_symbol

    pointer = support.Pointer(*start_coords, direction=start_dir)
    grid.add_pointer(pointer)

    path = [start_coords]

    for step in itertools.count(start=1):
        pointer.move()
        new_dir = get_new_dir(pointer)
        pointer.direction = new_dir

        path.append(pointer.coords)  # fill the path

        if pointer.coords == start_coords:
            break

    path_geometry = shapely.Polygon(path)
    path = set(path)
    num_inside = sum(
        shapely.contains_xy(path_geometry, *coord)
        for coord in grid
        if coord not in path
    )

    return num_inside


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
            (INPUT_S_1, EXPECTED_1),
    ),
    ids=('small', 'medium')
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
