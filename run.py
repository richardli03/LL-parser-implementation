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

stack = [(TERM, Terminals.END), (RULE, Nonterminals.S)]


class LLParse:
    def __init__(self) -> None:
        # Parse table
        self.table = [[1, -1, 0, -1, -1, -1], [-1, -1, 2, -1, -1, -1]]

        pass

    def lexical_analysis(self, string_to_tokenize):
        """Tokenize a string to

        :param string_to_analyze: _description_
        :type string_to_analyze: _type_
        :return: _description_
        :rtype: _type_
        """
        tokens = []
        for character in string_to_tokenize:
            if character == "+":
                tokens.append(Terminals.PLUS)
            elif character == "(":
                tokens.append(Terminals.LPAR)
            elif character == ")":
                tokens.append(Terminals.RPAR)
            elif character == "a":
                tokens.append(Terminals.A)
            else:
                tokens.append(Terminals.INVALID)
        tokens.append(Terminals.END)
        # print(tokens)
        return tokens

    def syntactic_analysis(self, tokens):
        """Syntatically analyze the tokenization of a string
        to determine whether to reject or accept the string based upon
        our grammar.

        :param tokens: _description_
        :type tokens: _type_
        """
        position = 0
        while len(stack) > 0:
            (stype, svalue) = stack.pop()
            token = tokens[position]
            if stype == TERM:
                if svalue == token:
                    position += 1
                    print("pop", svalue)
                    if token == Terminals.END:
                        print("input accepted")
                else:
                    print("bad term on input:", token)
                    break
            elif stype == RULE:
                print("svalue", svalue.name, "token", token.name)
                rule = self.table[svalue.value][token.value]
                print("rule", rule)
                for r in reversed(RULES[rule]):
                    stack.append(r)
            print("stack", stack)


if __name__ == "__main__":
    inputstring = "(a+a)"
    parser = LLParse()
    parser.syntactic_analysis(parser.lexical_analysis(inputstring))
