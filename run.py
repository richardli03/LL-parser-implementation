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
        """Tokenize a string for syntactic analysis.

        :param string_to_tokenize: Input string to analyze.
        :type string_to_tokenize: str
        :return: Tokens for syntactic analysis.
        :rtype: List[Union[Terminals, Nonterminals]]
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
        """Syntactically analyze the tokenization of a string.

        Determine whether to reject or accept the string based upon the grammar.

        :param tokens: Tokens for syntactic analysis.
        :type tokens: List[Union[Terminals, Nonterminals]]
        :return: True if the string is accepted, False otherwise.
        :rtype: bool
        """

        position = 0
        while len(stack) > 0:
            (stack_type, stack_value) = stack.pop()
            token = tokens[position]
            if stack_type == TERM:
                if stack_value == token:
                    position += 1
                    print("popping", stack_value)
                    if token == Terminals.END:
                        print("ACCEPT")
                        return True
                else:
                    print("REJECT")
                    raise ValueError(f"{token}")
            elif stack_type == RULE:
                # print("stack_value", stack_value.name, "token", token.name)
                rule = self.table[stack_value.value][token.value]
                # print("rule", rule)
                for r in reversed(RULES[rule]):
                    stack.append(r)
            print("current stack contains:", stack)
        return True


if __name__ == "__main__":
    # inputstring = "b*(a+a)"  # TO SEE VALUE ERROR
    inputstring = "(a+a)"
    first_sets = calculate_first_sets(RULES)
    follow_sets = calculate_follow_sets(RULES, first_sets)
    parsing_table = construct_parsing_table(RULES, first_sets, follow_sets)

    # print("Parsing Table:")
    # display_parsing_table(parsing_table)

    parser = LLParse(parsing_table)
    parser.syntactic_analysis(parser.lexical_analysis(inputstring))
