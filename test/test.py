"""
testing
"""
from sat_solver import sat_solver
clause = frozenset([-1, 2, 3])
assign = {
    1: 1,
    2: 0
}
sat_solver.logger.setLevel('FINER')
s = sat_solver.Solver()
assert s.compute_value(-1, assign) == 0
assert s.compute_value(1, assign) == 1
assert s.compute_value(2, assign) == 0
assert s.compute_value(-2, assign) == 1
assert s.compute_value(3, assign) == -1
assert s.compute_value(45, assign) == -1

cl1 = frozenset([1, 2])
assert not s.is_unit_clause(cl1, assign)
