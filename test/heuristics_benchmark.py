import os
from pkg.pysat import solver, branch_heuristics as solvers

solver.logger.setLevel('WARNING')


def test(test_suite, solver_name):
    expected_count = 0
    actual_sat_count = 0
    actual_unsat_count = 0

    time = 0
    branches = 0
    count = -1  # -1: maximum number of tests; n for first n tests

    if os.path.abspath('.').endswith('test'):
        directory = os.path.abspath(test_suite)
    else:
        directory = os.path.abspath(os.path.join('test', test_suite))
    dirs = os.listdir(directory)
    try:
        dirs[:] = dirs[:count]
    except IndexError:
        pass
    for file in dirs:
        filename = os.path.abspath(os.path.join(directory, file))
        solv = getattr(solvers, solver_name)(filename)
        is_sat, t, answer = solv.run()
        branches += solv.branching_count
        time += t
        if is_sat:
            actual_sat_count += 1
        else:
            actual_unsat_count += 1
        expected_count += 1

    print(solver_name)
    print('\tAverage time used: {:.3f} s'.format(time / expected_count))
    print('\tAverage branch picked: {:.1f}'.format(branches / expected_count))


def test_suite(suite):
    print('------------------------')
    print('Starting benchmarking with {} ...'.format(suite))
    test(suite, 'OrderedChoiceSolver')
    test(suite, 'RandomChoiceSolver')
    test(suite, 'FrequentVarsFirstSolver')
    test(suite, 'DynamicLargestIndividualSumSolver')


test_suite('uf20-91')
test_suite('uf50-218')
test_suite('uf75-325')
test_suite('uf100-430')
