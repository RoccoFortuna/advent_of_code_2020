import functools
import math
from typing import List, Tuple

"""
Given an integer (earliest possible departure time) and a list of
integers (ID corresponding to number of minutes between each departure
of each shuttle), return product of ID and number of minutes to wait for
such shuttle
"""

def parse_input_file(test: bool = False):
    input_path = "./d13_shuttle_search/input.txt" if not test else "./d13_shuttle_search/test_input.txt"
    with open(input_path, "r") as file:
        lines = file.read().splitlines()

    return int(lines[0]), lines[1].split(',')


def find_soonest_shuttle(departure: int, shuttle_ids: List[int]) -> int:
    """
    Solution to part 1

    Args:
        departure (int): departure time
        shuttle_ids (List[int]): correspond to time taken between
            departures starting at t=0

    Returns:
        int: product between ID of earliest shuttle departing and number
            of minutes to wait for the bus
    """
    valid_ids = [int(n) for n in shuttle_ids if n!='x']
    # initialise shortest waiting time to inf, shuttle ID to
    shortest_time_shuttle = (float('inf'), None)

    for shuttle_id in valid_ids:
        # ceiling(dep_time / shuttle_id) * shuttle_id gives
        # the nearest integer >= departure time,
        # so we gan get the time to wait by subtracting departure time
        waiting_time = (math.ceil(departure/shuttle_id) * shuttle_id ) - departure

        # and update if smaller than the minimum time to wait
        if waiting_time < shortest_time_shuttle[0]:
            shortest_time_shuttle = (waiting_time, shuttle_id)

    return shortest_time_shuttle[0] * shortest_time_shuttle[1]


def subseq_ids_meet_condition(subseq_shuttle_ids: List[Tuple[int, int]], t):
    """
    Check if subsequent ids meet condition

    Check if subsequent ids meet the following condition:
        each subsequent listed bus ID departs at that subsequent minute,
        starting from minute 1.
    """
    for shuttle_id, offset in zip(*subseq_shuttle_ids):
        print(shuttle_id, offset)
        print(t+offset)
        # if shuttle_id does not divide timestamp + offset, fail condition and continue
        if not ((t + offset) % shuttle_id == 0):
            return False

    return True



def chinese_remainder(n, a):
    sum = 0
    prod = functools.reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def find_subsequent_departures_time_CRT(shuttle_ids: List[int]) -> int:
    """Use Chineese Remainder Theorem:

    e.g.:
        if:
        n % 29 = 0
        n + 19 % 41 = 0 -> n % 41 = -19 = 41-19 = 22
        n + 29 % 661 = 0 -> n % 661 = -29 = 661-29 = 632
        ...

        then:
        n % (29 * 41 * 661 ...) = 22 * 632 * ...

    Args:
        shuttle_ids (List[int]): tuples with (shuttle_id, time offset)

    Returns:
        int: first departure time in subsequent sequence
    """
    shuttle_ids_offsets = [(int(n), -i) for i, n in enumerate(shuttle_ids) if n!='x']
    shuttle_ids, neg_increments = zip(*shuttle_ids_offsets)
    return chinese_remainder(shuttle_ids, neg_increments)


def find_subsequent_departures_time_SQEUENTIAL(shuttle_ids: List[int]) -> int:
    """Use incremental solution

    e.g.:
        with ids and offsets: (29, 0), (41, 19), (661, 29), (13, 42), (17, 43),
            (23, 52), (521, 60), (37, 66), (19, 79)

        Start incrementing t by 29 at a time,
            - if t + offset of next element is divisible by next element:
                increase increment to increment*element,
                continue recursing with next elements in ids_offsets

    Args:
        shuttle_ids (List[int]): tuples with (shuttle_id, time offset)

    Returns:
        int: first departure time in subsequent sequence
    """
    shuttle_ids_offsets = [(int(n), i) for i, n in enumerate(shuttle_ids) if n!='x']
    return recurse(shuttle_ids_offsets[1:], 0, shuttle_ids_offsets[0][0])

def recurse(ids_offsets, t, increment):
    # base case
    if len(ids_offsets) == 0:
        return t

    shuttle_id, offset = ids_offsets[0]
    while (t + increment + offset) % shuttle_id != 0:
        t += increment

    return recurse(ids_offsets[1:], t+increment, increment*shuttle_id)


if __name__ == "__main__":
    departure, shuttle_ids = parse_input_file(test=False)

    ans1 = find_soonest_shuttle(departure, shuttle_ids)
    print(ans1)


    ## Solve with two different approaches:
    # Chineese Remainder Theorem
    ans2 = find_subsequent_departures_time_CRT(shuttle_ids)
    print(ans2)

    # Sequential approach
    ans2 = find_subsequent_departures_time_SQEUENTIAL(shuttle_ids)
    print(ans2)
