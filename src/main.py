def main():
    # Create a new knowledge base
    kb = KB()

    # Add some sentences to the knowledge base
    kb.tell(expr("==> (& A B) C"))
    kb.tell(expr("& A B"))
    kb.tell(expr("==> C D"))

    # Print the knowledge base
    print(kb)

    # Ask some queries
    print(kb.ask(expr("C")))  # True
    print(kb.ask(expr("D")))  # True
    print(kb.ask(expr("A")))  # False
    print(kb.ask(expr("B")))  # False
    print(kb.ask(expr("E")))  # False
    print()

if __name__ == "__main__":
    main()
