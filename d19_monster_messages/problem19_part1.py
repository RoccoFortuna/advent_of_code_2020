from typing import List, Dict, Set
from collections import defaultdict

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


def recurse_generate_messages(rules: Dict[int, List[List[str]]], valid_messages: Set[str],
                                curr_mess: List[str], i: int, max_len: int):
    print(valid_messages)
    if len(curr_mess) > max_len:
        return

    if ''.join(curr_mess).isalpha():
        valid_messages.add(''.join(curr_mess))
        return

    ## substitute first element with possible substitutes
    el = curr_mess[i]
    # skip end terminal tokens
    #  and i < len(curr_mess)
    while el.isalpha():
        i += 1
        el = curr_mess[i]
    # char is now first number element


    # recurse with substituted mess
    el_becomes = rules[el]
    for new_els in el_becomes:
        fork_mess = curr_mess[:i] + new_els + curr_mess[i+1:]
        recurse_generate_messages(rules, valid_messages, fork_mess, i, max_len)





def count_valid_messages(rules: Dict[int, List[List[str]]], messages: str, start_rule: int = 0) -> int:
    """Count messages conforming to a set of rules

    Args:
        rules (Dict[List[List[str]]]): message generation rules
        messages (str): all recieved messages to filter valid ones from

    Returns:
        int: number of valid messages
    """
    # get maximum message length of messages to check for validity:
    max_len = max([len(m) for m in messages])

    # 1: generate set of possible messages
    valid_messages = set()
    # call set populating void
    recurse_generate_messages(rules, valid_messages, [str(start_rule)], i=0, max_len=max_len)
    # print(valid_messages)
    c = 0
    for m in messages:
        if m in valid_messages:
            c += 1

    return c



if __name__ == "__main__":
    rules, messages = parse_input_file(test=2)

    ans1 = count_valid_messages(rules, messages)
    print(ans1)

