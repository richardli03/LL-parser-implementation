from table import calculate_first_sets, calculate_follow_sets, construct_parsing_table
from constants import TERM, RULE, Terminals, Nonterminals, RULES

stack = [(TERM, Terminals.END), (RULE, Nonterminals.S)]


class LLParse:
    def __init__(self, table: [list[int]]) -> None:
        # Parse table
        # self.table = [[1, -1, 0, -1, -1, -1], [-1, -1, 2, -1, -1, -1]]
        self.table = table
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
                        return True
                else:
                    raise ValueError(f"bad term on input:, {token}")
            elif stype == RULE:
                print("svalue", svalue.name, "token", token.name)
                rule = self.table[svalue.value][token.value]
                print("rule", rule)
                for r in reversed(RULES[rule]):
                    stack.append(r)
            print("stack", stack)
        return True


if __name__ == "__main__":
    inputstring = "a"
    first_sets = calculate_first_sets(RULES)
    follow_sets = calculate_follow_sets(RULES, first_sets)
    parsing_table = construct_parsing_table(RULES, first_sets, follow_sets)

    # print("Parsing Table:")
    # display_parsing_table(parsing_table)

    parser = LLParse(parsing_table)
    parser.syntactic_analysis(parser.lexical_analysis(inputstring))
