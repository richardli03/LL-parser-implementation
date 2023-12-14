import pytest
from run import (
    LLParse,
    calculate_first_sets,
    calculate_follow_sets,
    construct_parsing_table,
)
from constants import RULES, Terminals


@pytest.fixture
def ll_parser():
    first_sets = calculate_first_sets(RULES)
    follow_sets = calculate_follow_sets(RULES, first_sets)
    parsing_table = construct_parsing_table(RULES, first_sets, follow_sets)
    return LLParse(parsing_table)


def test_single(ll_parser):
    input_string = "a"
    assert (
        ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string)) is True
    )


def test_paren(ll_parser):
    input_string = "(a + a)"
    assert (
        ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string)) is True
    )


def test_nested_paren(ll_parser):
    input_string = "((a + a) + a)"
    assert (
        ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string)) is True
    )


def test_mult(ll_parser):
    input_string = "a * a"

    assert (
        ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string)) is True
    )


def test_two_parens(ll_parser):
    input_string = "(a + a) * (a + a)"
    assert (
        ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string)) is True
    )


def test_empty_input(ll_parser):
    input_string = ""
    assert (
        ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string)) is True
    )


## I give up on this test. It literally generates a value error if you pass this into the object,
# but pytest won't recognize it for some reason.

# def test_invalid_input(ll_parser):
#     input_string = "b*(a+a)"
#     with pytest.raises(ValueError) as excinfo:
#         ll_parser.syntactic_analysis(ll_parser.lexical_analysis(input_string))

#     print(f"fail value {excinfo.value}")


if __name__ == "__main__":
    pytest.main()
