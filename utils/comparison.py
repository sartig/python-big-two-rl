from functools import cmp_to_key
from typing import List

from classes.card_set import CardSet
from utils.constants import PLAYABLE_PRIORITY, RANK_PRIORITY, SUIT_PRIORITY


def card_cmp(card1: str, card2: str) -> int:
    """
    Compares two cards based on their ranks and suits.

    Args:
        card1 (str): The first card to compare.
        card2 (str): The second card to compare.

    Returns:
        int: 1 if card1 is greater than card2, -1 if card1 is less than card2, and 0 if they are equal.
    """
    if RANK_PRIORITY.index(card1[0]) > RANK_PRIORITY.index(card2[0]):
        return 1
    elif RANK_PRIORITY.index(card1[0]) < RANK_PRIORITY.index(card2[0]):
        return -1
    elif SUIT_PRIORITY.index(card1[1]) > SUIT_PRIORITY.index(card2[1]):
        return 1
    elif SUIT_PRIORITY.index(card1[1]) < SUIT_PRIORITY.index(card2[1]):
        return -1
    else:
        return 0


card_cmp_key = cmp_to_key(card_cmp)


def play_cmp(hand1: CardSet, hand2: CardSet) -> int:
    """
    Compares two CardSet objects based on their hand type and cards.

    Args:
        hand1 (CardSet): The first set of cards to compare.
        hand2 (CardSet): The second set of cards to compare.

    Returns:
        int: 1 if hand1 is greater than hand2, -1 if hand1 is less than hand2, and 0 if they are equal.
    """
    if PLAYABLE_PRIORITY.index(hand1.hand_type) > PLAYABLE_PRIORITY.index(
        hand2.hand_type
    ):
        return 1
    elif PLAYABLE_PRIORITY.index(hand1.hand_type) < PLAYABLE_PRIORITY.index(
        hand2.hand_type
    ):
        return -1
    else:
        if hand1.hand_type == PLAYABLE_PRIORITY[6]:
            # four-of-a-kind compare first card
            return card_cmp(hand1.cards[0], hand2.cards[0])
        else:
            # all other cases (single, pair, triplet, straight, flush, full house, straight flush) compare last card
            return card_cmp(hand1.cards[-1], hand2.cards[-1])


play_cmp_key = cmp_to_key(play_cmp)


def sort_cards(cards: List[str]) -> None:
    """
    Sorts a list of cards in place using the `card_cmp_key` function as the sorting key, from lowest to highest.

    Args:
        cards (List[str]): The list of cards to be sorted.

    Returns:
        None: This function sorts the list of cards in place and does not return anything.
    """
    cards.sort(key=card_cmp_key)
