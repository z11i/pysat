"""
SAT solver using CDCL
"""
from .constants import DEFAULT_FILE, TRUE, FALSE, UNASSIGN
from .exceptions import FileFormatError, ConflictError
from .logger import set_logger

logger = set_logger()


class Solver:

    def __init__(self, filename=DEFAULT_FILE):
        self.filename = filename
        self.cnf, self.vars = Solver.read_file(filename)
        self.assigns = dict.fromkeys(list(self.vars), UNASSIGN)

    def solve(self):
        """
        Returns TRUE if SAT, False if UNSAT
        :return: whether there is a solution
        """
        if self.unit_propagate():
            return False
        dec_lvl = 0  # decision level
        while not self.are_all_variables_assigned():
            var, val = self.pick_branching_variable()
            dec_lvl += 1
            self.assigns[var] = val
            if self.unit_propagate():
                lvl = self.conflict_analyze()
                if lvl < 0:
                    return False
                self.backtrack(lvl)
                dec_lvl = lvl

    @staticmethod
    def read_file(filename):
        """
        Reads a DIMACS CNF format file, returns clauses (set of frozenset) and
        literals (set of int).
            :param filename: the file name
            :raises FileFormatError: when file format is wrong
            :returns: (clauses, literals)
        """
        with open(filename) as f:
            lines = [
                line.strip().split(' ') for line in f.readlines()
                if not line.startswith('c') and line != '\n'
            ]

        if lines[0][:2] == ['p', 'cnf']:
            count_literals, count_clauses = map(int, lines[0][-2:])
        else:
            raise FileFormatError('Number of literals and clauses are not declared properly.')

        literals = set()
        clauses = set()

        for line in lines[1:]:
            if line[-1] != '0':
                raise FileFormatError('Each line of clauses must end with 0.')
            clause = frozenset(map(int, line[:-1]))
            literals.update(map(abs, clause))
            clauses.add(clause)

        if len(literals) != count_literals or len(clauses) != count_clauses:
            raise FileFormatError('Unmatched literal count or clause count.')

        logger.fine('clauses: %s', clauses)
        logger.fine('literals: %s', literals)

        return clauses, literals

    def compute_value(self, literal):
        """
        Compute the value of the literal (could be -/ve or +/ve) from
        `assignment`. Returns -1 if unassigned
            :param literal: an int, can't be 0
            :returns: value of the literal
        """
        logger.finest('literal: %s', literal)
        logger.finest('assigns: %s', self.assigns)
        if literal == 0:
            raise ValueError('0 is an invalid literal!')

        variable = abs(literal)
        if variable not in self.assigns:
            logger.finest('%s not in assignment', variable)
            return UNASSIGN
        value = self.assigns[variable] ^ (literal < 0)
        logger.finest('value: %s', value)
        return value

    def compute_clause(self, clause):
        logger.finer('clause: %s', clause)
        return max(map(self.compute_value, clause))

    def compute_cnf(self):
        logger.debug('cnf: %s', self.cnf)
        logger.debug('assignments: %s', self.assigns)
        return min(map(self.compute_clause, self.cnf))

    def is_unit_clause(self, clause):
        """
        Checks if clause is a unit clause. If and only if there is
        exactly 1 literal unassigned, and all the other literals having
        value of 0.
            :param clause: set of ints
            :returns: (is_clause_a_unit, the_literal)
        """
        logger.finest('clause: %s', clause)
        values = []
        unassigned = None

        for literal in clause:
            value = self.compute_value(literal)
            values.append(value)
            unassigned = literal if value == UNASSIGN else unassigned

        check = (values.count(FALSE) == len(clause) - 1 and
                 values.count(UNASSIGN) == 1)
        logger.finer('%s: %s', clause, (check, unassigned))
        logger.finest('assignments: %s', self.assigns)
        return check, unassigned

    def assign_unassigned(self, literal):
        """
        Assign the variable such that literal's value is 1
        :param literal:
        :return:
        """

        var = abs(literal)
        value = TRUE if literal > 0 else FALSE
        if self.assigns[var] ^ -value == 1:  # one of the values is 1, another is 0
            raise ConflictError
        self.assigns[var] = value
        logger.finer('assigned %s to %s', var, self.assigns[var])

    def unit_propagate(self):
        """
        A unit clause has all of its literals but 1 assigned to 0. Then, the sole
        unassigned literal must be assigned to value 1. Unit propagation is the
        process of iteratively applying the unit clause rule.
        :return: None if no conflict is detected, else return the literal
        """
        checks = self.get_unit_clauses()
        for _, x in checks:
            try:
                self.assign_unassigned(x)
            except ConflictError:
                logger.fine('conflict detected for %s', x)
                return x
            logger.fine('assigned: %s, assignments: %s', x, self.assigns)
        if self.get_unit_clauses():
            self.unit_propagate()

    def get_unit_clauses(self):
        return list(filter(lambda x: x[0], map(self.is_unit_clause, self.cnf)))

    def are_all_variables_assigned(self):
        all_assigned = all(var in self.assigns for var in self.vars)
        none_unassigned = not any(var for var in self.vars if self.assigns[var] == UNASSIGN)
        return all_assigned and none_unassigned

    def pick_branching_variable(self):
        """
        Pick a variable to assign a value.
        :return: variable, value assigned
        """
        var = next(filter(
            lambda v: v in self.assigns and self.assigns[v] == UNASSIGN,
            self.vars))
        return var, TRUE

    def conflict_analyze(self):
        return 0

    def backtrack(self, level):
        pass
