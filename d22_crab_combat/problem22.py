from typing import List, Tuple, Deque, Set
from collections import deque
import copy

Deck = Deque[int]


def parse_input_file(test: int = 0) -> Tuple[List[int], List[int]]:
    if not test:
        with open('./d22_crab_combat/input.txt', 'r') as f:
            lines = f.read().strip()
    else:
        with open(f'./d22_crab_combat/test_input{test}.txt', 'r') as f:
            lines = f.read().strip()

    print(lines)
    p1_txt, p2_txt = lines.split("\n\n")


    p1 = [int(k) for k in p1_txt.strip().split("\n")[1:]]

    p2 = [int(k) for k in p2_txt.strip().split("\n")[1:]]

    return p1, p2


def simulate_combat_game(p1: Deck, p2: Deck) -> Tuple[Deck, Deck]:
    """Simulate 2-player game of Combat, give final decks' configuration.

    The game consists of a series of rounds: both players draw their top card,
    and the player with the higher-valued card wins the round. The winner keeps
    both cards, placing them on the bottom of their own deck so that the winner's
    card is above the other card. If this causes a player to have all of the
    cards, they win, and the game ends.

    Args:
        p1 (Deck): Player1's deck
        p2 (Deck): Player2's deck

    Returns:
        Tuple[Deck, Deck]: final decks of player1 and player2
    """

    while p1 and p2: # while both deques have elements
        top1, top2 = p1.popleft(), p2.popleft()
        assert top1 != top2, f"tops are equal: top1: {top1} == {top2} :top2\n{p1}\n{p2}"
        if top1 > top2:
            p1.append(top1)
            p1.append(top2)
        elif top2 > top1:
            p2.append(top2)
            p2.append(top1)

    return p1, p2


def simulate_recursive_combat_game(p1: Deck, p2: Deck, seen: Set[Tuple[Deck, Deck]]) -> Tuple[Deck, Deck]:
    """Simulate recursive combat game

    See simulate_combat_game for basic rules.
    In the recursive version, whenever the top card's values are at most the sizes
    of the players' decks, the winner of the round is the winner of the sub game where
    each player plays with their top card's value number of cards from the top of the deck.

    If the top cards' values are not both at most the sizes of the remaining deck, the round
    is determined as normal: highest top cards' valued player wins the round and puts their
    own card at the bottom of their deck, then puts the opponent's top card at the bottom.

    Whenever a deck is emptied from losing a card to the opponent due to losing a round,
    the (sub)game ends and the player with cards in the deck is the winner.

    Args:
        p1 (Deck): deque of integers, where p1.intersection(p2) is empty.
        p2 (Deck): deque of integers, where p2.intersection(p1) is empty.
        seen (Set[Tuple[Deck, Deck]]): decks' configurations already encountered in the (sub)game.
            This is necessary to end the (sub)game if it would loop.

    Returns:
        Tuple[Deck, Deck]: the end decks of Player1 and Player2.
    """
    # terminate if config already happened (-X-> infinite recursion)
    while p1 and p2: # while both deques have elements
        if (tuple(p1), tuple(p2)) in seen:
            return p1, None # returns p1 winning
        else:
            seen.add((tuple(p1), tuple(p2)))

        top1, top2 = p1.popleft(), p2.popleft()

        # if not enough cards, play as normal
        if top1 > len(p1) or top2 > len(p2):
            assert top1 != top2, f"Two tops were the same: {top1}"
            p1_winner = top1 > top2
        # else recurse
        else:
            # copy cards for each deck equal to top card's value
            p1_copy = deque(list(p1)[:top1])
            p2_copy = deque(list(p2)[:top2])
            final_sub_p1, final_sub_p2 = simulate_recursive_combat_game(p1_copy, p2_copy, set())
            p1_winner = len(final_sub_p1) > 0

        # update based on who won
        if p1_winner:
            p1.append(top1)
            p1.append(top2)
        else:
            p2.append(top2)
            p2.append(top1)

    return p1, p2



def compute_winning_score(p1: Deck, p2: Deck, recursive: bool = False) -> int:
    """Return winner's score of simulated game of Combat, given initial p1 and p2 decks


    Use Python's collections.deque datastructure to access and modify array at both sides
    efficiently.

    Args:
        p1 (Deck):
        p2 (Deck):

    Returns:
        int: score of winning player at the end of the simulated game of Combat
    """
    p1 = deque(p1)
    p2 = deque(p2)
    if recursive:
        p1, p2 = simulate_recursive_combat_game(p1, p2, set())
    else:
        p1, p2 = simulate_combat_game(p1, p2)
    winner_deck = p1 if p1 else p2
    print(winner_deck)
    score = 0
    for i, card in enumerate(winner_deck):
        score += (len(winner_deck)-i)*card

    return score


if __name__ == "__main__":
    p1, p2 = parse_input_file(test=0)

    ans1 = compute_winning_score(p1, p2)
    print(ans1)

    ans2 = compute_winning_score(p1, p2, recursive=True)
    print(ans2)