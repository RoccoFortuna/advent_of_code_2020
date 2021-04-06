from typing import Tuple, List
from tqdm import tqdm

def parse_input_file(test = 0):
    if test:
        with open(f"./d23_crab_cups/test_input{test}.txt", "r") as f:
            inp = f.readline()
    else:
        with open("./d23_crab_cups/input.txt", "r") as f:
            inp = f.readline()

    return [int(digit) for digit in inp]



class LLNode():
    def __init__(self, val: int):
        self.val = val
        self.next = None


class LLoop():
    def __init__(self, l: list):
        self.max = max(l)

        init_head = LLNode(l[0])

        # store reference to each node with val key
        self.nodes_lookup = {init_head.val: init_head}

        self.head = init_head
        self.curr_cup = self.head

        node = init_head
        for el in l[1:]:
            new_node = LLNode(el)
            node.next = new_node

            # store reference to each node
            self.nodes_lookup[el] = new_node

            # iterate to next node
            node = new_node

        # finally link last node with first to close Linked Loop
        node.next = init_head


    def __str__(self):
        node = self.head
        s = [str(node.val)] if self.curr_cup.val != node.val else ['(' + str(node.val) + ')']

        node = node.next
        while node.val != self.head.val:
            if node.val == self.curr_cup.val:
                s.append('(' + str(node.val) + ')')
            else:
                s.append(str(node.val))

            node = node.next

        return ' '.join(s)


    def make_move(self, k: int = 3):
        # detach nodes from Linked Loop
        removed_head, removed_tail = self.remove_nodes_clockwise(self.curr_cup, k)


        # save values in between as not targets
        non_targets = {removed_tail.val}
        removed_node = removed_head
        while removed_node.val != removed_tail.val:
            non_targets.add(removed_node.val)
            removed_node = removed_node.next

        # try targets (not in non_targets) until found
        target = (self.curr_cup.val - 1) % (self.max + 1)
        while self.nodes_lookup.get(target) is None or target in non_targets:
            # print(target)
            target = (target - 1) % (self.max + 1)


        self.insert_nodes_clockwise(self.nodes_lookup[target], removed_head, removed_tail)



    def insert_nodes_clockwise(self, target_node: LLNode, ins_head: LLNode, ins_tail: LLNode):
        ins_tail.next = target_node.next
        target_node.next = ins_head


    def remove_nodes_clockwise(self, curr_node: 'LLNode', k: int):
        """Remove k nodes clockwise from curr_node

        e.g.:
        linked loop:
        1 -> 4 -> 7 -> 9 -> 5 -> 2 ¬
        ^--------------------------+
        curr_node: LLNode(4)
        k = 3

        detached segment head becomes: LLNode(7) -> LLNode(9) -> LLNode(5) -> None
        new linked loop:

        Args:
            k (int): number of nodes to detach

        Returns:
            Tuple[LLNode, LLNode]: the head and tail of detached segment of nodes
        """
        detached_head = curr_node.next

        # find continuation of LLoop after detaching, k nodes further
        detached_tail = curr_node
        for _ in range(k):
            detached_tail = detached_tail.next

        # get continuation segment's head
        cont_head = detached_tail.next
        # remove last detached node's link to the continuation
        detached_tail.next = None

        # link curr_node to LinkedLoop new continuation
        curr_node.next = cont_head

        # return detached segment's head node
        return detached_head, detached_tail


def make_moves(labels: List[int], n: int = 100, k: int = 3) -> int:
    """
    Simulate n moves on labels, picking up k cups starting at index i

    For each move: remove k cups from circle at index i+1, then place them
    back in same order after cup with label

    Args:
        labels (List[int]): labels ordered
        n (int, optional): number of moves to perform on labels. Defaults to 100.
        k (int): number of cups to pick up

    Returns:
        int: product of two cups following cup 1.
    """
    # construct Linked Loop from labels
    lloop = LLoop(labels)
    for m in tqdm(range(1, n+1)): # perform n make_moves
        lloop.make_move()
        lloop.curr_cup = lloop.curr_cup.next

    one_node = lloop.nodes_lookup.get(1)
    return one_node.next.val * one_node.next.next.val




if __name__ == "__main__":
    labels = parse_input_file(test=0)
    ONE_MILLION = 1000000
    TEN_MILLION = 10000000

    n_moves = TEN_MILLION
    n_cups = ONE_MILLION

    labels2 = labels + list(range(max(labels)+1, n_cups +1))
    ans2 = make_moves(labels2, n_moves)

    print(ans2)




