from typing import List, Tuple, Union
import itertools

Line = List[str]
Plane = List[Line]
Space = List[Plane] # Space[z][y][x] is the indexing order, where yx is the initial plane
Hyperspace = List[Space] # Hyperspace[w][z][y][x] is the indexing order, where yx is the initial plane

def parse_input_file(test: bool = False) -> Space:
    if test:
        with open('./d17_conway_cubes/test_input.txt', 'r') as f:
            lines = f.read().splitlines()
    else:
        with open('./d17_conway_cubes/input.txt', 'r') as f:
            lines = f.read().splitlines()

    return [[[[char for char in line] for line in lines]]] # return 2D slice of 4D hyperspace


def get_empty_hyperspace(w_len, z_len, y_len, x_len) -> Space:
    return [[[['.' for _ in range(x_len)] for _ in range(y_len)] for _ in range(z_len)] for _ in range(w_len)]


def copy_extend_hypercube(hypercube: Hyperspace):
    w_len, z_len, y_len, x_len = len(hypercube), len(hypercube[0]), len(hypercube[0][0]), len(hypercube[0][0][0])

    # initialize empty cube, with additional entries at both sides of each dimension
    new_hypercube = get_empty_hyperspace(w_len+2, z_len+2, y_len+2, x_len+2) # initialize empty Space

    # copy existing values of original hypercube
    for w in range(w_len):
        for z in range(z_len):     # skip first entry of each
            for y in range(y_len): # dimension and stop
                for x in range(x_len): # one dimension before the end
                    new_hypercube[w+1][z+1][y+1][x+1] = hypercube[w][z][y][x]

    return new_hypercube

def get_hypercube_val(hypercube: Hyperspace, w:int, z: int, y: int, x: int) -> Union[str, None]:
    """
    Return cube value at coordinates z, y, x

    Args:
        hypercube (Hyperspace): hypercube to check for position value /validity
        w (int): w coordinate
        z (int): z coordinate
        y (int): y coordinate
        x (int): x coordinate

    Returns:
        Union[str, None]: '#' or '.' if position is valid, None otherwise.
    """
    w_len, z_len, y_len, x_len = len(hypercube), len(hypercube[0]), len(hypercube[0][0]), len(hypercube[0][0][0])
    if (0 <= w < w_len) and (0 <= z < z_len) and (0 <= y < y_len) and (0 <= x < x_len):
        return hypercube[w][z][y][x]
    # else return None is default




def expand_hypercube(hypercube: Hyperspace) -> Hyperspace:
    """Given a hypercube configuration, returns the next cycle configuration

    Next cycle is a hypercube with altered sub-cubes according to
        the following rules:
            - If a cube is active and exactly 2 or 3 of its neighbors
            are also active, the cube remains active. Otherwise,
            the cube becomes inactive.
            - If a cube is inactive but exactly 3 of its neighbors are
            active, the cube becomes active. Otherwise,
            the cube remains inactive.

    Args:
        hypercube (Hyperspace): current hypercube configuration

    Returns:
        Hyperspace: next cycle's configuration
    """
    w_len, z_len, y_len, x_len = len(hypercube), len(hypercube[0]), len(hypercube[0][0]), len(hypercube[0][0][0])

    new_hypercube = copy_extend_hypercube(hypercube)

    incr = [-1, 0, 1]
    wxyz_increments = set(itertools.product(incr, repeat=4))
    # remove null increment (0, 0, 0, 0), since we do not want
    # to count a space for its own activation
    wxyz_increments.remove((0, 0, 0, 0))

    # check for each new space
    for w in range(w_len+2):
        for z in range(z_len+2):
            for y in range(y_len+2):
                for x in range(x_len+2):
                    n_active_neighbors = 0
                    # count active subcubes at each increment
                    for incr in wxyz_increments:
                        w_incr, z_incr, y_incr, x_incr = incr
                        # get value at original cube of incremented position
                        hypercube_val = get_hypercube_val(hypercube, w+w_incr-1, z+z_incr-1, y+y_incr-1, x+x_incr-1)
                        if hypercube_val == '#':
                            n_active_neighbors += 1

                    # if active and condition met, deactivate
                    if new_hypercube[w][z][y][x] == '#' and n_active_neighbors not in [2, 3]:
                        new_hypercube[w][z][y][x] = '.'

                    # if inactive and condition met, activate
                    elif new_hypercube[w][z][y][x] == '.' and n_active_neighbors == 3:
                        new_hypercube[w][z][y][x] = '#'

    return strip_empty_hyperspace(new_hypercube)


def strip_empty_hyperspace(hypercube: Hyperspace) -> Hyperspace:
    """Given a cube, removes empty trailing dimensions

    Args:
        cube (Space): input space to trim trailing empty space from

    Returns:
        Space: input cubes without empty entries in any dimension
    """
    # get minimum and maximum id of filled space for each dimension
    min_w = min_z = min_y = min_x = float('inf')  # initialize mins
    max_w = max_z = max_y = max_x = float('-inf') # initialize maxs
    w_len, z_len, y_len, x_len = len(hypercube), len(hypercube[0]), len(hypercube[0][0]), len(hypercube[0][0][0])

    for w in range(w_len):
        for z in range(z_len):
            for y in range(y_len):
                for x in range(x_len):
                    if hypercube[w][z][y][x] == '#':
                        # update min coors
                        if w < min_w:
                            min_w = w
                        if z < min_z:
                            min_z = z
                        if y < min_y:
                            min_y = y
                        if x < min_x:
                            min_x = x
                        # update max coors
                        if w > max_w:
                            max_w = w
                        if z > max_z:
                            max_z = z
                        if y > max_y:
                            max_y = y
                        if x > max_x:
                            max_x = x

    # now trim space based on the max and min occurring active cubes
    # initialize empty cube
    new_w_len, new_z_len, new_y_len, new_x_len = max_w-min_w+1, max_z-min_z+1, max_y-min_y+1, max_x-min_x+1
    new_hypercube = get_empty_hyperspace(new_w_len, new_z_len, new_y_len, new_x_len)
    # copy from min to max of non empty region
    for w in range(new_w_len):
        for z in range(new_z_len):
            for y in range(new_y_len):
                for x in range(new_x_len):
                    new_hypercube[w][z][y][x] = hypercube[min_w+w][min_z+z][min_y+y][min_x+x]


    return new_hypercube

def print_hyperspace(hyperspace: Hyperspace):
    """Print space to log,
        '#': active
        '.': inactive
    Args:
        hyperspace (Hyperspace): Hyperspace to print
    """
    w_len, z_len, y_len, x_len = len(hyperspace), len(hyperspace[0]), len(hyperspace[0][0]), len(hyperspace[0][0][0])
    for w in range(w_len):
        for z in range(z_len):
            print(f"z={z-z_len//2}, w={w-w_len//2}")
            for y in range(y_len):
                print("".join(hyperspace[w][z][y]))
            print()


def perform_cycles(start_hypercube: Hyperspace, n: int) -> Hyperspace:
    """

    Args:
        start_cube (Hyperspace): [description]
        n (int): [description]

    Returns:
        Hyperspace: [description]
    """
    curr_hypercube = start_hypercube
    for _ in range(n):
        curr_hypercube = expand_hypercube(curr_hypercube)
        print_hyperspace(curr_hypercube)
    return curr_hypercube

def count_active_subcubes(hypercube: Hyperspace) -> int:
    w_len, z_len, y_len, x_len = len(hypercube), len(hypercube[0]), len(hypercube[0][0]), len(hypercube[0][0][0])
    n_active = 0
    for w in range(w_len):
        for z in range(z_len):
            for y in range(y_len):
                for x in range(x_len):
                    if hypercube[w][z][y][x] == '#':
                        n_active += 1

    return n_active



def get_active_hypercubes_at(inp_hypercube: Hyperspace, t: int = 6) -> int:
    """Given the conway cubes space, perform t cycles and count active cubes

    Args:
        inp_cube (Hyperspace): starting cubes configuration
        t (int, optional): Number of cycles to go through before counting
            final active cubes. Defaults to 6.

    Returns:
        int: final active cubes at the end of t cycles.
    """
    cube_at_t = perform_cycles(inp_hypercube, t)
    return count_active_subcubes(cube_at_t)

if __name__ == "__main__":
    inp_cube = parse_input_file()
    ans2 = get_active_hypercubes_at(inp_cube, t=6)
    print(ans2)

