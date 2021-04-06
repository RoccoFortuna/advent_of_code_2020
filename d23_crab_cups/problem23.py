from typing import Tuple
from tqdm import tqdm

def parse_input_file(test = 0):
    if test:
        with open(f"./d23_crab_cups/test_input{test}.txt", "r") as f:
            inp = f.readline()
    else:
        with open("./d23_crab_cups/input.txt", "r") as f:
            inp = f.readline()

    return [int(digit) for digit in inp]


def make_moves(labels: str, n: int = 100, k: int = 3, i: int = 0) -> str:
    """
    Simulate n moves on labels, picking up k cups starting at index i

    For each move: remove k cups from circle at index i+1, then place them
    back in same order after cup with label

    Args:
        labels (str):
        k (int): [description]
        n (int, optional): [description]. Defaults to 100.
        i (int, optional): [description]. Defaults to 0.

    Returns:
        str: [description]
    """
    for _ in tqdm(range(n)): # perform n make_moves
        curr_cup = labels[i]
        labels, i = make_move(labels, i, k, (min(labels), max(labels)))
        i = (labels.index(curr_cup) + 1) % len(labels)

    pos1 = labels.index(1)
    labels = [str(num) for num in labels]
    return f"{''.join(labels[pos1+1:] + labels[:pos1])}"


def make_move(labels, i: int, k: int, minmax: Tuple[int, int]) -> Tuple[str, int]:
    # find destination cup, initialize at curr_cup -1 (with wraparound)
    dest_cup = labels[i]
    dest_cup = dest_cup - 1 if dest_cup > minmax[0] else minmax[1]

    # get new labels removing k cups
    new_labels = labels[max(i + k - len(labels) + 1, 0):i+1] + labels[i+1+k:]
    removed = labels[i+1:i+1+k] + labels[:max(i + k - len(labels) + 1, 0)]

    # update index based on new cups config
    idx_offset = max(i + k - len(labels) + 1, 0)
    i = i + idx_offset % len(labels)

    dest_idx = None
    while True:
        try:
            dest_idx = new_labels.index(dest_cup)
            # if found, break loop, otherwise except and continue
            break
        except ValueError:
            dest_cup = dest_cup - 1 if dest_cup > minmax[0] else minmax[1]


    # update labels to include removed at new placing
    new_labels = new_labels[:dest_idx+1] + removed + new_labels[dest_idx+1:]

    return new_labels, i


if __name__ == "__main__":
    labels = parse_input_file(test=0)
    print(f"labels:")
    print(labels)

    ans1 = make_moves(labels, 100)
    print(ans1)

    #####################
    # This approach is way to slow to scale to part 2:
    labels = parse_input_file(test=0)
    ONE_MILLION = 1000000
    TEN_MILLION = 10000000

    n_moves = TEN_MILLION
    n_cups = ONE_MILLION

    labels2 = labels + list(range(max(labels)+1, n_cups +1))
    ans2 = make_moves(labels2, n_moves)



