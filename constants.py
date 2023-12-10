from enum import Enum

# All constants are indexed from 0
TERM = 0
RULE = 1


# Terminals
class Terminals(Enum):
    LPAR = 0
    RPAR = 1
    A = 2
    PLUS = 3
    END = 4
    INVALID = 5


# Non-Terminals
class Nonterminals(Enum):
    S = 0
    F = 1


RULES = [
    [(RULE, Nonterminals.F)],
    [
        (TERM, Terminals.LPAR),
        (RULE, Nonterminals.S),
        (TERM, Terminals.PLUS),
        (RULE, Nonterminals.F),
        (TERM, Terminals.RPAR),
    ],
    [(TERM, Terminals.A)],
]

if __name__ == "__main__":
    print("constants")
