from typing import List, Tuple

def parse_input_file() -> List[str]:
    input_path = "./input.txt"
    with open(input_path, "r") as file:
        lines = file.read().strip().split("\n")

    return lines


def count_trees_in_path(landscape: List[str], increments: Tuple[int]) -> int:
    """
    Count number of trees in the path given by increments

    Start at (0, 0), progress vertically by y=increments[0],
    and horizontally by x=increments[1].

    landscape contains rows of empty space '.' and trees '#', e.g.:
        X marks starting position ->["X.......#.............#........",
                                     "...#....#...#....#.............",
                                     ".#..#...#............#.....#..#",
                                     "..#......#..##............###..",
                                     "..........#......#..#..#......."]

    Args:
        landscape (List[str]): input of problem, example given above.
        increments (Tuple[int]): y, x increments to traverse the
            landscape downwards.

    Returns:
        int: number of trees ('#') in the path
    """
    H, W = len(landscape), len(landscape[0])
    position = (0, 0)
    count = 0
    while position[0] < H:
        if landscape[position[0]][position[1]] == '#':
            count += 1
        position = (position[0]+increments[0], (position[1]+increments[1]) % W)
    return count


def multiply_trees_in_paths(landscape: List[str], slopes_increments: List[tuple]) -> int:
    """Multiplies numbers of trees encountered through each of given slopes


    landscape contains rows of empty space '.' and trees '#', e.g.:
        X marks starting position ->[X.......#.............#........,
                                     ...#....#...#....#.............,
                                     .#..#...#............#.....#..#,
                                     ..#......#..##............###..,
                                     ..........#......#..#..#.......]

    Args:
        landscape (List[str]): input of problem, example given above.
            '#':tree, '.':space
        slopes_increments (List[tuple]): y, x increments to traverse the
            landscape downwards.

    Returns:
        int: product of trees encountered through each slopes.
    """
    prod = 1
    for increments in slopes_increments:
        prod *= count_trees_in_path(landscape, increments)
    return prod


if __name__ == "__main__":
    #
    # Part 1
    #
    landscape = parse_input_file()
    ans1 = count_trees_in_path(landscape, (1, 3))
    print(ans1)

    #
    # Part 2
    #
    slopes_increments = [(1, 1),
                         (1, 3),
                         (1, 5),
                         (1, 7),
                         (2, 1),]
    ans2 = multiply_trees_in_paths(landscape, slopes_increments)
    print(ans2)

