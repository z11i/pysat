import os
from pkg.pysat import solver, branch_heuristics as solvers

solver.logger.setLevel('WARNING')


def test(solver_name):
    expected_count = 0
    actual_sat_count = 0
    actual_unsat_count = 0

    time = 0
    count = -1  # -1: maximum number of tests; n for first n tests

    directory = os.path.abspath('uf20-91')
    dirs = os.listdir(directory)
    try:
        dirs[:] = dirs[:count]
    except IndexError:
        pass
    for file in dirs:
        filename = os.path.abspath(os.path.join(directory, file))
        solv = getattr(solvers, solver_name)(filename)
        is_sat, t, answer = solv.run()
        time += t
        if is_sat:
            actual_sat_count += 1
        else:
            actual_unsat_count += 1
        expected_count += 1

    print(f'{solver_name}\t Average time used: {time / expected_count:.3f} s')


print('Starting benchmarking...')
test('Solver')
test('FrequentVarsFirstSolver')
test('RandomChoiceSolver')
test('DynamicLargestIndividualSumSolver')
