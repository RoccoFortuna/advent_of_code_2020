from typing import List, Set, Tuple
from tqdm import tqdm

def parse_input_file(test = 0) -> List[List[str]]:
    if test:
        with open(f"./d24_lobby_layout/test_input{test}.txt", "r") as f:
            lines = f.read().splitlines()
    else:
        with open("./d24_lobby_layout/input.txt", "r") as f:
            lines = f.read().splitlines()

    def parse_line(line: List[str]):
        # construct directions line
        l = []
        i = 0
        while i < len(line):
            composed_directions = {"ne", "nw", "se", "sw"}
            if line[i:i+2] in composed_directions:
                l.append(line[i:i+2])
                i += 2

            else:
                l.append(line[i])
                i += 1
        return l

    ll = []
    for l in lines:
        ll.append(parse_line(l))

    return ll # list of parsed directions with elements in ["e", "w", "ne", "se", "nw", "sw"]


def get_black_tiles(directions_list: List[List[str]]) -> Set[Tuple[int, float]]:
    """Get initial black tiles' configuration

    Args:
        directions_list (List[List[str]]): [description]

    Returns:
        [type]: [description]
    """
    black_tiles = set() # 2D coors (x, y)

    direction2incr = {"e": (1, 0), "w": (-1, 0),\
        "ne": (0.5, 1), "sw": (-0.5, -1), "nw": (-0.5, 1), "se": (0.5, -1)}

    for directions in directions_list:
        coors = (0, 0)
        for d in directions:
            incr = direction2incr[d]
            coors = tuple(p + q for p, q in zip(coors, incr))

        # swap tiles' color
        if coors in black_tiles:
            black_tiles.remove(coors)
        else:
            black_tiles.add(coors)

    return black_tiles


def count_black_neighbors(black_tiles: Set[Tuple[int, int]],
    ref_tile: Tuple[int, int], neighboring_whites: Set[Tuple[int, int]] = None) -> int:
    """Count black tiles neighbors to reference hex tile

    Args:
        black_tiles (Set[Tuple[int, int]]): set of coordinates denoting black tiles
        ref_tile (Tuple[int, int]): tile being considered. Find number of
            its black neighboring tiles.
        neighboring_whites (Set[Tuple[int, int]], optional): set of neighboring tiles.
            Defaults to None.

    Returns:
        int: number of black neighboring tiles.
    """

    direction2incr = {"e": (1, 0), "w": (-1, 0),\
        "ne": (0.5, 1), "sw": (-0.5, -1), "nw": (-0.5, 1), "se": (0.5, -1)}

    # count neighbors of black to know if it's still black
    n_black_neighbors = 0
    for incr in direction2incr.values():
        neighbor = tuple(p+q for p, q in zip(ref_tile, incr))
        if neighbor in black_tiles:
            n_black_neighbors += 1
        # store white neighboring tiles to later find out if they turn black
        elif neighboring_whites is not None:
            neighboring_whites.add(neighbor)

    return n_black_neighbors



def simulate_gol_turn(black_tiles: Set[Tuple[int, int]]):
    """Simulate hex version of game of life.

    Each turn, tiles are all flipped according to the following rules:
    - Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
    - Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.

    Args:
        black_tiles (Set[Tuple[int, int]]): previous turn's black tiles
    """
    new_blacks = set()
    neighboring_whites = set()
    for bt in black_tiles:
        n_black_neighbors = count_black_neighbors(black_tiles, bt, neighboring_whites)
        # print(f"n black neighbors: {n_black_neighbors}")
        # keep only black tiles with 1 or 2 neighbors
        if n_black_neighbors in [1, 2]:
            new_blacks.add(bt)

    # check which of the neighboring white tiles turns black
    for wt in neighboring_whites:
        n_black_neighbors = count_black_neighbors(black_tiles, wt)
        if n_black_neighbors == 2:
            new_blacks.add(wt)
    return new_blacks


def game_of_life_hex(black_tiles: Set[Tuple[int, int]], n=100) -> Set[Tuple[int, int]]:
    """
    Simulate game of life in hex tiling

    perform n days of game of life in a hex perfect tiling extending infinitely
    in all directions, where all tiles are initially white but the tiles
    at coordinates in black_tiles input Set.

    Args:
        black_tiles (Set[Tuple[int, int]]): coordinates of black tiles.
        n (int, optional): number of days to simulate in game of life.
            Defaults to 100.

    Returns:
        Set[Tuple[int, int]]: black tiles at the end of game of life
            simulation of n days.
    """
    # for _ in tqdm(range(n)):
    for i in range(n+1):
        if i%10 == 0:
            print(f"{i}: {len(black_tiles)}")
        # print(len(black_tiles))
        black_tiles = simulate_gol_turn(black_tiles)
    return black_tiles


if __name__ == "__main__":
    directions_list = parse_input_file(test=0)

    init_black_tiles = get_black_tiles(directions_list)
    ans1 = len(init_black_tiles)
    # print(ans1)

    black_tiles_100 = game_of_life_hex(init_black_tiles, 100)
    ans2 = len(black_tiles_100)
