from functools import cmp_to_key

from classes import Playable
from constants import PLAYABLE_PRIORITY, RANK_PRIORITY, SUIT_PRIORITY


def card_cmp(card1: str, card2: str) -> int:
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


def play_cmp(hand1: Playable, hand2: Playable) -> int:
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
