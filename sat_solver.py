"""
SAT solver using CDCL
"""

import argparse
import logging
import sys


class FileFomratError(Exception):
    """ Raised when file format is not in DIMACS CNF format """
    pass

def unit_propagate(clauses, assignment):
    pass

def read_file(fname):
    """
    Reads a DIMACS CNF format file, returns clauses (set of frozensets) and literals (set of int).
        :param fname: the file name
        :raises FileFormatError: when file format is wrong
        :returns: (clauses, literals)
    """
    with open(fname) as f:
        lines = [
            line.strip().split(' ') for line in f.readlines()
            if not line.startswith('c') and line != '\n'
        ]

    if lines[0][:2] == ['p', 'cnf']:
        count_literals, count_clauses = map(int, lines[0][-2:])
    else:
        raise FileFomratError('Number of literals and clauses are not declared properly.')

    lits = set()
    clss = set()

    for line in lines[1:]:
        if line[-1] != '0':
            raise FileFomratError('Each line of clauses must end with 0.')
        clause = frozenset(map(int, line[:-1]))
        lits.update(map(abs, clause))
        clss.add(clause)

    if len(lits) != count_literals or len(clss) != count_clauses:
        raise FileFomratError('Unmatched literal count or clause count.')

    logger.debug('clauses: %s', clauses)
    logger.debug('literals: %s', literals)

    return clss, lits

def set_logger(level):
    """ Sets the module logger """
    l = logging.getLogger(__name__)
    l.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(funcName)s][%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    l.addHandler(handler)
    return l

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Reads a file and try to determine satisfiability by CDCL.'
    )
    parser.add_argument(
        'filepath',
        type=str,
        default='test/sample.cnf',
        nargs='?',
        help='path of .cnf file')
    parser.add_argument(
        '--loglevel',
        default='WARNING',
        nargs='?',
        help='level of logging (WARNING, DEBUG, etc.)')
    args = parser.parse_args()
    logger = set_logger(getattr(logging, args.loglevel))

    clauses, literals = read_file(args.filepath)
