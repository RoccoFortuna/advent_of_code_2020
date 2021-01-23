from typing import List, Set

def parse_input_file() -> List[List[str]]:
    input_path = "./d6_custom_customs/input.txt"
    with open(input_path, "r") as file:
        groups_str = file.read().strip().split("\n\n")

    groups = []
    for group_str in groups_str:
        group = group_str.split('\n') # split each line of each group
        groups.append(group)

    return groups

def get_groups_ans_union_sum(groups: List[List[str]]) -> int:
    """Get the sum of lengths of the union of characters in each group

    Each group has a number of people, each person
    answered "yes" to a number of questions (different characters).
    Find the sum of numbers of positive answers in the union of
    answers given by people in each group, e.g.:
        The following test case:
            abc     (answer group 0, person 0)  sum: 3

            a       (answer group 1, person 0)
            b       (answer group 1, person 1)
            c       (answer group 1, person 2)  sum: 3

        returns 3+3 = 6

    Args:
        groups (List[List[str]]): positive asnwers given by each person,
            in each group

    Returns:
        int: sum of numbers of positive answers in each
            group's union of answers
    """
    ret = 0
    for group in groups:
        all_ans = []
        for el in group:
            all_ans.extend([char for char in el])
        ret += len(set(all_ans))
    return ret

def get_groups_ans_intersection_sum(groups: List[List[str]]) -> int:
    """Get the sum of lengths of the intersection of characters in each group

    Each group has a number of people, each person
    answered "yes" to a number of questions (different characters).
    Find the sum of numbers of positive answers in the intersection of
    answers given by people in each group, e.g.:
        The following test case:
            abc     (answer group 0, person 0)  sum: 3

            a       (answer group 1, person 0)  the intersection
            b       (answer group 1, person 1)  between {'a'}, {'b'}, {'c'} is empty
            c       (answer group 1, person 2)  sum: 0

        returns 3+0 = 3

    Args:
        groups (List[List[str]]): positive asnwers given by each person,
            in each group

    Returns:
        int: sum of numbers of positive answers in each
            group's intersection of answers
    """
    ret = 0
    for group in groups:
        print(f'group: {group}')
        ans_intersection = set([char for char in group[0]])
        for el in group[1:]:
            ans_intersection = ans_intersection.intersection(set([char for char in el]))


        print(f'ans_intersection: {ans_intersection}')
        ret += len(set(ans_intersection))
    return ret


if __name__ == "__main__":
    groups = parse_input_file()

    ans1 = get_groups_ans_union_sum(groups)
    print(ans1)

    ans2 = get_groups_ans_intersection_sum(groups)
    print(ans2)