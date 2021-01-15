from typing import List

"""
Find two ints in input that sum up to 2020. Return their product.
"""


def parse_input_file() -> List[int]:
    """Parse input ints

    Returns:
        List[int]: input ints
    """
    input_path = "./input.txt"
    with open(input_path, "r") as file:
        input_list = [int(k) for k in file.read().strip().split("\n")]
    return input_list



def find_two_ints_summing_to(l: List[int], total: int) -> int:
    """Find two ints in list that sum to total

    Args:
        l (list): positive integers
        total (int): total to sum up two integers in l to

    Returns:
        int: product of the two integers that sum up to total
    """
    found_numbers = set()
    for n in l:
        if total - n in found_numbers:
            return (total - n) * n

        found_numbers.add(n)




def find_three_ints_summing_to(l: List[int], total: int) -> int:
    """Find three ints in list that sum to total

    Time complexity: O(n**2): iterate through all elements, compute
        difference with each element
    Space complexity: O(n**2): for each element, store
        difference with each element

    Args:
        l (list): positive integers
        total (int): total to sum up three integers in l to

    Returns:
        int: product of the three integers that sum up to total
    """
    seen = set()

    for i in range(len(l)):
        for j in range(i+1, len(l)):
            num1 = l[i]
            num2 = l[j]
            target = total - num1 - num2
            if target in seen:
                return target * num1 * num2
            seen.add(num2)
            seen.add(num1)


if __name__ == "__main__":
    input_list = parse_input_file()

    ans1 = find_two_ints_summing_to(input_list, 2020)
    print(f'Answer to part1: {ans1}')

    ans2 = find_three_ints_summing_to(input_list, 2020)
    print(f'Answer to part2: {ans2}')


