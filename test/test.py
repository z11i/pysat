"""
testing
"""
from pkg.pysat import solver
solver.logger.setLevel('DEBUG')

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
