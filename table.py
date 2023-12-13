from typing import Union, List, Tuple, Set
from constants import TERM, RULE, Terminals, Nonterminals, RULES


def calculate_first_sets(
    rules: List[List[Tuple[int, Union[Terminals, Nonterminals]]]]
) -> List[Set[Union[Terminals, Nonterminals]]]:
    first_sets = [set() for _ in range(len(rules))]

    while True:
        old_first_sets = [set(fs) for fs in first_sets]

        for i, rule in enumerate(rules):
            for symbol_type, symbol_value in rule:
                if symbol_type == TERM:
                    first_sets[i].add(symbol_value)
                    break
                elif symbol_type == RULE:
                    first_sets[i] |= first_sets[symbol_value.value]
                    if Terminals.END not in first_sets[symbol_value.value]:
                        break
            else:
                first_sets[i].add(Terminals.END)

        if old_first_sets == first_sets:
            break

    return first_sets


def calculate_follow_sets(
    rules: List[List[Tuple[int, Union[Terminals, Nonterminals]]]],
    first_sets: List[Set[Union[Terminals, Nonterminals]]],
) -> List[Set[Union[Terminals, Nonterminals]]]:
    follow_sets = [set() for _ in range(len(rules))]
    follow_sets[Nonterminals.S.value].add(Terminals.END)

    while True:
        old_follow_sets = [set(fs) for fs in follow_sets]

        for i, rule in enumerate(rules):
            for j, (symbol_type, symbol_value) in enumerate(rule):
                if symbol_type == RULE:
                    follow_sets[symbol_value.value] |= follow_sets[i]

                    if j < len(rule) - 1:
                        next_symbol_type, next_symbol_value = rule[j + 1]
                        if next_symbol_type == TERM:
                            follow_sets[symbol_value.value].add(next_symbol_value)
                        elif next_symbol_type == RULE:
                            follow_sets[symbol_value.value] |= first_sets[
                                next_symbol_value.value
                            ] - {Terminals.END}
                    elif j == len(rule) - 1 and Terminals.END in first_sets[i]:
                        follow_sets[symbol_value.value] |= follow_sets[i]

        if old_follow_sets == follow_sets:
            break

    return follow_sets


def construct_parsing_table(
    rules: List[List[Tuple[int, Union[Terminals, Nonterminals]]]],
    first_sets: List[Set[Union[Terminals, Nonterminals]]],
    follow_sets: List[Set[Union[Terminals, Nonterminals]]],
) -> List[List[int]]:
    parsing_table = [[-1] * len(Terminals) for _ in range(len(rules))]

    for i, rule in enumerate(rules):
        first_set = first_sets[i]

        for terminal in first_set:
            if parsing_table[i][terminal.value] == -1:
                parsing_table[i][terminal.value] = i
            else:
                raise ValueError(
                    f"Conflict in parsing table at [{i}, {terminal.value}]"
                )

        if Terminals.END in first_set:
            for terminal in follow_sets[i]:
                if parsing_table[i][terminal.value] == -1:
                    parsing_table[i][terminal.value] = i
                else:
                    raise ValueError(
                        f"Conflict in parsing table at [{i}, {terminal.value}]"
                    )

    return parsing_table


def display_parsing_table(parsing_table: List[List[int]]) -> None:
    for idx, row in enumerate(parsing_table):
        print(f"[{idx}] {row}")


if __name__ == "__main__":
    first_sets = calculate_first_sets(RULES)
    follow_sets = calculate_follow_sets(RULES, first_sets)
    parsing_table = construct_parsing_table(RULES, first_sets, follow_sets)

    display_parsing_table(parsing_table)
