"""
testing
"""
from pkg.pysat import solver
solver.logger.setLevel('DEBUG')
clause = frozenset([-1, 2, 3])
assign = {
    1: 1,
    2: 0,
    3: -1
}
s = solver.Solver('../test/sample.cnf')
s.assigns = assign
assert s.compute_value(-1) == 0
assert s.compute_value(1) == 1
assert s.compute_value(2) == 0
assert s.compute_value(-2) == 1
assert s.compute_value(3) == -1

assert not s.is_unit_clause(frozenset([1, 2]))[0]
assert s.is_unit_clause(frozenset([-1, 3]))[0]
assert not s.is_unit_clause(frozenset([-1, 2]))[0]
assert not s.is_unit_clause(frozenset([-2, 3]))[0]

s1 = solver.Solver('../test/test1.cnf')
s1.assigns = {
    1: 0,
    2: -1,
    3: -1,
    4: 0,
}
assert not s1.are_all_variables_assigned()
s1.unit_propagate()
assert s1.are_all_variables_assigned()

s2 = solver.Solver('../test/test2.cnf')
s2.run()
assert s2.compute_cnf() == 1

s3 = solver.Solver('../test/test3.cnf')
s3.run()
assert s3.compute_cnf() == 1

s4 = solver.Solver('../test/test4.cnf')
s4.run()
assert s4.compute_cnf() == 1

s5 = solver.Solver('../test/test5.cnf')
s5.run()
assert s5.compute_cnf() == 1
