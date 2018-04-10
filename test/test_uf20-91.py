import os
from pkg.pysat import solver
solver.logger.setLevel('INFO')

expected_sat_count = 1000
actual_sat_count = 0
actual_unsat_count = 0

time = 0

directory = os.path.abspath('uf20-91')
dirs = sorted(os.listdir(directory))
for file in dirs:
    filename = os.path.abspath(os.path.join(directory, file))
    solv = solver.Solver(filename)
    is_sat, t = solv.run()
    time += t
    if is_sat:
        actual_sat_count += 1
    else:
        actual_unsat_count += 1

print(f'Correct results: {actual_sat_count}/{expected_sat_count}')
print(f'False negative: {actual_unsat_count}')
print(f'Average time used: {time / expected_sat_count:.2f} s')
