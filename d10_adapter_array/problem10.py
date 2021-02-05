from collections import defaultdict
from typing import List, Dict

def parse_input_file():
    input_path = "./d10_adapter_array/input.txt"
    with open(input_path, "r") as file:
        lines = file.readlines()
    return [int(line) for line in lines if line]



def get_diff_distr(nums: List[int]) -> List[int]:
    """Get the distribution differences of pairs of subsequent nums in sorted input nums list

    Args:
        nums (List[int]): input integers, not sorted.

    Returns:
        List[int]: distribution of differences between subsequent nums pairs
    """
    sorted_nums = sorted(nums)
    distr = defaultdict(int)
    prev = 0
    for n in sorted_nums:
        distr[n-prev] += 1
        prev = n

    return distr


def get_adapter_combinations(nums: List[int]) -> int:
    """Get number of possible combinations of arrangements of nums

    Possible combinations feature no subsequent numbers with a difference
    greater than 3. Not all n in nums need to be used.

    Args:
        nums (List[int]): input numbers

    Returns:
        int: number of possible combinations of nums
    """
    sorted_nums = sorted(nums)

    # initialize dp
    dp = defaultdict(int)
    dp[0] = 1

    for n in sorted_nums:
        dp[n] = dp.get(n-1, 0) + dp.get(n-2, 0) + dp.get(n-3, 0)

    return dp[n]


if __name__ == "__main__":
    adapter_array = parse_input_file()
    ans1 = get_diff_distr(adapter_array)

    # +1 required as builtin joltage adapter is 3 higher than highest adapter
    print(ans1[1] * (ans1[3]+1))

    ans2 = get_adapter_combinations(adapter_array)
    print(ans2)