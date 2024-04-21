import unittest
from sympy import sympify, to_cnf

from src.utils import conjuncts, disjuncts


class TestUtils(unittest.TestCase):
    def test_disjuncts_1(self):
        expr = sympify("A | (B & C)")
        disjuncts_ = disjuncts(expr)
        self.assertEqual(disjuncts_, [sympify("A"), sympify("B & C")])

    def test_disjuncts_2(self):
        expr = sympify("A | B | C")
        disjuncts_ = disjuncts(expr)
        self.assertEqual(disjuncts_, [sympify("A"), sympify("B"), sympify("C")])

    def test_disjuncts_3(self):
        expr = sympify("(A | B) & C")
        disjuncts_ = disjuncts(expr)
        self.assertEqual(disjuncts_, [sympify("(A | B) & C")])

    def test_conjuncts_1(self):
        expr = sympify("A & (B | C)")
        conjuncts_ = conjuncts(expr)
        self.assertEqual(conjuncts_, [sympify("A"), sympify("B | C")])

    def test_conjuncts_2(self):
        expr = to_cnf("A | (B & C)")
        disjuncts_ = conjuncts(expr)
        self.assertEqual(disjuncts_, [sympify("(A | B)"), sympify("(A | C)")])


if __name__ == "__main__":
    unittest.main()
