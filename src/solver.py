import random
from typing import Dict, List

from sympy import Symbol
from sympy.logic.boolalg import BooleanFunction, is_cnf
import utils


class Solver:
    """SAT solver."""

    @staticmethod
    def solve(clauses):
        return Solver.__solve_walk_sat(clauses)

    @staticmethod
    def __solve_walk_sat(
        clauses: List[BooleanFunction], p: float = 0.5, max_flips: int = 1000
    ) -> Dict[Symbol, bool] | None:
        """Checks for satisfiability of the given clauses using WalkSAT algorithm.

        @Warning: Clauses must be in CNF!

        Parameters:
            clauses (List[BooleanFunction]): The list of clauses to be checked for satisfiability.
            p (float): The probability of choosing a random symbol.
            max_flips (int): The maximum number of flips allowed.

        Returns:
            Dict[Symbol, bool] | None: A model that satisfies the clauses, or None if no such model exists.

        >>> Solver.__solve_walk_sat([A & B & Not(C)])
        {A: True, B: True, C: False}
        """

        # Check if the clauses are all in CNF
        if not all(is_cnf(clause) for clause in clauses):
            raise ValueError("Clauses must be in CNF!")

        # Get all the symbols in the clauses
        symbols = set().union(*[clause.free_symbols for clause in clauses])

        # Build a random model
        model = {s: random.choice([True, False]) for s in symbols}
        for _ in range(max_flips):
            satisfied, unsatisfied = [], []
            for clause in clauses:
                (satisfied if clause.subs(model) else unsatisfied).append(clause)

            # If all clauses are satisfied, return the model
            if not unsatisfied:
                return model

            clause = random.choice(unsatisfied)
            if utils.prob(p):
                sym = random.choice(list(clause.free_symbols))
            else:
                # Flip the symbol in clause that maximizes number of sat clauses
                def sat_count(sym):
                    # Return the the number of clauses satisfied after flipping the symbol.
                    model[sym] = not model[sym]
                    count = len([clause for clause in clauses if clause.subs(model)])
                    model[sym] = not model[sym]
                    return count

                sym = max(clause.free_symbols, key=sat_count)
            model[sym] = not model[sym]

        # If no solution is found within the flip limit, we return failure
        return None
