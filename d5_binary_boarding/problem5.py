from typing import List

def parse_input_file() -> List[str]:
    input_path = "./d5_binary_boarding/input.txt"
    with open(input_path, "r") as file:
        lines = file.read().strip().split("\n")

    return lines

def binarize_bpass(bpass: str) -> str:
    """Turn boarding pass into binary number

    Args:
        bpass (str): made of chars with char in ['B', 'F', 'R', 'L']

    Returns:
        str: binarized string where 'B' and 'R' are converted to 1,
            'F', 'L' are converted to 0.
    """
    return ''.join([str(int(k in ['B', 'R'])) for k in bpass])

def find_max_bpass_id(bpasses: List[str]) -> int:
    """Given bpasses, returns max id

    bpass id is binary representation of bpass, where
    e.g. BFFFBBFRRR -> 100110111 because B,R->1 and F,L->0

    Args:
        bpasses (List[str]): contains bpasses of format e.g. BFFFBBFRRR
            of which max id must be found
    """
    max_bpass_id = float('-inf')
    for bpass in bpasses:
        bpass_id = int(binarize_bpass(bpass), 2)
        if bpass_id > max_bpass_id:
            max_bpass_id = bpass_id
    return max_bpass_id


def find_my_bpass_id(bpasses: List[str]) -> int:
    """Given bpasses, return id that is missing from contiguous list

    bpass id is binary representation of bpass, where
    e.g. BFFFBBFRRR -> 100110111 because B,R->1 and F,L->0

    Args:
        bpasses (List[str]): contains bpasses of format e.g. BFFFBBFRRR
            of which missing id must be found
    """
    found_ids = set()
    min_bpass_id = float('inf')
    max_bpass_id = float('-inf')

    for bpass in bpasses:
        bpass_id = int(binarize_bpass(bpass), 2)

        # update current lowest and highest ids, to know range of ids
        if bpass_id > max_bpass_id:
            max_bpass_id = bpass_id
        if bpass_id < min_bpass_id:
            min_bpass_id = bpass_id

        found_ids.add(bpass_id)

    # look for first missing bpass_id in range
    for bpass_id in range(min_bpass_id+1, max_bpass_id):
        if bpass_id not in found_ids:
            return bpass_id

    return 'my god, didnt find anything...'

if __name__ == "__main__":
    bpasses = parse_input_file()
    ans1 = find_max_bpass_id(bpasses)
    print(ans1)

    ans2 = find_my_bpass_id(bpasses)
    print(ans2)