from typing import List, Tuple

def parse_input_file() -> List[Tuple[str, int]]:
    input_path = "./d12_rain_risk/input.txt"
    with open(input_path, "r") as file:
        lines = file.read().splitlines()


    return [(line[0], int(line[1:])) for line in lines]


def exec_instr_part1(position: Tuple[int, int, int], instr: Tuple[str, int]) -> Tuple[int, int, int]:
    """
    Execute instruction from given position, return new position

    instructions:
        Action N means to move north by the given value.
        Action S means to move south by the given value.
        Action E means to move east by the given value.
        Action W means to move west by the given value.
        Action L means to turn left the given number of degrees.
        Action R means to turn right the given number of degrees.
        Action F means to move forward by the given value in the
            direction the ship is currently facing.

    Args:
        position (Tuple[int, int, int]): describes x, y positions ([0] and [1] resp.),
            as well as facing direction ([2]), where 0,1,2,3 facing direction
            values indicate East, South, West and North resp.
        instr (Tuple[str, int]): instruction type (in 'NSEWLRF') and instr value

    Returns:
        Tuple[int, int, int]: resulting position after executing instruction
    """
    instr_type, instr_val = instr
    x, y, direction = position

    # handle F before and modify instr_type based on direction
    if instr_type == "F":
        corr = {0:'E', 1:'S', 2:'W', 3:'N'} # map corresponding direction
        instr_type = corr[direction]

    if instr_type == "N":
        return (x, y+instr_val, direction)

    elif instr_type == "S":
        return (x, y-instr_val, direction)

    elif instr_type == "E":
        return (x+instr_val, y, direction)

    elif instr_type == "W":
        return (x-instr_val, y, direction)

    elif instr_type == "R":
        turning_val = instr_val//90
        new_direction = (direction + turning_val) % 4
        return (x, y, new_direction)

    elif instr_type == "L":
        turning_val = instr_val//90
        new_direction = (direction - turning_val) % 4
        return (x, y, new_direction)


def exec_instr_part2(position: Tuple[int, int], waypoint: Tuple[int, int], instr: Tuple[str, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Execute instruction from given position, return new position


        PART 2 instructions:
        Action N means to move the waypoint north by the given value.
        Action S means to move the waypoint south by the given value.
        Action E means to move the waypoint east by the given value.
        Action W means to move the waypoint west by the given value.
        Action L means to rotate the waypoint around the ship left
            (counter-clockwise) the given number of degrees.
        Action R means to rotate the waypoint around the ship right
            (clockwise) the given number of degrees.
        Action F means to move forward to the waypoint a number of
            times equal to the given value.

    Args:
        position (List[int]): describes x, y positions ([0] and [1] resp.),
            as well as facing direction ([2]), where 0,1,2,3 facing direction
            values indicate East, South, West and North resp.
        instr (Tuple[str, int]): instruction type (in 'NSEWLRF') and instr value
    """
    instr_type, instr_val = instr
    x, y = position
    wayp_x, wayp_y = waypoint

    if instr_type == "N":
        return position, (wayp_x, wayp_y+instr_val)

    elif instr_type == "S":
        return position, (wayp_x, wayp_y-instr_val)

    elif instr_type == "E":
        return position, (wayp_x+instr_val, wayp_y)

    elif instr_type == "W":
        return position, (wayp_x-instr_val, wayp_y)

    elif instr_type == "R":
        turning_val = (instr_val//90) % 4           # get number of times to turn
        # can turn right x times by turning left 4-x times
        waypoint = turn_left(waypoint, 4-turning_val)
        return position, waypoint

    elif instr_type == "L":
        turning_val = (instr_val//90) % 4           # get number of times to turn
        waypoint = turn_left(waypoint, turning_val)
        return position, waypoint

    elif instr_type == "F":
        return (x+instr_val*wayp_x, y+instr_val*wayp_y), waypoint



def turn_left(waypoint: Tuple[int], n: int) -> Tuple[int]:
    """Turns the waypoint counter-clockwise around 0, 0 n times

    Each turn corresponds to swapping x with y and inverting the new x

    e.g.:
        turn_right((2, 1), 3) -> 1: (-1, 2) -> 2: (-2, -1) -> 3: (1, -2)
        so output is (1, -2)

    Args:
        waypoint (Tuple[int]):
        turning_val (int): numer of times to turn left waypoint around (0, 0)
    """
    x, y = waypoint
    for _ in range(n):
        x, y = -y, x

    return x, y



def simulate_navigation(instructions: Tuple[str, int], part: int = 1) -> Tuple[int, int]:
    """
    Execute given set of instructions from initial position.

        PART 1 instructions:
        Action N means to move north by the given value.
        Action S means to move south by the given value.
        Action E means to move east by the given value.
        Action W means to move west by the given value.
        Action L means to turn left the given number of degrees.
        Action R means to turn right the given number of degrees.
        Action F means to move forward by the given value in the
            direction the ship is currently facing.

        PART 2 instructions:
        Action N means to move the waypoint north by the given value.
        Action S means to move the waypoint south by the given value.
        Action E means to move the waypoint east by the given value.
        Action W means to move the waypoint west by the given value.
        Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
        Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
        Action F means to move forward to the waypoint a number of times equal to the given value.

    Args:
        instructions (Tuple[str, int]): instr (Tuple[str, int]): instruction
            type (in ['N', 'S', 'E', 'W', 'L', 'R', 'F']) and instr value.

    Returns:
        Tuple[int, int]: final position after executing instructions
    """
    if part == 1:
        position = (0, 0, 0) # x, y and facing direction (0:east, 1:south, 2:west, 3:north)
        for instr in instructions:
            position = exec_instr_part1(position, instr)

    elif part == 2:
        position = (0, 0)   # init position (x, y)
        waypoint = (10, 1)       # init waypoint position (x, y)
        for instr in instructions:
            position, waypoint = exec_instr_part2(position, waypoint, instr)

    return position[:2]



if __name__ == "__main__":
    instructions = parse_input_file()

    position = simulate_navigation(instructions, part=1)
    ans1 = abs(position[0]) + abs(position[1])
    print(ans1)

    position2 = simulate_navigation(instructions, part=2)
    ans2 = abs(position2[0]) + abs(position2[1])
    print(ans2)
