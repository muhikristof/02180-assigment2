from copy import deepcopy
from dataclasses import dataclass
import heapq
from typing import List

from sympy import to_cnf, Expr


class Belief:
    """A class to represent a belief in the knowledge base."""

    def __init__(self, expr: Expr, order: float):
        """Initializes the Belief object.

        Parameters:
            expr (sympy.Expr): The expression representing the belief.
            order (float): The order of the belief.
        """
        if order > 1 or order < 0:
            raise ValueError("Order must be between 0 and 1.")

        self.expr = to_cnf(expr)
        self.order = order

    def __lt__(self, other):
        return self.order < other.order

    def __eq__(self, other):
        return self.expr == other.expr and self.order == other.order

    def __str__(self):
        return f"Belief(expr={self.expr}, order={self.order})"

    def __repr__(self):
        return self.__str__()


class KnowledgeBase:
    """A class to represent a knowledge base.

    Attributes:
        beliefs (List[Belief]): The list of Beliefs representing the knowledge base, ordered by order.
    """

    def __init__(self, beliefs: List[Belief] | None = None):
        """Initializes the KnowledgeBase object.

        Parameters:
            beliefs (List[Belief]): The list of Beliefs representing the initial state of the knowledge base.
        """

        self.beliefs: List[Belief] = deepcopy(beliefs) if beliefs else []
        if beliefs:
            heapq.heapify(beliefs)

    def tell(self, belief: Belief):
        """Adds a belief to the knowledge base.

        Parameters:
            belief (Belief): The belief to be added to the knowledge base.
        """

        heapq.heappush(self.beliefs, belief)

    def ask(self):
        pass

    def entails(self, expr):
        pass

    def retract(self, expr):
        pass
