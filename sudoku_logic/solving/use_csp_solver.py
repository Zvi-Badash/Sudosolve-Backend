from time import perf_counter
from sudoku_logic.solving.Sudoku import Sudoku

# print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
# with open('all-sudokus.txt', 'r') as f:
#     times = []
#     for curr_line in f:
#         start = perf_counter()
#         puzzle = Sudoku(curr_line)
#         solved = puzzle.backtracking_search()
#         if solved is not None:
#             elapsed = perf_counter() - start
#             times.append(elapsed / 1000)
#         else:
#             print(f'Couldn\'t solve {curr_line}.')
#
# print(
#     f'''
# Solved {len(times)} Sudokus in {sum(times)} seconds.
# avg. solving time was {sum(times) / len(times)}. (avg. of {len(times) / sum(times)} Hz.)
# max solving time was {max(times)} seconds.
# ''')
#

start = perf_counter()
puzzle = Sudoku('080000000000050900701002060020000080030004000408900600604007010300000000000200007')

puzzle.display()
print(puzzle.assignment_to_str())

puzzle.backtracking_search()
puzzle.display()
print(puzzle.assignment_to_str())

print(puzzle.nassigns)
print(f'solved an easy Sudoku in  {(perf_counter() - start) / 1000} seconds.')

# print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
