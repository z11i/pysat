"""
SAT solver using CDCL
"""

import argparse
from pkg.pysat import solver


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads a file and try to determine satisfiability by CDCL.'
    )
    parser.add_argument(
        'filename',
        type=str,
        default='test/sample.cnf',
        nargs='?',
        help='path of .cnf file')
    parser.add_argument(
        '--loglevel',
        default='INFO',
        nargs='?',
        help='level of logging (WARNING, DEBUG, etc.)')

    args = parser.parse_args()

    solver.logger.setLevel(args.loglevel)
    solver = solver.Solver(filename=args.filename)
    sat, time = solver.run()