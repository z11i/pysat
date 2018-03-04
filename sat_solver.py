"""
SAT solver using CDCL
"""

import sys

class FileFomratError(Exception):
    """ Raised when file format is not in DIMACS CNF format """
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
    return clss, lits

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = 'test/sample.cnf'

    clauses, literals = read_file(filename)
