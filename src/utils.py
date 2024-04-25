from sympy.logic.boolalg import Or, And, to_cnf
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
        if isinstance(subexpr, op):
            for arg in subexpr.args:  # access the arguments of the operator
                collect(arg)
        else:
            result.append(subexpr)

    if isinstance(expr, str):
        expr = to_cnf(expr)  # Convert string expressions to CNF
    collect(expr)
    return result


def associate(op, expr_list):
    """Rebuild an expression from a list of sub-expressions using a specified operator    """
    if not expr_list:
        return op.identity
    elif len(expr_list) == 1:
        return expr_list[0]
    else:
        combined_expr = op(*expr_list)  # Rebuild the expression using the operator
        return combined_expr
