import re
from typing import List, Dict, Tuple, Set

def parse_input_file(test=False):
    if test:
        with open("./d16_ticket_translation/test_input.txt", 'r') as f:
            txt = f.read()

    else:
        with open("./d16_ticket_translation/input.txt", 'r') as f:
            txt = f.read()

    rules_txt, your_ticket_txt, nearby_tickets_txt = txt.split('\n\n')

    rules = {}
    # parse rules
    for line in rules_txt.splitlines():
        field_name, intervals_txt = line.split(": ")
        # parse intervals
        lo1, hi1, lo2, hi2 = re.findall("[0-9]+", intervals_txt)
        rules[field_name] = (int(lo1), int(hi1), int(lo2), int(hi2))

    # parse your ticket
    your_ticket = [int(k) for k in your_ticket_txt.split("\n")[1].strip("\n").split(",")]

    # parse nearby tickets
    nearby_tickets = [[int(k) for k in line.strip().split(',')] for line in nearby_tickets_txt.splitlines()[1:]]

    return rules, your_ticket, nearby_tickets


def get_invalid_fields(rules: Dict[str, Tuple[int]], ticket: List[int]) -> List[int]:
    """Given set of rules and a single ticket, returns fields not conforming to any rule

    A ticket value conforms to the rules if it is within an interval in any of the
    rules.

    Args:
        rules (Dict[str, Tuple[int]]): name of rule -> two intervals as (lo1,hi1,lo2,hi2)
            to check for field validity
        ticket (List[int]): field values

    Returns:
        List[int]: the list of invalid fields
    """
    invalid_fields = []
    for field_val in ticket:
        valid = False
        for field_name, intervals in rules.items():
            lo1, hi1, lo2, hi2 = intervals
            # check if invalid
            # if field_val<lo1 or (field_val>hi1 and field_val<lo2) or field_val > hi2:
            if (lo1 <= field_val <= hi1) or (lo2 <= field_val <= hi2):
                valid = True
                break
        if not valid:
            invalid_fields.append(field_val)

    return invalid_fields

def sum_invalid_fields(rules: Dict[str, Tuple[int]], nearby_tickets: List[List[int]]) -> int:
    """Give sum of invalid fields in all nearby tickets

    A ticket is invalid if it does not conform with any rule.
    A ticket value conforms to a rule if its value is within one of the
        corresponding intervals.

    Args:
        rules (Dict[str, Tuple[int]]):
        nearby_tickets (List[List[int]]): all other tickets as list of field values

    Returns:
        int: the sum of invalid field values
    """
    s = 0
    for ticket in nearby_tickets:
        invalid_fields = get_invalid_fields(rules, ticket)
        s += sum(invalid_fields)

    return s


def filter_out_invalid_tickets(rules: Dict[str, Tuple[int]], tickets: List[List[int]]) -> List[List[int]]:
    """Given set of rules and a list of tickets, return the list of only valid tickets

    A ticket value conforms to the rules if it is within an interval in any of the
    rules.

    Args:
        rules (Dict[str, Tuple[int]]): name_of_field -> two intervals as (lo1,hi1,lo2,hi2)
            to check for field validity, i.e. if field value is within either of the intervals
        ticket (List[int]): field values

    Returns:
        List[int]: the list of valid tickets among the input tickets, according
            to the given input rules
    """
    valid_tickets = []
    for ticket in nearby_tickets:
        invalid_fields = get_invalid_fields(rules, ticket)
        if len(invalid_fields) == 0: # if no invalid fields in the ticket
            valid_tickets.append(ticket)

    return valid_tickets


def determine_field_positions(rules: Dict[str, Tuple[int]], tickets: List[List[int]]) -> List[str]:
    """
    No assumptions made, explore possible combinations of positions of fields recursively

    Args:
        rules (Dict[str, Tuple[int]]): name_of_field -> two intervals as (lo1,hi1,lo2,hi2)
            to check for field validity, i.e. if field value is within either of the intervals
        tickets (List[List[int]]): other tickets as list of field values

    Returns:
        List[str]: field names at index corresponding to the real fields positions on tickets,
            based on other valid tickets
    """
    n_fields = len(tickets[0]) # all tickets have the same fields
    possible_fields = [{field_name for field_name in rules.keys()} for _ in range(n_fields)] # each index has a set with its possible fields

    # first rule out what fields cannot be at which positions, because
    # any ticket shows an invalid entry there
    for ticket in tickets:
        for idx, field_val in enumerate(ticket):
            for field_name, intervals in rules.items():
                lo1, hi1, lo2, hi2 = intervals
                # check if rule name could not be at curr position
                if not ((lo1<=field_val<=hi1) or (lo2<=field_val<=hi2)):
                    possible_fields[idx].remove(field_name)


    # now recurse to find the right combination
    return recurse_positions_combinations(possible_fields, [], set())

def recurse_positions_combinations(possible_fields: List[Set[str]], current_config: List[str], determined_fields: Set[str]) -> List[str]:
    """Determine a valid configuration of field positions in tickets

    Args:
        possible_fields (List[Set[str]]): set of field names each position in the ticket could have.
        current_config (List[str]): constructed positions list until current recursive step.
        determined_fields (Set[str]): fields that have been given a position until current recursive step.

    Returns:
        List[str]: field name for each position in the list, corresponding to position in the ticket.
    """
    # base case
    # if all fields have been determined, we found a valid configuration
    if len(possible_fields) == 0:
        return current_config

    # otherwise try every possible configuration at current step
    for field_name in possible_fields[0]:
        if field_name in determined_fields:
            continue # skip if we have already determined position for the given field name
        determined_fields.add(field_name)
        ret = recurse_positions_combinations(possible_fields[1:], current_config+[field_name], determined_fields)
        if ret is not None:
            return ret
        determined_fields.remove(field_name)





if __name__ == "__main__":
    rules, your_ticket, nearby_tickets = parse_input_file(test=False)

    ans1 = sum_invalid_fields(rules, nearby_tickets)
    print(ans1)

    valid_tickets = filter_out_invalid_tickets(rules, nearby_tickets)
    field_positions = determine_field_positions(rules, valid_tickets)
    print(field_positions)

    ans2 = 1
    for i, field_name in enumerate(field_positions):
        if "departure" in field_name:
            ans2 *= your_ticket[i]
    print(ans2)