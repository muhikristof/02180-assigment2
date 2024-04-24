from knowledge_base import KnowledgeBase, Belief


def main():
    # Create a new knowledge base
    kb = KnowledgeBase()

    # Add some sentences to the knowledge base
    kb.expand(Belief("A & B & C & Not(D)", 1.0))
    kb.expand(Belief("A & B", 1.0))
    kb.expand(Belief("A & C", 1.0))
    print(kb)
    kb.revise(Belief("A & B & C", 1.0))
    print(kb)
    # kb.expand(Belief("A | C", 0.75))
    # kb.expand(Belief("A & C", 0.75))
    # kb.expand(Belief("A | F", "0.4"))
    # kb.expand(Belief("D >> A", "0.4"))
    # print(kb)

    # kb.expand(Belief("B & (C >> (A | D)) >> Not(D) >> Not(D)", "0.7"))

    # print(kb)

    # # Ask some queries
    # print(kb.ask("A"))  # True
    # print(kb.ask("B"))  # True
    # print(kb.ask("A >> D"))  # False
    # print(kb.ask("Not(A)"))  # False
    # print(kb.ask("F & Not(F)"))  # False
    # print(kb.ask("F | Not(F)"))  # True


if __name__ == "__main__":
    main()
