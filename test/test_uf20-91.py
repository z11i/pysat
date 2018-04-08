import os
from pkg.pysat import solver
solver.logger.setLevel('INFO')

directory = os.path.abspath('uf20-91')
for file in os.listdir(directory):
    filename = os.path.abspath(os.path.join(directory, file))
    solv = solver.Solver(filename)
    is_sat, _ = solv.run()
    assert is_sat
