"""
RegEx version of part 1, with pruning of too long regexpressions, and
updated rules:
    - parsed_rules['8'] = [['42'], ['42', '8']]
    - parsed_rules['11'] = [['42', '31'], ['42', '11', '31']]

"""

from typing import List, Dict, Set
from collections import defaultdict
import re

def parse_input_file(test: int = 0):
    if not test:
        with open('./d19_monster_messages/input.txt', 'r') as f:
            rules, messages = f.read().split("\n\n")
    else:
        with open(f'./d19_monster_messages/test_input{test}.txt', 'r') as f:
            rules, messages = f.read().split("\n\n")

    parsed_rules = defaultdict(list)
    for rule in rules.splitlines():
        left, right = rule.split(": ")
        for r in right.split(" | "):
            parsed_rules[left].append([s.strip('"') for s in r.split()])

    messages = messages.split()

    return parsed_rules, messages



def recurse_generate_patterns(rules: Dict[int, List[List[str]]], valid_patterns: Set[str],
                                curr_pattern: List[str], i: int, max_len: int, curr_len: int= 1):
    """
    Generate RegEx patterns to match the valid messages

    Expands numerical rules to obtain final rule with only terminals "a" and "b".
    Treat rules '8' and '11' in a special way:
        8: since we have rules['8'] = [['42'], ['42', '8']],
            8 can produce 1 or more 42s, so we replace with 42+
        11: since we have rules['11'] = [['42', '31'], ['42', '11', '31']],
            11 can produce equal number n of 42s as 31s. This is not supported in
            regex, and therefore recursion is used. A heuristic was applied based
            on the expected computational complexity, where n is at most 5.

    When a pattern contains no more numerical rules to expand, it is added to the
    set of valid messages patterns valid_patterns.

    Args:
        rules (Dict[int, List[List[str]]]): message validity rules
        valid_patterns (Set[str]): RegEx patterns corresponding to valid messages
        curr_pattern (List[str]): pattern found until this point in recursion
        i (int): position on the current pattern string, to convert to only terminal
            characters "a" and "b".
        max_len (int): not used atm. Could be employed for pruning with curr_len.
        curr_len (int, optional): Minimum length of matched sequence by
            curr_pattern. Starts from 1, with curr_pattern as 0.

    """
    while i < len(curr_pattern):
        # print(curr_pattern)
        print(valid_patterns)
        # change current element
        el = curr_pattern[i]
        # if current element is not numeric (anymore), increase i
        # (i.e. skip '|', '(', ')' and terminal chars 'a', 'b')
        if not el.isnumeric():
            i += 1
            continue

        if el == '11':
            # need to expand itself "a couple" of times? assumption is that messages
            # have a limited size, so a too long regex won't match anyways
            new_el = ['42', '31']
            for _ in range(4):
                new_pattern = curr_pattern[:i] + new_el + curr_pattern[i+1:]
                recurse_generate_patterns(rules, valid_patterns, new_pattern, i, max_len, curr_len + len(new_el))

                new_el = ['42'] + new_el + ['31']
            return


        transforms_to = rules[el]
        curr_len_increment = min([len(k) for k in transforms_to])
        curr_len += curr_len_increment
        assert len(transforms_to) <= 2, (f'more than one pipe: {el}: {transforms_to}')
        new_el = transforms_to[0] if len(transforms_to) == 1 else ['('] + transforms_to[0] + ['|'] + transforms_to[1] + [')']

        # if '8': 42 | 42 8, so 42+
        plus_quantifier = ['+'] if el == '8' else []
        curr_pattern = curr_pattern[:i] + new_el + plus_quantifier + curr_pattern[i+1:] # exclude @i


    # if no numbers in it, it's a valid pattern matching terminals
    str_pattern = ''.join(curr_pattern)
    if re.search('\d', str_pattern) is None:
        # if no digit is matched, rule is terminal
        valid_patterns.add(str_pattern)
        return




def count_valid_messages(rules: Dict[int, List[List[str]]], messages: str, start_rule: int = 0) -> int:
    """Count messages conforming to a set of rules

    Args:
        rules (Dict[List[List[str]]]): valid messages rules
        messages (str): all recieved messages to filter valid ones from

    Returns:
        int: number of valid messages
    """
    # get maximum message length of messages to check for validity:
    max_len = max([len(m) for m in messages])

    # 1: generate set of possible messages
    valid_messages_patterns = set()
    # call set populating void
    recurse_generate_patterns(rules, valid_messages_patterns, [str(start_rule)], i=0, max_len=max_len)
    # print(valid_messages)
    c = 0
    for m in messages:
        for pattern in valid_messages_patterns:
            # if m matches
            if re.fullmatch(pattern, m):
                c += 1  # only count if it matches any of the valid patterns
                break
    return c



if __name__ == "__main__":
    rules, messages = parse_input_file(test=0)

    # for k, v in rules.items():
    #     print(f"{type(k)}: {type(v)}")
    #     print(f"{k}: {v}")

    ans2 = count_valid_messages(rules, messages)
    print(ans2)
