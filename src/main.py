from knowledge_base import KnowledgeBase, Belief
from sympy import sympify


def main():
    # Create a new knowledge base
    kb = KnowledgeBase()

    # Add some sentences to the knowledge base
    kb.tell(Belief("A & B & C & Not(D)", 1))

    # Ask some queries
    print(kb.ask("A"))  # True
    print(kb.ask("B"))  # True
    print(kb.ask("A >> D"))  # False


if __name__ == "__main__":
    main()
