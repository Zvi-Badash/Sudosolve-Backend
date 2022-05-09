import random

from sudoku_logic.generating.DifficultyLevel import DifficultyLevel
from sudoku_logic.solving.Sudoku import Sudoku

givens = {
    DifficultyLevel.EASY: 35,
    DifficultyLevel.MEDIUM: 30,
    DifficultyLevel.HARD: 25,
    DifficultyLevel.INSANE: 15,
}


def _get_initially_filled() -> str:
    generated = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    mutations = list('123456789')
    for _ in range(1, 10):
        # choose random index to change
        ind = random.randint(0, len(generated) - 1)

        # swap out the char at index with a random mutation
        generated = generated[:ind] + random.choice(mutations) + generated[ind + 1:]

    # If the generated puzzle is valid, return it
    # Otherwise, repeat
    puzzle = Sudoku(generated)
    if puzzle.backtracking_search() is None:
        return _get_initially_filled()
    return generated


def get_sudoku(level: DifficultyLevel = DifficultyLevel.INSANE) -> str:
    initial = Sudoku(_get_initially_filled())
    initial.backtracking_search()

    solved = initial.assignment_to_str()
    removed = set()
    for _ in range(0, len(solved) - givens[level]):
        # choose random index to remove
        ind = random.randint(0, len(solved) - 1)
        while ind in removed:
            ind = random.randint(0, len(solved) - 1)

        removed.add(ind)

        # remove digit from said position
        solved = solved[:ind] + '0' + solved[ind + 1:]
    return solved


def demo():
    puzzle = Sudoku(get_sudoku(level=DifficultyLevel('s')))
    puzzle.display()
    print(puzzle.assignment_to_str().count('.'))
