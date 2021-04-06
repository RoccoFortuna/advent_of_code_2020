from typing import List, Union
import re


def parse_input_file(test: int = 0):
    if not test:
        with open('./d18_operation_order/input.txt', 'r') as f:
            lines = f.read().splitlines()
    else:
        with open(f'./d18_operation_order/test_input{test}.txt', 'r') as f:
            lines = f.read().splitlines()

    parsed_input = []
    for line in lines:
        chars = re.findall("([\d]+|[^ ])", line)
        parsed_input.append(chars)

    return parsed_input



def find_closing_bracket_idx(expr: List[str]) -> int:
    """Finds closing bracket of expression starting with bracket

    Args:
        expr (List[str]): the expression starting from an opening bracket

    Returns:
        [int]: index of corresponding closing bracket
    """
    assert expr[0] == '(', f"First element of expression was not ')', but {expr[0]}"
    i = 0
    char = expr[i]
    opening = 0
    while not (char == ')' and opening == 1):
        if char == '(':
            opening += 1
        if char == ')':
            opening -= 1

        i += 1
        char = expr[i]
    return i




def execute_op(op: str, num1: str, num2: str) -> str:
    """Applies operation op to tot and num

    Args:
        op (str): one in ['*', '+']
        tot (str): total to apply operation with num with
        num (str): num to apply operation on total

    Returns:
        str: new total, string result of operation between
            tot and num
    """
    if op == '+':
        return str(int(num1) + int(num2))
    elif op == '*':
        return str(int(num1) * int(num2))
    else:
        print(f"!!! Op was: {op}")



def recurse_compute_expr(expr: List[str]) -> List[str]:
    """Compute expression in nonconventional way, in order they appear in

    Order of operations follows first-come first-serve, but parenthesis
        override order.

    Args:
        expr (List[str]): expression

    Returns:
        int: value resulting from executing operations in the expression
    """
    tot = 0
    op = '+'

    # consume expression from start to end
    while expr:
        char = expr[0]
        expr = expr[1:]

        if char in ['+', '*']:
            op = char
        elif char.isnumeric():
            tot = execute_op(op, tot, char)

        # base case
        elif char == ')':
            print(f"!!! Should not have found a closing bracket?!!!\n{expr}")

        elif char == '(':
            closing_bracket_idx = find_closing_bracket_idx(expr)
            # op with recursive result
            if op is not None:
                tot = execute_op(op, tot, recurse_compute_expr(expr[:closing_bracket_idx]))
                expr = expr[closing_bracket_idx+1:]
                op = '+' # after closing a bracket there is an op again, so reset op to +
            else:
                tot = recurse_compute_expr(expr[:closing_bracket_idx])
                expr = expr[closing_bracket_idx+1:]

    return tot



def compute_sum_exprs(exprs: List[str]) -> int:
    """Computes sum of each expression calculated unconventionally

    Compute operations in the order they occur in, then give sum of results.

    Args:
        exprs (List[str]): numbers, opening/closing brackets, and operations +/*.

    Returns:
        int: sum of results from each expression in exprs
    """

    tot = 0
    for i, expr in enumerate(exprs):
        print(i+1)
        tot += int(recurse_compute_expr(expr))
    return tot



if __name__ == "__main__":
    exprs = parse_input_file(test=0)
    # print(exprs)

    ans1 = compute_sum_exprs(exprs)
    print(ans1)
