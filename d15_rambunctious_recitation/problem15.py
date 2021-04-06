from typing import List

def parse_input_file(test: bool = False):
    if test:
        with open("d15_rambunctious_recitation/test_input.txt", 'r') as file:
            nums = [int(n) for n in file.readline().split(",")]
    else:
        with open("d15_rambunctious_recitation/input.txt", 'r') as file:
            nums = [int(n) for n in file.readline().split(",")]

    return nums


def find_nth_number_spoken(nums: List[int], n: int = 2020) -> int:
    """Find nth number in memory game with following rules

    Rules:
        If that was the first time the number has been spoken,
            the current player says 0.
        Otherwise, the number had been spoken before; the current
            player announces how many turns apart the number is from
            when it was previously spoken.

    Args:
        n (int, optional): position of number in sequence of numbers
        resulting from given rules. Defaults to 2020.

    Returns:
        int: number at nth position in sequence resulting from memory game
            following given rules
    """
    last_occ = {val: i for i, val in enumerate(nums[:-1])} # value: last occurrence

    last_spoken = nums[-1]
    for turn in range(len(last_occ), n-1): # or n+1?
        if last_spoken not in last_occ:
            new_num = 0
        else: # if not the first occurrence
            new_num = turn - last_occ[last_spoken]

        last_occ[last_spoken] = turn
        last_spoken = new_num
        # turns_nums.append(new_num)

    return last_spoken


if __name__ == "__main__":
    nums = parse_input_file(test=False)

    ans1 = find_nth_number_spoken(nums, n=2020)
    print(ans1)

    ans2 = find_nth_number_spoken(nums, n=30000000)
    print(ans2)