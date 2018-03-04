"""
DIMACS CNF format representations.
"""
class Literal:
    """
    Represents a literal in the DIMACS CNF format. The name
    of the literal is represented as an integer string.
    Negative number denotes the negation.
    """
    def __init__(self, value):
        self.name = value
        self.negation = value
        self._assignment = None

    @property
    def name(self):
        """ Name of the literal, always absolute value """
        return self._name

    @property
    def negation(self):
        """ Whether the literal is a negation of the actual literal """
        return self._negation

    @property
    def assignment(self):
        """ The assigned value to the literal, either 0 or 1 """
        return self._assignment

    def value(self):
        """ The resultant value of the literal, considering negation and assignment """
        if self._assignment is None:
            return None
        return -int(self._assignment) if self.negation else self._assignment

    @name.setter
    def name(self, value):
        number = int(value)
        if number == 0:
            raise ValueError('Unable to create a Literal of 0')
        # pylint: disable=W0201
        self._name = abs(number)

    @negation.setter
    def negation(self, value):
        number = int(value)
        if number == 0:
            raise ValueError('Unable to create a Literal of 0')
        # pylint: disable=W0201
        self._negation = (number < 0)

    @assignment.setter
    def assignment(self, value):
        if value is None:
            raise ValueError('Assignment cannot be None')

        val = int(value)
        if not (val == 0 or val == 1):
            raise ValueError('Unable to assign a value other than 0 or 1')

        # pylint: disable=W0201
        self._assignment = val

    def __str__(self):
        return 'C({}{})'.format('-' if self._negation else '', self._name)

    def __repr__(self):
        return self.__str__()


class Clause:
    """
    Represents a clause of the CNF form. Disjunction of literals.
    """
    def __init__(self, *args):
        self._literals = list(args)

    @property
    def literals(self):
        """ A list of Literals in disjunction """
        return self._literals

    @literals.setter
    def literals(self, lst):
        self._literals = [Literal(x) for x in lst]

    def __getitem__(self, idx):
        return self._literals[idx]

    def __setitem__(self, idx, item):
        if isinstance(item, Literal):
            self._literals[idx] = item
        else:
            self._literals[idx] = Literal(item)


class Reader:
    """ Read a .cnf file and return a list of Clauses """
    @staticmethod
    def read(fname):
        """ Reads fname and returns list of Clauses """
        with open(fname) as f:
            lines = [x.strip() for x in f.readlines()]

        literals = dict()
        clauses = []

        for line in lines:
            if line.startswith('c ') or line.startswith('p '):
                # comments skipped. number of literals/clauses do not
                # need to be read as we are using lists
                continue
            else:
                numbers = [int(x) for x in line.split(' ')][:-1]
                clause = []
                for number in numbers:
                    if number not in literals:
                        literals[number] = Literal(number)
                    clause.append(literals[number])
                clauses.append(clause)

        return clauses
