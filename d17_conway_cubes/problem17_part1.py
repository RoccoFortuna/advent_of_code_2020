from typing import List, Tuple, Union
import itertools


Plane = List[List[str]]
Space = List[Plane] # Space[z][y][x] is the indexing order, where yx is the initial plane


def parse_input_file(test: bool = False) -> Space:
    if test:
        with open('./d17_conway_cubes/test_input.txt', 'r') as f:
            lines = f.read().splitlines()
    else:
        with open('./d17_conway_cubes/input.txt', 'r') as f:
            lines = f.read().splitlines()

    return [[[char for char in line] for line in lines]]


def get_empty_space(z_len, y_len, x_len) -> Space:
    # return [[['.']*x_len]*y_len]*z_len # Does NOT work because mutable objects shallow-copied
    return [[['.' for _ in range(x_len)] for _ in range(y_len)] for _ in range(z_len)]


def copy_extend_cube(cube: Space):
    z_len, y_len, x_len = (len(cube), len(cube[0]), len(cube[0][0]))
    # initialize empty cube, with additional entries at both sides of each dimension
    new_cube = get_empty_space(z_len+2, y_len+2, x_len+2) # initialize empty Space

    # copy existing values of original cube
    for z in range(z_len):     # skip first entry of each
        for y in range(y_len): # dimension and stop
            for x in range(x_len): # one dimension before the end
                new_cube[z+1][y+1][x+1] = cube[z][y][x]

    return new_cube

def get_cube_val(cube: Space, z: int, y: int, x: int) -> Union[str, None]:
    """
    Return cube value at coordinates z, y, x

    Args:
        cube (Space):
        z (int): z coordinate
        y (int): y coordinate
        x (int): x coordinate

    Returns:
        Union[str, None]: '#' or '.' if position is valid, None otherwise.
    """
    z_len, y_len, x_len = (len(cube), len(cube[0]), len(cube[0][0]))
    if (0 <= z < z_len) and (0 <= y < y_len) and (0 <= x < x_len):
        return cube[z][y][x]

    # else return None is default

# def strip_empty_space(cube: Space) -> Space:



def expand_cube(cube: Space) -> Space:
    """Given a cube configuration, returns the next cycle configuration

    Next cycle is a cube with altered sub-cubes according to
        the following rules:
            - If a cube is active and exactly 2 or 3 of its neighbors
            are also active, the cube remains active. Otherwise,
            the cube becomes inactive.
            - If a cube is inactive but exactly 3 of its neighbors are
            active, the cube becomes active. Otherwise,
            the cube remains inactive.

    Args:
        cube (Space): current cube configuration

    Returns:
        Space: next cycle's configuration
    """
    z_len, y_len, x_len = (len(cube), len(cube[0]), len(cube[0][0]))
    new_cube = copy_extend_cube(cube)

    incr = [-1, 0, 1]
    xyz_increments = set(itertools.product(incr, repeat=3))
    # remove null increment (0, 0, 0), since we do not want
    # to count a space for its own activation
    xyz_increments.remove((0, 0, 0))

    # check for each new space
    for z in range(z_len+2):
        for y in range(y_len+2):
            for x in range(x_len+2):
                n_active_neighbors = 0
                # count active subcubes at each increment
                for incr in xyz_increments:
                    z_incr, y_incr, x_incr = incr
                    # get value at original cube of incremented position
                    cube_val = get_cube_val(cube, z+z_incr-1, y+y_incr-1, x+x_incr-1)
                    if cube_val == '#':
                        n_active_neighbors += 1

                # if active and condition met, deactivate
                if new_cube[z][y][x] == '#' and n_active_neighbors not in [2, 3]:
                    new_cube[z][y][x] = '.'

                # if inactive and condition met, activate
                elif new_cube[z][y][x] == '.' and n_active_neighbors == 3:
                    new_cube[z][y][x] = '#'

    return strip_empty_space(new_cube)


def strip_empty_space(cube: Space) -> Space:
    """Given a cube, removes empty trailing dimensions

    Args:
        cube (Space): input space to trim trailing empty space from

    Returns:
        Space: input cubes without empty entries in any dimension
    """
    # get minimum and maximum id of filled space for each dimension
    min_z = min_y = min_x = float('inf')  # initialize mins
    max_z = max_y = max_x = float('-inf') # initialize maxs
    z_len, y_len, x_len = (len(cube), len(cube[0]), len(cube[0][0]))

    for z in range(z_len):
        for y in range(y_len):
            for x in range(x_len):
                if cube[z][y][x] == '#':
                    # see if coors need updating
                    if z < min_z:
                        min_z = z
                    if y < min_y:
                        min_y = y
                    if x < min_x:
                        min_x = x
                    if z > max_z:
                        max_z = z
                    if y > max_y:
                        max_y = y
                    if x > max_x:
                        max_x = x

    # now trim space based on the max and min occurring active cubes
    # initialize empty cube
    new_z_len, new_y_len, new_x_len = max_z-min_z+1, max_y-min_y+1, max_x-min_x+1
    new_cube = [[['.' for _ in range(new_x_len)] for _ in range(new_y_len)] for _ in range(new_z_len)]
    # copy from min to max of non empty region
    for z in range(new_z_len):
        for y in range(new_y_len):
            for x in range(new_x_len):
                new_cube[z][y][x] = cube[min_z+z][min_y+y][min_x+x]


    return new_cube

def print_space(space: Space):
    """Print space to log,
        '#': active
        '.': inactive
    Args:
        space (Space): space to print
    """
    z_len, y_len, x_len = len(space), len(space[0]), len(space[0][0])
    for z in range(z_len):
        print(f"z={z-z_len//2}")
        for y in range(y_len):
            print("".join(space[z][y]))
        print()


def perform_cycles(start_cube: Space, n: int) -> Space:
    """

    Args:
        start_cube (Space): [description]
        n (int): [description]

    Returns:
        Space: [description]
    """
    curr_cube = start_cube
    for _ in range(n):
        curr_cube = expand_cube(curr_cube)
        print_space(curr_cube)
    return curr_cube

def count_active_subcubes(cube: Space) -> int:
    z_len, y_len, x_len = (len(cube), len(cube[0]), len(cube[0][0]))
    n_active = 0
    for z in range(z_len):
        for y in range(y_len):
            for x in range(x_len):
                if cube[z][y][x] == '#':
                    n_active += 1

    return n_active



def get_active_cubes_at(inp_cube: Space, t: int = 6) -> int:
    """Given the conway cubes space, perform t cycles and count active cubes

    Args:
        inp_cube (Space): starting cubes configuration
        t (int, optional): Number of cycles to go through before counting
            final active cubes. Defaults to 6.

    Returns:
        int: final active cubes at the end of t cycles.
    """
    cube_at_t = perform_cycles(inp_cube, t)
    return count_active_subcubes(cube_at_t)

if __name__ == "__main__":
    inp_cube = parse_input_file(test=True)
    ans1 = get_active_cubes_at(inp_cube, t=6)
    print(ans1)

