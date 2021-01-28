import re
from typing import List, Tuple, Dict, Set

Color = str

def parse_input_file():
    with open('./input.txt', 'r') as f:
        lines = f.read().strip().split('\n')

    clr_contains = {}
    for line in lines:
        a = line.split(" bags contain ")
        container_clr, second = line.split(" bags contain ")
        if not second[0].isnumeric():
            continue # skip entry if contains second="no other bags."

        second = second.strip('.').split(", ")

                        # clr: n
        contained_clr2n = {sec.split(' ', 1)[1].replace(' bags', '').replace(' bag', ''):int(sec.split(' ', 1)[0]) for sec in second}

        # store new color being contained
        clr_contains[container_clr] = contained_clr2n

    return clr_contains



def get_containable_colors(color: Color, containers_dict: Dict[Color, Dict[Color, int]], l: List[Color]) -> List[Color]:
    """Recursive DFS to get colors that can be contained by given starting color.

    Pruning could be implemented, therefore not efficient solution.

    Args:
        color (Color): color string, e.g. "shiny turquoise"
        containers_dict (Dict[Color, Dict[Color, int]]): mapping between a color
            and the colors it can directly contain with associated number of
            containable instances.
        l (List[Color]): contains colors encountered up to current recursive DFS step

    Returns:
        List[Color]: all colors reachable from initial color given containers_dict
    """
    if color not in containers_dict: # color considered does not have children -> useless
        return []

    for clr in containers_dict[color].keys(): # consider each of the children colors
        l.append(clr)

        # recurse to populate l
        get_containable_colors(clr, containers_dict, l)

    # return recursively populated list of colors reachable from starting color
    return l


def count_target_color_containers(containers_dict: Dict[Color, Dict[Color, int]], target: Color) -> int:
    """Count number of colors that can eventually contain target colored bag.

    containers_dict gives bag colors that can be contained within each color.
    Colored bags can contain other colored bags recursively, e.g.:
        shiny turquoise bags contain 5 dull purple bags
        and
        dull purple bags contain 3 faded cyan bags, 5 pale red bags,
        so shiny turquoise bags contain (15) faded cyan bags and (25) pale red bags.


    Args:
        containers_dict (Dict[Color, Dict[Color, int]]): bag colors that can be
        contained within each colored bag

        target (Color): target color to find number of bag colors that can contain it
            at some point

    Returns:
        int: number of bag colors that can eventually contain the target bag color
    """
    c = 0
    # loop through all colors
    for color in containers_dict.keys():
        # do not count target color as containing itself
        if color == target:
            continue
        # get entire list of colors that can be contained by current iteration color
        containables = get_containable_colors(color, containers_dict, [])
        # count as containing target if that's the case
        if target in containables:
            c += 1
    return c


def get_n_bags_contained_in(containers_dict: Dict[Color, Dict[Color, int]], curr_clr: Color, multiplier: int) -> int:
    """Count the total number of bags contained in input colored bag.

    Args:
        containers_dict (Dict[Color, Dict[Color, int]]): colors of bags contained
            in each colored bag, with associated number of containable instances
        curr_clr (Color): bag color at current recursive DFS step.
        multiplier (int): number of bags of the current color containable within
            first layer bag color.

    Returns:
        int: number of all bags that can be contained from top level
            bag color.
    """
    if curr_clr not in containers_dict:
        return 1 * multiplier # if no children, count bag itself

    # otherwise recurse
    return (sum([get_bags_contained_in(containers_dict, child_clr, mul) for child_clr, mul in container_contains[curr_clr].items()])+1) * multiplier



if __name__ == "__main__":
    container_contains = parse_input_file()
    target = "shiny gold"
    ans1 = count_target_color_containers(container_contains, target)
    print(ans1)

    ans2 = get_n_bags_contained_in(container_contains, target, 1) - 1 # minus 1 to not count the shiny bag
    print(ans2)
