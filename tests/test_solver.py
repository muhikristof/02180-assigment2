import unittest
from sympy import sympify, to_cnf

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/src")

from src.solver import Solver


class TestUtils(unittest.TestCase):
    def test_solve_walk_sat_1(self):
        model = Solver.solve([sympify("A & B & Not(C)")])
        self.assertEqual(
            model, {sympify("A"): True, sympify("B"): True, sympify("C"): False}
        )

    def test_solve_walk_sat_2(self):
        model = Solver.solve([sympify("A & B & C")])
        self.assertEqual(
            model, {sympify("A"): True, sympify("B"): True, sympify("C"): True}
        )

    def test_solve_walk_sat_3(self):
        model = Solver.solve([sympify("A >> B")])
        self.assertEqual(
            model, {sympify("A"): True, sympify("B"): True, sympify("C"): True}
        )


if __name__ == "__main__":
    unittest.main()
