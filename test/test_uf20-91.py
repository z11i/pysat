import os
from sat_solver import sat_solver
sat_solver.logger.setLevel('INFO')

directory = os.path.abspath('uf20-91')
for file in os.listdir(directory):
    filename = os.path.abspath(os.path.join(directory, file))
    solver = sat_solver.Solver(filename)
    solver.run()
