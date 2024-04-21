import random
import utils


class Solver:
    """SAT solver."""

    @staticmethod
    def solve(clauses):
        return Solver.__solve_walk_sat(clauses)

    @staticmethod
    def __solve_walk_sat(clauses, p=0.5, max_flips=1000):
        """Checks for satisfiability of all clauses by randomly flipping values of variables
        >>> WalkSAT([A & ~A], 0.5, 100) is None
        True
        """
        # Set of all symbols in all clauses
        symbols = {sym for clause in clauses for sym in clause.free_symbols}
        # model is a random assignment of true/false to the symbols in clauses
        model = {s: random.choice([True, False]) for s in symbols}
        for _ in range(max_flips):
            satisfied, unsatisfied = [], []
            for clause in clauses:
                (satisfied if clause.subs(model) else unsatisfied).append(clause)

            if not unsatisfied:  # if model satisfies all the clauses
                return model
            clause = random.choice(unsatisfied)
            if utils.prob(p):
                sym = random.choice(list(clause.free_symbols))
            else:
                # Flip the symbol in clause that maximizes number of sat. clauses
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
