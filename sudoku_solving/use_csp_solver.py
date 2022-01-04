from aima import Sudoku, easy1

e = Sudoku(easy1)
e.display(e.infer_assignment())
print(e.curr_domains)
