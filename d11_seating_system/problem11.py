from typing import List, Dict
import copy


def parse_input_file(test: bool = False):
    if test:
        input_path = "./d11_seating_system/test_input.txt"
    else:
        input_path = "./d11_seating_system/input.txt"

    with open(input_path, "r") as file:
        lines = file.readlines()
    return [[char for char in s if char != '\n'] for s in lines]


def get_n_adj_occ(seats_layout: List[str], y: int, x: int) -> int:
    """Given seats layout, find number of occupied seats adjacent to (y, x)

    Seats layout is a grid of:
        - "#": occupied seat
        - "L": empty seat
        - ".": floor (always empty)



    Args:
        seats_layout (List[str]): seats layout
        y (int): y coor of position to chech for
        x (int): x coor of position to chech for

    Returns:
        int: number of occupied seats adjacent to position (y, x)
    """
    adjacency_increments =\
        [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    n_adj_occ = 0
    for y_incr, x_incr in adjacency_increments:
        y_coor, x_coor = y+y_incr, x+x_incr

        # if coordinate not valid
        if y_coor < 0 or y_coor >= len(seats_layout) or x_coor < 0 or x_coor >= len(seats_layout[0]):
            continue

        # if new coor is occupied -> count it
        if seats_layout[y_coor][x_coor] == '#':
            n_adj_occ += 1

    return n_adj_occ


def simulate_step_part1(prev_layout: List[str]) -> List[str]:
    """Simulate a step of the seats system (part1)

    Seats system follows the following rules:
    - If a seat is empty (L) and there are no occupied seats
        adjacent to it, the seat becomes occupied.
    - If a seat is occupied (#) and four or more seats adjacent
        to it are also occupied, the seat becomes empty.
    - Otherwise, the seat's state does not change.

    Args:
        prev_layout (List[str]): rows of chars as seats state

    Returns:
        List[str]: new seats layout
    """
    new_layout = copy.deepcopy(prev_layout)

    for y in range(len(prev_layout)): # vertical coordinate
        for x in range(len(prev_layout[0])): # horizontal coordinate
            # determine current place state
            curr_state = prev_layout[y][x]

            if curr_state == '.': # nothing to change
                continue

            # count adjacent occupied seats
            adj_occ = get_n_adj_occ(prev_layout, y, x)

            if curr_state == '#' and adj_occ >= 4: # if rule applies
                new_layout[y][x] = 'L' # make seat empty

            elif curr_state == 'L' and adj_occ == 0: # if rule applies
                new_layout[y][x] = '#' # make seat occupied

    return new_layout


def get_n_visible_occ(prev_layout: List[str], y: int, x: int) -> int:
    """Find number of visible occupied places from given coor

    From a given position (y,x), sight extends in vertical/horizontal
        and diagonal directions until a seat is found (occupied '#' or not 'L')


    Args:
        prev_layout (List[str]): seats layout to count visible occupied seats from
        y (int): vertical position to look from
        x (int): horizontal position to look from

    Returns:
        int: number of directions where a '#' is present before a 'L'.
    """

    adjacency_increments =\
        [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    n_visible_occ = 0
    for y_incr, x_incr in adjacency_increments:
        y_coor, x_coor = y+y_incr, x+x_incr
        is_valid_location = not (y_coor < 0 or y_coor >= len(prev_layout) or x_coor < 0 or x_coor >= len(prev_layout[0]))

        # keep increasing until boundaries of layout, or '#' or 'L' are found
        while is_valid_location and prev_layout[y_coor][x_coor] != 'L' and prev_layout[y_coor][x_coor] != '#':
            y_coor, x_coor = y_coor+y_incr, x_coor+x_incr
            is_valid_location = not (y_coor < 0 or y_coor >= len(prev_layout) or x_coor < 0 or x_coor >= len(prev_layout[0]))

        # if new coor is occupied -> count it
        if is_valid_location and prev_layout[y_coor][x_coor] == '#':
            n_visible_occ += 1

    return n_visible_occ

def simulate_step_part2(prev_layout: List[str]) -> List[str]:
    """ Simulate a step of the seats system

    Seats system follows the following rules:
    - If a seat is empty (L) and there are no occupied seats
        adjacent to it, the seat becomes occupied.
    - If a seat is occupied (#) and four or more seats adjacent
        to it are also occupied, the seat becomes empty.
    - Otherwise, the seat's state does not change.

    Args:
        prev_layout (List[str]): rows of chars as seats state
    """
    new_layout = copy.deepcopy(prev_layout)

    for y in range(len(prev_layout)): # vertical coordinate
        for x in range(len(prev_layout[0])): # horizontal coordinate
            # determine current place state
            curr_state = prev_layout[y][x]

            if curr_state == '.': # nothing to change
                continue

            # count adjacent occupied seats
            visible_occ = get_n_visible_occ(prev_layout, y, x)

            if curr_state == '#' and visible_occ >= 5: # if rule applies
                new_layout[y][x] = 'L' # make seat empty

            elif curr_state == 'L' and visible_occ == 0: # if rule applies
                new_layout[y][x] = '#' # make seat occupied

    return new_layout


def simulate_seat_system(seats_layout: List[str], part: int) -> List[str]:
    """Simulate seat system on seats layout for given problem part

    Args:
        seats_layout (List[str]): grid of seats
        part (int): 1 for part 1, 2 for part 2

    Returns:
        List[str]: final seats layout
    """
    if part == 2:
        simulate_step = simulate_step_part2
    elif part == 1:
        simulate_step = simulate_step_part1

    new_layout = copy.deepcopy(seats_layout)
    prev_layout = None
    while prev_layout != new_layout:
        prev_layout = copy.deepcopy(new_layout)
        new_layout = simulate_step(new_layout)

    return new_layout



def final_n_occupied_seats(seats_layout: List[str], part: int = 1) -> int:
    """
    Given a seats layout, simulate system and count occ seats at termination

    Seats layout is given as a list of strings, where:
        '#': occupied seat
        'L': empty seat
        '.': no seat

    Args:
        seats_layout (List[str]): rows of seats layout as string

    Returns:
        int: number of occupied seats at the end of the seats system simulation
            for corresponding part.
    """

    final_layout = simulate_seat_system(seats_layout, part)

    count = 0
    for row in final_layout:
        for char in row:
            if char == '#':
                count += 1

    return count


if __name__ == "__main__":
    layout = parse_input_file(test=False)

    ans1 = final_n_occupied_seats(layout)
    print(ans1)

    ans2 = final_n_occupied_seats(layout, part = 2)
    print(ans2)