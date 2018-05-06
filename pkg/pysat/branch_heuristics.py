import operator
import random

from pkg.pysat.solver import Solver
from pkg.utils.constants import UNASSIGN, TRUE, FALSE


class RandomChoiceSolver(Solver):
    def pick_branching_variable(self):
        """
        Picks an unassigned variable randomly
        :return: int
        """
        return random.choice(list(self.all_unassigned_vars())), \
               random.sample([TRUE, FALSE], 1)[0]


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
        return next(filter(lambda v: self.assigns[v] == UNASSIGN, self.vars_order_frequency)), \
               random.sample([TRUE, FALSE], 1)[0]


class DynamicLargestIndividualSumSolver(Solver):
    """
    for a given variable x:
        C(x,p) = # unresolved clauses in which x appears positively
        C(x,n) = # unresolved clauses in which x appears negatively
    find a variable a such that C(a,p) is max, a variable b such that C(b,n) is max
    if C(a,p) > C(b,n), assign a to TRUE, else assign b to FALSE
    """

    def all_unresolved_clauses(self):
        return filter(lambda c: self.compute_clause(c) == UNASSIGN, self.cnf)

    def pick_branching_variable(self):
        v_pos = {x: 0 for x in self.vars if self.assigns[x] == UNASSIGN}
        v_neg= {x: 0 for x in self.vars if self.assigns[x] == UNASSIGN}
        for clause in self.all_unresolved_clauses():
            for v in clause:
                try:
                    if v > 0:
                        v_pos[v] += 1
                    else:
                        v_neg[abs(v)] += 1
                except KeyError:
                    pass

        print(v_pos)
        pos_count = max(v_pos.items(), key=operator.itemgetter(1))
        print(v_neg)
        neg_count = max(v_neg.items(), key=operator.itemgetter(1))
        if pos_count[1] > neg_count[1]:
            return pos_count[0], TRUE
        else:
            return neg_count[0], FALSE
