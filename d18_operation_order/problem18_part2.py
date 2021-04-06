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


def find_opening_bracket_idx(elements):
    """Finds opening bracket of expression ending with closing bracket

    Args:
        expr (List[str]): the expression ending on a closing bracket

    Returns:
        [int]: index of corresponding opening bracket
    """
    i = len(elements) -1
    char = elements[i]

    assert char == ')', f"Last element of expression was not ')', but {expr[0]}"

    closing = 0
    while not (char == '(' and closing == 1):
        if char == ')':
            closing += 1
        if char == '(':
            closing -= 1

        i -= 1
        char = elements[i]
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



def recurse_compute_expr(expr: List[str]) -> str:
    """
    Recursive computation of Sums first, then Products, (parentheses have priority).

    Iterate over string looking for sums. When found, compute sum of left and right
        terms:
        - If left term is a closing bracket, look for corresponding opening
        bracket and recurse in expression within the brackets to compute the result.
        - If right term is an opening bracket, look for corresponding closing bracket
        and recurse in expression within the brackets to compute the result.

        then sum and reset index to start of left term (left term itself, or in case
        of a bracket, left opening bracket).

    Repeat same process for products.

    return only remaining element.

    Args:
        expr (List[str]): a list of numbers, opening/closing brackets, and operations +/*.

    Returns:
        str: [description]
    """
    expr = ['0', '+'] + expr
    #### SUMS:
    i = 0
    while i < len(expr):
        char = expr[i]

        if expr[i] == '+':
            # recurse if bracketed expression

            # dummy index at start of expression to replace with result
            closing_idx = i+1
            # dummy index at start of expression to replace with result
            opening_idx = i-1


            if expr[i+1] == '(':
                closing_idx = find_closing_bracket_idx(expr[i+1:])+ i+1
                # compute term in the brackets recursively
                # from after '(' to ')' exclusive
                right_term = recurse_compute_expr(expr[i+2:closing_idx])
            else:
                right_term = expr[i+1]

            if expr[i-1] == ')':
                opening_idx = find_opening_bracket_idx(expr[:i-1+1]) # inclusive of ')'
                # compute term in brackets recursively
                # from before ')' to right after resp. opening '('
                left_term = recurse_compute_expr(expr[opening_idx+1:i-1])
            else:
                left_term = expr[i-1]

            result = execute_op(expr[i], left_term, right_term)
            # update expression
            expr = expr[:opening_idx] + [result] + expr[closing_idx+1:]
            i = opening_idx + 1
        else:
            i += 1

    #### MULTIPLICATIONS:
    i = 0
    while i < len(expr):

        if expr[i] == '*':
            # recurse if bracketed expression

            # dummy index at start of expression to replace with result
            closing_idx = i+1
            # dummy index at start of expression to replace with result
            opening_idx = i-1


            if expr[i+1] == '(':
                closing_idx = find_closing_bracket_idx(expr[i+1:])+ i+1
                # compute term in the brackets recursively
                # from after '(' to ')' exclusive
                right_term = recurse_compute_expr(expr[i+2:closing_idx])
            else:
                right_term = expr[i+1]

            if expr[i-1] == ')':
                opening_idx = find_opening_bracket_idx(expr[:i-1+1]) # inclusive of ')'
                # compute term in brackets recursively
                # from before ')' to right after resp. opening '('
                left_term = recurse_compute_expr(expr[opening_idx+1:i-1])
            else:
                left_term = expr[i-1]

            result = execute_op(expr[i], left_term, right_term)
            # update expression
            expr = expr[:opening_idx] + [result] + expr[closing_idx+1:]
        else:
            i += 1

    assert len(expr) == 1, f"expr: {expr}"
    return expr[0]


def compute_sum_exprs(exprs: List[str]) -> int:
    """Computes sum of each expression calculated unconventionally

    Computes each expression with reversed priority (first sums, then
    products), then returns the sum of all results

    Args:
        exprs (List[str]): numbers, opening/closing brackets, and operations +/*.

    Returns:
        int: sum of results from each expression in exprs
    """
    tot = 0
    for i, expr in enumerate(exprs):
        tot += int(recurse_compute_expr(expr))
        print(tot)
    return tot



if __name__ == "__main__":
    exprs = parse_input_file(test=0)

    ans2 = compute_sum_exprs(exprs)
    print(ans2)
