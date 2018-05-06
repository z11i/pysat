import os
from pkg.pysat import solver
solver.logger.setLevel('WARNING')

expected_count = 0
actual_sat_count = 0
actual_unsat_count = 0

time = 0
count = -1  # -1: maximum number of tests; n for first n tests

directory = os.path.abspath('uuf50-218')
dirs = os.listdir(directory)
try:
    dirs[:] = dirs[:count]
except IndexError:
    pass
for file in dirs:
    filename = os.path.abspath(os.path.join(directory, file))
    solv = solver.Solver(filename)
    is_sat, t, answer = solv.run()
    print(answer)
    time += t
    if is_sat:
        actual_sat_count += 1
    else:
        actual_unsat_count += 1
    expected_count += 1

print(f'Correct results: {actual_unsat_count}/{expected_count}')
print(f'False positive: {actual_sat_count}')
print(f'Average time used: {time / expected_count:.2f} s')
