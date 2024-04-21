from sympy.logic.boolalg import Or, And
import random


def prob(p) -> bool:
    """Return True with probability p."""
    return random.uniform(0, 1) < p


def disjuncts(expr):
    """Return a list of disjuncts in the expression expr.
    >>> disjuncts(A | B)
    [A, B]
    >>> disjuncts(A & B)
    [(A & B)]
    """
    return dissociate(Or, expr)


def conjuncts(expr):
    """Return a list of conjuncts in the expression expr.
    >>> conjuncts(A & B)
    [A, B]
    >>> conjuncts(A | B)
    [(A | B)]
    """
    return dissociate(And, expr)


def dissociate(op, expr):
    """Given an associative operator op, return a flattened list of its args.
    >>> dissociate(And, A & B)
    [A, B]
    >>> dissociate(Or, A | B | C)
    [A, B, C]
    """
    result = []

    def collect(subexpr):
        if subexpr.func == op:
            for arg in subexpr.args:
                collect(arg)
        else:
            result.append(subexpr)

    collect(expr)
    return result
