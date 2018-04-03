"""
testing
"""
from sat_solver import sat_solver
clause = frozenset([-1, 2, 3])
assign = {
    1: 1,
    2: 0
}
sat_solver.logger.setLevel('FINE')
s = sat_solver.Solver()
s.assigns = assign
assert s.compute_value(-1) == 0
assert s.compute_value(1) == 1
assert s.compute_value(2) == 0
assert s.compute_value(-2) == 1
assert s.compute_value(3) == -1
assert s.compute_value(45) == -1

assert not s.is_unit_clause(frozenset([1, 2]))[0]
assert s.is_unit_clause(frozenset([-1, 3]))[0]
assert not s.is_unit_clause(frozenset([-1, 2]))[0]
assert not s.is_unit_clause(frozenset([-2, 3]))[0]

print(s.unit_propagate())
"""

s1 = sat_solver.Solver('../test/test1.cnf')
s1.assignments = {
    1: 0,
    4: 0
}
s1.unit_propagate()
