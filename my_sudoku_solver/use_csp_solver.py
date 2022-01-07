from time import perf_counter
from datetime import datetime
from my_sudoku_solver.Sudoku import Sudoku

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
with open('all-sudokus.txt', 'r') as f:
    times = []
    for curr_line in f:
        start = perf_counter()
        puzzle = Sudoku(curr_line)
        solved = puzzle.backtracking_search()
        if solved is not None:
            elapsed = perf_counter() - start
            times.append(elapsed / 1000)
        else:
            print(f'Couldn\'t solve {curr_line}.')

print(
    f'''
Solved {len(times)} in {sum(times)} seconds.
avg. solving time was {sum(times) / len(times)}. (avg. of {len(times) / sum(times)} Hz.)
max solving time was {max(times)} seconds.
''')

print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
