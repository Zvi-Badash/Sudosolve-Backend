from typing import *
from utils import count, argmin_random_tie

Variable = Union[str, int]
Domain = Dict[Variable, List]
Neighbors = Dict[Variable, List]
Assignment = Dict[Variable, Any]


class CSP:
    def __init__(self, variables: List[Variable], domains: Union[None, Domain],
                 neighbors: Union[None, Neighbors], constraints: Callable):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.nassigns = 0

    # ---------------- BASIC CSP ----------------

    def assign(self, var: Variable, val: Any, assignment) -> None:
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment) -> None:
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var: Variable, val: Any, assignment) -> int:
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def infer_assignment(self) -> Assignment:
        """Return the partial assignment implied by the current inferences."""
        return {v: self.domains[v][0]
                for v in self.variables if 1 == len(self.domains[v])}

    def restore(self, removals) -> None:
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.domains[B].append(b)

    def suppose(self, var, value) -> List[Tuple[Variable, Any]]:
        """Start accumulating inferences from assuming var=value."""
        removals = [(var, a) for a in self.domains[var] if a != value]
        self.domains[var] = [value]
        return removals

    # ---------------- INFERENCE ----------------

    def revise(self, Xi: Variable, Xj: Variable, removals: List) -> bool:
        revised = False
        for x in self.domains[Xi][:]:
            sat_vars = [y for y in self.domains[Xj] if self.constraints(Xi, x, Xj, y)]
            if not sat_vars:
                self.domains[Xi].remove(x)
                removals.append((Xi, x))
                revised = True
        return revised

    def AC3(self, removals, var: Variable = None) -> bool:
        q: Set[Tuple[Variable, Variable]] = {(Xi, Xk) for Xi in self.variables for Xk in self.neighbors[Xi]} \
            if var is None else {(X, var) for X in \
                                 self.neighbors[var]}

        while len(q) != 0:
            (Xi, Xj) = q.pop()
            if self.revise(Xi, Xj, removals):
                if not self.domains[Xi]:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        q.add((Xk, Xi))
        return True

    # ------------------- ORDERING -------------------

    def num_legal_values(self, var, assignment) -> int:
        if self.domains:
            return len(self.domains[var])
        else:
            return count(self.nconflicts(var, val, assignment) == 0 for val in self.domains[var])

    def lcv(self, var, assignment) -> Any:
        """Least-constraining-values heuristic."""
        return sorted(self.domains[var], key=lambda val: self.nconflicts(var, val, assignment))

    def mrv(self, assignment) -> Variable:
        """Minimum-remaining-values heuristic."""
        return argmin_random_tie([v for v in self.variables if v not in assignment],
                                 key=lambda var: self.num_legal_values(var, assignment))

    # ------------------- SEARCH -------------------
    def backtracking_search(self) -> Assignment:
        """[Figure 6.5]"""

        def backtrack(assignment):
            if len(assignment) == len(self.variables):
                return assignment
            var = self.mrv(assignment)
            for value in self.lcv(var, assignment):
                if 0 == self.nconflicts(var, value, assignment):
                    self.assign(var, value, assignment)
                    removals = self.suppose(var, value)
                    if self.AC3(var=var, removals=removals):
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                    self.restore(removals)
            self.unassign(var, assignment)
            return None

        return backtrack({})
