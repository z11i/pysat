"""
SAT solver using CDCL
"""
import pprint
import time
from pkg.utils.constants import TRUE, FALSE, UNASSIGN
from pkg.utils.exceptions import FileFormatError
from pkg.utils.logger import set_logger

logger = set_logger()


class Solver:

    def __init__(self, filename):
        logger.info('========= create pysat from %s =========', filename)
        self.filename = filename
        self.cnf, self.vars = Solver.read_file(filename)
        self.assigns = dict.fromkeys(list(self.vars), UNASSIGN)
        self.nodes = dict((k, ImplicationNode(k, UNASSIGN)) for k in list(self.vars))
        self.branching_vars = set()

    def run(self):
        start_time = time.time()
        sat = self.solve()
        spent = time.time() - start_time
        logger.info('Equation is {}, resolved in {:.2f} s'
                    .format('SAT' if sat else 'UNSAT', spent))
        return sat, spent

    def solve(self):
        """
        Returns TRUE if SAT, False if UNSAT
        :return: whether there is a solution
        """
        # if self.unit_propagate():
        #     return False
        dec_lvl = 0  # decision level
        bt_var = None  # backtrack variable
        bt_val = None  # backtrack value
        while not self.are_all_variables_assigned():
            logger.debug('--------decision level: %s ---------', dec_lvl)
            var, val = self.pick_branching_variable(dec_lvl, bt_var, bt_val)
            bt_var = bt_val = None  # reset branching variable we don't keep assigning it
            logger.debug('picking %s to be %s', var, val)
            dec_lvl += 1
            self.assigns[var] = val
            conf_var, conf_cls = self.unit_propagate(var, dec_lvl)
            if conf_var:
                logger.fine(self.nodes)
                lvl = self.conflict_analyze(conf_var, conf_cls, dec_lvl - 1)
                logger.debug('level reset to %s', lvl)
                if lvl < 0:
                    return False
                bt_var, bt_val = self.backtrack(lvl)
                dec_lvl = lvl
        return True

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
                line.strip().split() for line in f.readlines()
                if (not (line.startswith('c') or
                         line.startswith('%') or
                         line.startswith('0'))
                    and line != '\n')
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

        if len(literals) != count_literals or len(lines) - 1 != count_clauses:
            raise FileFormatError(
                'Unmatched literal count or clause count.'
                ' Literals expected: {}, actual: {}.'
                ' Clauses expected: {}, actual: {}.'
                    .format(count_literals, len(literals), count_clauses, len(clauses)))

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
        value = self.assigns[abs(literal)]
        value = value if value == UNASSIGN else value ^ (literal < 0)
        logger.finest('value: %s', value)
        return value

    def compute_clause(self, clause):
        values = list(map(self.compute_value, clause))
        value = UNASSIGN if UNASSIGN in values else max(values)
        logger.finest('clause: %s, value: %s', clause, value)
        return value

    def compute_cnf(self):
        logger.fine('cnf: %s', self.cnf)
        logger.fine('assignments: %s', self.assigns)
        return min(map(self.compute_clause, self.cnf))

    def is_unit_clause(self, clause):
        """
        Checks if clause is a unit clause. If and only if there is
        exactly 1 literal unassigned, and all the other literals having
        value of 0.
            :param clause: set of ints
            :returns: (is_clause_a_unit, the_literal_to_assign, the clause)
        """
        logger.finest('clause: %s', clause)
        values = []
        unassigned = None

        for literal in clause:
            value = self.compute_value(literal)
            logger.finest('value of %s: %s', literal, value)
            values.append(value)
            unassigned = literal if value == UNASSIGN else unassigned

        check = (values.count(FALSE) == len(clause) - 1 and
                 values.count(UNASSIGN) == 1)
        logger.finest('%s: %s', clause, (check, unassigned))
        logger.finest('assignments: %s', self.assigns)
        return check, unassigned, clause

    def update_graph(self, var, val, clause=None, level=-1):
        node = self.nodes[var]
        node.value = val
        node.level = level

        # update parents
        if clause:  # clause is None, meaning this is branching, no parents to update
            for v in [abs(lit) for lit in clause if abs(lit) != var]:
                node.parents.append(self.nodes[v])
                self.nodes[v].children.append(node)
            node.clause = clause
            logger.fine('node %s has parents: %s', var, node.parents)

    def unit_propagate(self, var=None, level=0):
        """
        A unit clause has all of its literals but 1 assigned to 0. Then, the sole
        unassigned literal must be assigned to value 1. Unit propagation is the
        process of iteratively applying the unit clause rule.
        :return: None if no conflict is detected, else return the literal
        """
        # check for unsatisfied clauses
        if var:
            unsats = list(filter(lambda c: self.compute_clause(c) == 0, self.cnf))
            if unsats:
                logger.debug('unsatisfied clause detected: %s when %s is assigned %s',
                             unsats[0], var, self.assigns[var])
                return var, unsats[0]

        # check for unit clauses to implicate new assignments
        unit_clauses = self.get_unit_clauses()

        for _, lit, clause in unit_clauses:
            var = abs(lit)
            value = TRUE if lit > 0 else FALSE
            self.update_graph(var, value, clause, level)
            if self.assigns[var] ^ value == 1:  # one of the values is 1, another is 0
                logger.fine('parents of %s: %s', var, self.nodes[var].parents)
                logger.debug('conflict detected for %s', lit)
                return lit
            self.assigns[var] = value
            logger.debug('propagated %s to be %s, because %s', var, value, self.nodes[var].clause)
            conf_var, conf_cls = self.unit_propagate(var, level)
            if conf_var:
                return conf_var, conf_cls
            logger.finer('assignments: %s', self.assigns)

        return None, None

    def get_unit_clauses(self):
        return list(filter(lambda x: x[0], map(self.is_unit_clause, self.cnf)))

    def are_all_variables_assigned(self):
        all_assigned = all(var in self.assigns for var in self.vars)
        none_unassigned = not any(var for var in self.vars if self.assigns[var] == UNASSIGN)
        return all_assigned and none_unassigned

    def pick_branching_variable(self, level, bt_var=None, bt_val=None):
        """
        Pick a variable to assign a value.
        :return: variable, value assigned
        """
        if bt_var is not None and bt_val is not None:
            var = bt_var
            val = bt_val
        else:
            var = next(filter(
                lambda v: v in self.assigns and self.assigns[v] == UNASSIGN,
                self.vars))
            val = TRUE
        self.branching_vars.add(var)
        self.update_graph(var, val, level=level)
        return var, val

    def conflict_analyze(self, conf_var, conf_cls, curr_level):
        """
        Analyze the most recent conflict and learn a new clause from the conflict.
        - Find the cut in the implication graph that led to the conflict
        - Derive a new clause which is the negation of the assignments that led to the conflict

        Returns a decision level to be backtracked to.
        :param conf_var: (int) the variable that has conflicts
        :param conf_cls: (set of int) the clause that introduces the conflict
        :param curr_level: (int) current decision level
        :return: decision level int
        """
        logger.fine('conflict clause: %s', conf_cls)
        logger.fine('existing clause: %s', self.nodes[conf_var].clause)

        learnt = conf_cls.union(self.nodes[conf_var].clause)
        learnt = frozenset([x for x in learnt if abs(x) != abs(conf_var)])
        self.cnf.add(learnt)
        logger.debug('learnt: %s', learnt)
        parents_conflict = set()
        for literal in conf_cls:
            if abs(literal) == abs(conf_var):
                continue
            parents_conflict.add(abs(literal))
            parents_conflict.update(
                [x.variable for x in self.nodes[abs(literal)].all_parents()
                 if x.variable in self.branching_vars and x.level != curr_level])
        parents_existing = set()
        parents_existing.update(
            [x.variable for x in self.nodes[abs(conf_var)].all_parents()
             if x.variable in self.branching_vars and x.level != curr_level])
        disjunction = parents_existing.intersection(parents_conflict)

        if disjunction:
            level = self.nodes[max(disjunction)].level
        else:
            level = curr_level - 1
        return level

    def backtrack(self, level):
        """
        Non-chronologically backtrack ("back jump") to the appropriate decision level,
        where the first-assigned variable involved in the conflict was assigned
        """
        logger.debug('backtracking to %s', level)
        bt_var = None
        bt_val = None
        for var, node in self.nodes.items():
            if node.level < level:
                node.children[:] = [child for child in node.children if child.level < level]
            else:
                if node.level == level and node.variable in self.branching_vars:
                    # reset level to branching decision, remembers branching variable
                    bt_var = node.variable
                    bt_val = node.value ^ TRUE
                node.value = UNASSIGN
                node.level = -1
                node.parents = []
                node.children = []
                node.clause = None
                self.assigns[node.variable] = UNASSIGN

        self.branching_vars = set([
            var for var in self.vars
            if (self.assigns[var] != UNASSIGN
                and len(self.nodes[var].parents) == 0)
        ])

        logger.finer('after backtracking, graph:\n%s', pprint.pformat(self.nodes))

        return bt_var, bt_val


class ImplicationNode:
    """
    Represents a node in an implication graph. Each node contains
    - its value
    - its implication children (list)
    - parent nodes (list)
    """

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
        self.level = -1
        self.parents = []
        self.children = []
        self.clause = None

    def all_parents(self):
        parents = set(self.parents)
        for parent in self.parents:
            for p in parent.all_parents():
                parents.add(p)
        return list(parents)

    def __str__(self):
        sign = '+' if self.value == TRUE else '-' if self.value == FALSE else '?'
        return "[{}{}:L{}, {}p, {}c]".format(
            sign, self.variable, self.level, len(self.parents), len(self.children))

    def __repr__(self):
        return str(self)
