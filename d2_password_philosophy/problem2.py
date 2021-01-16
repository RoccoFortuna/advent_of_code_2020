from typing import List, Tuple

def parse_input_file() -> List[Tuple[int, int, str, str]]:
    input_path = "./input.txt"
    with open(input_path, "r") as file:
        lines = [k for k in file.read().strip().split("\n")]

    test_cases = []
    for line in lines:
        occ_range, char, s = line.split()
        # clean elements: lo-hi -> range(lo, hi+1), char: -> char, s is clean already
        lo, hi = occ_range.split('-')
        char = char[0]
        test_cases.append((int(lo), int(hi), char, s))
    return test_cases



def validate_passwords_part1(test_cases: List[tuple]) -> int:
    """Given policies and passwords, returns number of valid passwords

    Args:
        test_cases (List[tuple]): test cases containing lo, and hi values for range
            the character of which occurrences must be within the range, and the
            string for which to check the condition is met.

    Returns:
        int: number of test cases for which the string meets the validity
            condition
    """
    count = 0
    for test_case in test_cases:
        if test_case_passes_part1(test_case):
            count += 1

    return count

def test_case_passes_part1(test_case: Tuple[int, int, str, str]) -> bool:
    """Given test case, determines if it's passed for part1

    A part1 test case needs to check if a character char in the string s is
    present c times, where c is within the given range(lo, hi)

    Args:
        test_case (Tuple[int, int, str, str]): (lo, hi, char, s)

    Returns:
        bool: true if condition is met, false otherwise. That is,
            True if char appears in s n times where lo <= n <= hi.
    """
    # count occurrences of char
    lo, hi, char, s = test_case # unpack test case
    c = s.count(char)                # count occurrences
    return c in range(lo, hi+1)      # check if count is in range (inclusive)


def validate_passwords_part2(test_cases: List[tuple]) -> int:
    """Given policies and passwords, returns number of valid passwords

    Args:
        test_cases (List[tuple]): test cases containing 1-indexed indices,
            the character that must be at EXACTLY one of the positions,
            and the string for which to check the condition is met.

    Returns:
        int: number of test cases for which the string meets the validity
            condition
    """
    count = 0
    for test_case in test_cases:
        if test_case_passes_part2(test_case):
            count += 1

    return count


def test_case_passes_part2(test_case: Tuple[int, int, str, str]) -> bool:
    """Given test case, determines if it's passed

    A part2 test case needs to check if a character char in the string s is
    present exactly at ONE of the two indices

    Args:
        test_case (Tuple[int, int, str, str]): (lo, hi, char, s)

    Returns:
        bool: true if condition is met, false otherwise. That is,
            returns whether char appears in s either lo or hi times.
    """
    # count occurrences of char
    lo, hi, char, s = test_case                 # unpack test case
    return (s[lo-1] == char) ^ (s[hi-1] == char)# use exclusive OR (^) to ensure EXACTLY one

if __name__ == "__main__":
    test_cases = parse_input_file()

    ans1 = validate_passwords_part1(test_cases)
    print(ans1)

    ans2 = validate_passwords_part2(test_cases)
    print(ans2)