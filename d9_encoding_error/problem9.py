from typing import List, Tuple
import d1_report_repair.problem1 as problem1

def parse_input_file():
    input_path = "./d9_encoding_error/input.txt"
    with open(input_path, "r") as file:
        lines = file.readlines()
    return [int(line) for line in lines if line]


def find_non_sum_of_prev(nums: List[int], prev: int = 25) -> int:
    """Find first number that is not a sum of any two prev numbers

    Given list of nums, find a number that is not the sum of
    any two of the prev number of immediately preceding numbers, e.g.:
        nums = [2, 3, 4, 7, 11, 12, 13]
        prev = 3
        then  7 = 3+4, ok
             11 = 7+4, ok
             12 = ???, !!
        Return 12 because no two numbers in [4, 7, 11] can be summed to yield 12.

    Args:
        nums (List[int]): list of numbers to check condition for.
        prev (int, optional): Number of preceding ints to consider from
            the nums list to find a pair that sums to current number. Defaults to 25.

    Returns:
        int: number that is not sum of any two prev numbers.
    """
    for idx in range(prev, len(nums)):
        if problem1.find_two_ints_summing_to(nums[idx-prev: idx], nums[idx]) is None:
            return nums[idx]


def find_contiguous_summing_to(nums: List[int], target: int) -> int:
    """
    Find sum of max and min values of contiguous subarray summing to target

    Given is a list of ints, find the contiguous subarray that
    sums to target int. Then return the sum between minimum and
    maximum values in the subarray.

    Args:
        nums (List[int]): numbers to find contiguous array in.
        target (int): number to sum up to.

    Returns:
        int: sum between min and max value in found subarray.
    """
    lo, hi = 0, 1 # pointers

    curr_sum = nums[lo] + nums[hi]

    while True:
        if curr_sum == target:  # target found
            break
        elif lo == hi or curr_sum < target: # if one element or curr_sum too small -> enlarge interval
            hi += 1
            curr_sum += nums[hi]

        elif curr_sum > target:     # curr_sum too big, shrink interval
            curr_sum -= nums[lo]    # remove from sum before increasing
            lo += 1

    min_val, max_val = min(nums[lo: hi+1]), max(nums[lo: hi+1])
    return min_val + max_val

if __name__ == "__main__":
    nums = parse_input_file()

    ans1 = find_non_sum_of_prev(nums)
    print(ans1)

    ans2 = find_contiguous_summing_to(nums, ans1)
    print(ans2)