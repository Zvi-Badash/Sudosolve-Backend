import itertools
import re
from functools import reduce

from .CSP import CSP
from .utils import flatten

_R3 = list(range(3))
_CELL = itertools.count().__next__
_BGRID = [[[[_CELL() for x in _R3] for y in _R3] for bx in _R3] for by in _R3]
_BOXES = flatten([list(map(flatten, brow)) for brow in _BGRID])
_ROWS = flatten([list(map(flatten, zip(*brow))) for brow in _BGRID])
_COLS = list(zip(*_ROWS))

_NEIGHBORS = {v: set() for v in flatten(_ROWS)}
for unit in map(set, _BOXES + _ROWS + _COLS):
    for v in unit:
        _NEIGHBORS[v].update(unit - {v})


class Sudoku(CSP):
    rows = _ROWS
    neighbors = _NEIGHBORS
    bgrid = _BGRID

    def __init__(self, grid):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        squares = iter(re.findall(r'\d|\.', grid))
        domains = {var: [ch] if ch in '123456789' else list('123456789')
                   for var, ch in zip(flatten(self.rows), squares)}
        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid)  # Too many squares
        CSP.__init__(self, None, domains, self.neighbors, lambda A, a, B, b: a != b)

    def assignment_to_str(self) -> str:
        def show_box(box):
            return [''.join(map(show_cell, row)) for row in box]

        def show_cell(cell):
            cell = str(self.infer_assignment().get(cell, '.'))
            return cell if len(cell) == 1 else '.'

        def abut(lines1, lines2):
            return list(
                map(''.join, list(zip(lines1, lines2))))

        return ''.join(
            ''.join(reduce(
                abut, map(show_box, brow))) for brow in self.bgrid)

    def display(self) -> None:
        def show_box(box):
            return [' '.join(map(show_cell, row)) for row in box]

        def show_cell(cell):
            cell = str(self.infer_assignment().get(cell, '.'))
            return cell if len(cell) == 1 else '.'

        def abut(lines1, lines2):
            return list(
                map(' | '.join, list(zip(lines1, lines2))))

        print('\n------+-------+------\n'.join(
            '\n'.join(reduce(
                abut, map(show_box, brow))) for brow in self.bgrid))
        print()
