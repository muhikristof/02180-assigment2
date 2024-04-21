from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
import heapq
from itertools import groupby
from typing import List
from solver import Solver

from sympy import Equivalent, to_cnf
from sympy.logic.boolalg import BooleanFunction, Not


class Belief:
    """A class to represent a belief in the knowledge base.

    Attributes:
        expr (BooleanFunction): The expression representing the belief.
        order (Decimal): The order of the belief.
    """

    def __init__(self, expr: BooleanFunction | str, order: str | int | float | Decimal):
        """Initializes the Belief object.

        Parameters:
            expr (BooleanFunction | str): The expression representing the belief.
            order (Decimal): The order of the belief.
        """
        self.expr = to_cnf(expr)
        self.order = Decimal(order)

        if self.order > 1 or self.order < 0:
            raise ValueError("Order must be between 0 and 1.")

    def __lt__(self, other):
        """@WARNING: We define __lt__ like that so that heapq orders the beliefs in descending order! It is not consistent with the __le__ operator!"""
        return not (self.order < other.order)

    def cmp_lt(self, other):
        return self.order < other.order

    def cmp_gt(self, other):
        return self.order > other.order

    def cmp_le(self, other):
        return self.order <= other.order

    def cmp_ge(self, other):
        return self.order >= other.order

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
        """Adds a belief to the knowledge base. This action is considered UNSAFE, as it does not check for consistency of the knowledge base.

        Parameters:
            belief (Belief): The belief to be added to the knowledge base.
        """
        heapq.heappush(self.beliefs, belief)

    def revise(self, belief: Belief):
        """Revises the knowledge base by retracting any belief that is inconsistent with the new belief and expanding the knowledge base with the new belief.

        Revision is implemented using Levi's identity: B ⋆ φ = (B ÷ ¬φ) + φ.

        Parameters:
            belief (Belief): The belief to be added to the knowledge base.
        """
        pass

    def retract(self, belief: Belief):
        """Retracts a belief from the knowledge base."""
        pass

    def max_degree(self, expr: BooleanFunction | bool) -> Decimal:
        """Finds such a maximum degree of belief in the knowledge base that for all
        beliefs with the same or higher degree of belief, the given expression is entailed.

        Parameters:
            expr (BooleanFunction | bool): The expression to be checked for entailment.

        Returns:
            Decimal: Maximum degree of belief in the knowledge base that entails the given expression.
        """
        expr_cnf = to_cnf(expr)
        if expr_cnf or self.entails([], expr_cnf):
            return Decimal(1)

        local_kb = []
        for order, beliefs in groupby(self.beliefs, key=lambda b: b.order):
            local_kb += [b.expr for b in beliefs]
            if self.entails(local_kb, expr_cnf):
                return order

        return Decimal(0)

    def expand(self, new_belief: Belief):
        """Expands the knowledge base with the new belief."""

        if self.ask(Not(new_belief.expr)):
            raise ValueError("Contradictory beliefs.")

        # For tautological beliefs, set order to 1
        if self.entails([], new_belief.expr):
            new_belief.order = Decimal(1)
        else:
            for kb_belief in filter(lambda b: new_belief.cmp_ge(b), self.beliefs):
                impl_degree = self.max_degree(kb_belief.expr >> new_belief.expr)

                if (kb_belief.order <= new_belief.order < impl_degree) or self.entails(
                    [], Equivalent(new_belief.expr, kb_belief.expr)
                ):
                    # Update the order of the belief from the knowledge base to the new degree of belief
                    kb_belief.order = new_belief.order
                else:
                    kb_belief.order = impl_degree

                # Fix the order of the belief in the knowledge base
                heapq.heapify(self.beliefs)

        self.tell(new_belief)

    def ask(self, expr: BooleanFunction | str) -> bool:
        """Checks if the given expression is entailed by the knowledge base.

        Parameters:
            expr (BooleanFunction | str): The expression to be checked for entailment.

        Returns:
            bool: True if the expression is entailed by the knowledge base, False otherwise.
        """
        return self.entails(self.clauses(), expr)

    def clauses(self) -> List[BooleanFunction]:
        """Returns the list of clauses representing the knowledge base."""
        return [b.expr for b in self.beliefs]

    @staticmethod
    def entails(kb: List[BooleanFunction], expr: BooleanFunction | str) -> bool:
        """Checks if the given expression is entailed by the knowledge base using the semantic deduction theorem:
        φ ⊨ ψ, iff φ → ψ is a tautology. In other words, φ ⊨ ψ iff the sentence (φ ∧ ¬ψ) is unsatisfiable.

        Parameters:
            kb (List[BooleanFunction]): The list of clauses representing the knowledge base.
            expr (BooleanFunction | str): The expression to be checked for entailment.

        Returns:
            bool: True if the expression is entailed by the knowledge base, False otherwise.
        """
        return Solver.solve(kb + [to_cnf(Not(expr))]) is None

    def __repr__(self):
        return (
            "KnowledgeBase(beliefs=[\n"
            + "\n".join([f"\t{b}," for b in self.beliefs])
            + "\n])"
        )
