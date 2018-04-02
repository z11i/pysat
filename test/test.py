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
assert s.compute_value(-1, assign) == 0
assert s.compute_value(1, assign) == 1
assert s.compute_value(2, assign) == 0
assert s.compute_value(-2, assign) == 1
assert s.compute_value(3, assign) == -1
assert s.compute_value(45, assign) == -1

assert not s.is_unit_clause(frozenset([1, 2]), assign)[0]
assert s.is_unit_clause(frozenset([-1, 3]), assign)[0]
assert not s.is_unit_clause(frozenset([-1, 2]), assign)[0]
assert not s.is_unit_clause(frozenset([-2, 3]), assign)[0]
