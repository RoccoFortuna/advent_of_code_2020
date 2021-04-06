from typing import List, Tuple, Set


def parse_input_file(test: int = 0):
    if not test:
        with open('./d21_allergen_assessment/input.txt', 'r') as f:
            lines = f.read().strip().split("\n")
    else:
        with open(f'./d21_allergen_assessment/test_input{test}.txt', 'r') as f:
            lines = f.read().strip().split("\n")

    food2allergens = []
    for line in lines:
        ingrs, allergens = line.split(" (contains ")
        ingrs = ingrs.split()
        allergens = allergens.strip(')').split(", ")
        food2allergens.append((ingrs, allergens))

    return food2allergens



def get_allergens_ingrs_universe(food2allergens: List[Tuple[List[str], List[str]]]) -> Tuple[List[str], List[str]]:
    """Get all ingrs and allergens from tuples with foods and allergens contained

    Given a list of all foods with respective allergens, constructs all possible
    ingredients and all possible allergens.

    Args:
        food2allergens (List[Tuple[List[str], List[str]]]): pairs of food (as list
            of ingredients) and contained allergens

    Returns:
        Tuple[List[str], List[str]]: all allergens and all ingredients
    """
    all_allergens = set()
    all_ingrs = set()
    for ingrs, allergens in food2allergens:
        all_allergens = all_allergens.union(set(allergens))
        all_ingrs = all_ingrs.union(set(ingrs))

    return all_allergens, all_ingrs


def find_allergens(food2allergens: List[Tuple[List[str], List[str]]]) -> Set[str]:
    """Find all ingrs with certainly no allergenics

    Each allergen belongs to one and only one ingredient.

    ### Find allergenic ingredients:
    Initialize all allergens with all possible ingredients,
    For every line, intersect each allergen's set of ingredients with the line's ingrs

    Then whenever the set of possible ingredients containing each allergen, set-differenced
    with the ingredients surely containing an allergen, is of size 1,
        the only ingredient possibly containing the allergen must be the one.
        Update the set of ingrs surely containing an allergen and go on.

    End when an entire loop through the ingredients yields no new allergenic ingredient

    ### Get non-allergenic ingredients:
    Set difference all_ingredients with allergenic ingredients to get
    non-allergenic ingredients.

    Args:
        food2allergens (List[Tuple[List[str], List[str]]]): pairs of food (as list
            of ingredients) and contained allergens

    Returns:
        int: number of occurrences of ingredients with surely no allergens
    """
    # get universe of allergens
    all_allergens, all_ingrs = get_allergens_ingrs_universe(food2allergens)

    # initialize allergens' possibly contining ingredient
    allergen2ingrs = {allergen: all_ingrs.copy() for allergen in all_allergens}
    # intersect with each other allergens list of each ingr occurring
    for food, allergens in food2allergens:
        for allergen in allergens:
            allergen2ingrs[allergen] = allergen2ingrs[allergen].intersection(set(food))

    # Get all ingredients without allergens:
    # iterate over allergens and remove iteratively all allergens
    # with only one possible ingredient

    # store tuples of pairs (ingredient, its allergen)
    ingr2allergen = []
    allergenic_ingrs = set()
    # iterate until non_allergenic_ingrs has not changed since iteration before
    new_allergenic_found = True
    while new_allergenic_found:
        new_allergenic_found = False
        for allergen in all_allergens:
            # get possible ingredients having this allergen
            possible_allergen_ingrs = allergen2ingrs[allergen].difference(allergenic_ingrs)
            if len(possible_allergen_ingrs) == 1:
                ingr, = possible_allergen_ingrs
                allergenic_ingrs.add(ingr)
                new_allergenic_found = True

                ingr2allergen.append((ingr, allergen))

    non_allergenic_ingrs = all_ingrs.difference(allergenic_ingrs)
    return non_allergenic_ingrs, ingr2allergen

def get_n_nonallergens(food2allergens: List[Tuple[List[str], List[str]]]) -> int:
    """Find total n of occurrences of ingrs with certainly no allergenics


    Args:
        food2allergens (List[Tuple[List[str], List[str]]]): pairs of food (as list
            of ingredients) and contained allergens

    Returns:
        int: number of occurrences in foods of ingredients with surely no allergens
    """
    non_allergenic_ingrs = find_allergens(food2allergens)[0]
    # count occurrences of ingredients without allergens
    count = 0
    for food, _ in food2allergens:
        for ingr in food:
            if ingr in non_allergenic_ingrs:
                count += 1
    return count


def get_canonical_dangerous_ingredient_list(food2allergens: List[Tuple[List[str], List[str]]]) -> str:
    ingr2allergen = find_allergens(food2allergens)[1]
    # sort ingredients alphabetically by their allergen
    sorted_ingrs = sorted(ingr2allergen, key=lambda x: x[1])

    s = ','.join([ingr for ingr, _ in sorted_ingrs])
    return s



if __name__ == "__main__":
    food2allergens = parse_input_file(test=0)

    ans1 = get_n_nonallergens(food2allergens)
    print(ans1)

    ans2 = get_canonical_dangerous_ingredient_list(food2allergens)
    print(ans2)