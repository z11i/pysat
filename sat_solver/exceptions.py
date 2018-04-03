"""
Defines exceptions used by the SAT Solver
"""


class FileFormatError(Exception):
    """ Raised when file format is not in DIMACS CNF format """
    pass
