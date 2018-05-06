"""
SAT solver using CDCL
"""

import argparse
import os
from pkg.pysat import solver
from pkg.pysat import branch_heuristics as solvers


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads a file and try to determine satisfiability by CDCL.'
        ' Example usage: python3 -m pkg.main test/sample.cnf'
    )
    parser.add_argument(
        'filename',
        type=str,
        nargs='?',
        help='path of .cnf file')
    parser.add_argument(
        'heuristics',
        type=str,
        nargs='?',
        default='RandomChoiceSolver',
        help='choose heuristics to branch variable: RandomChoiceSolver (default) | FrequentVarsFirstSolver')
    parser.add_argument(
        '--loglevel',
        default='WARNING',
        nargs='?',
        help='level of logging (WARNING, DEBUG, etc.)')

    args = parser.parse_args()

    if args.filename is None:
        parser.print_help()
        exit()

    solver.logger.setLevel(args.loglevel)
    solver = getattr(solvers, args.heuristics)(args.filename)
    _, _, answer = solver.run()
    print(answer)
