from typing import *
from utils import count

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

    # ---------------- BASIC CSP ----------------

    def assign(self, var: Variable, val: Any, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var: Variable, val: Any, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def infer_assignment(self) -> Assignment:
        """Return the partial assignment implied by the current inferences."""
        return {v: self.domains[v][0]
                for v in self.variables if 1 == len(self.domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.domains[B].append(b)

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        removals = [(var, a) for a in self.domains[var] if a != value]
        self.domains[var] = [value]
        return removals

    # ---------------- INFERENCE ----------------

    def revise(self, Xi: Variable, Xj: Variable) -> bool:
        revised = False
        for x in self.domains[Xi][:]:
            sat_vars = [y for y in self.domains[Xj] if self.constraints(Xi, x, Xj, y)]
            if not sat_vars:
                print('[+] PRUNED ')
                self.domains[Xi].remove(x)
                revised = True
        return revised

    def AC3(self, queue=None):
        q: Set[Tuple[Variable, Variable]] = {(Xi, Xk) for Xi in self.variables for Xk in
                                             self.neighbors[Xi]} if queue is None else queue
        while len(q) != 0:
            (Xi, Xj) = q.pop()
            if self.revise(Xi, Xj):
                if not self.domains[Xi]:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        q.add((Xk, Xi))
