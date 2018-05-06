import operator
import random
from pkg.pysat.solver import Solver
from pkg.utils.constants import UNASSIGN


class RandomChoiceSolver(Solver):
    def pick_branching_variable(self):
        """
        Picks an unassigned variable randomly
        :return: int
        """
        return random.choice(list(self.all_unassigned_vars()))


class FrequentVarsFirstSolver(Solver):
    def preprocess(self):
        vs = {x: 0 for x in self.vars}
        for clause in self.cnf:
            for v in clause:
                vs[abs(v)] += 1
        self.vars_order_frequency = [
            t[0] for t in
            sorted(vs.items(), key=operator.itemgetter(1), reverse=True)]

    def pick_branching_variable(self):
        return next(filter(lambda v: self.assigns[v] == UNASSIGN, self.vars_order_frequency))
