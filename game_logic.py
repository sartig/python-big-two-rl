from itertools import combinations
from typing import List, Optional

from classes import Playable
from constants import PLAYABLE_PRIORITY, RANK_PRIORITY, SUIT_PRIORITY
from utils import card_cmp, play_cmp


def get_pairs(deck: List[str]) -> List[Playable]:
    # assumes deck is sorted
    pairs = []
    for i in range(len(deck) - 1):
        for j in range(i + 1, len(deck)):
            if deck[i][0] == deck[j][0]:
                pairs.append(Playable(PLAYABLE_PRIORITY[1], [deck[i], deck[j]]))
    return pairs


def get_triplets(deck: List[str]) -> List[Playable]:
    # assumes deck is sorted
    triplets = []
    card_ranks = [card[0] for card in deck]
    rank_counts = [card_ranks.count(rank) for rank in RANK_PRIORITY]
    valid_ranks = [
        [rank, count] for rank, count in zip(RANK_PRIORITY, rank_counts) if count >= 3
    ]
    for rank, count in valid_ranks:
        if count == 3:
            triplets.append(
                Playable(
                    PLAYABLE_PRIORITY[2], [card for card in deck if card[0] == rank]
                )
            )
        else:  # count must be 4
            combs = combinations([card for card in deck if card[0] == rank], 3)
            for comb in combs:
                triplets.append(Playable(PLAYABLE_PRIORITY[2], list(comb)))
    return triplets


def get_straights(deck: List[str]) -> List[Playable]:
    # straights are in rank order, with 3 being lowest and 2 being highest. lowest = 3-4-5-6-7, highest = J-Q-K-A-2
    straights = []
    deck_ranks = sorted(
        list(set([card[0] for card in deck])), key=lambda x: RANK_PRIORITY.index(x)
    )
    straight_starting_ranks = []
    for i in range(len(deck_ranks) - 4):
        if RANK_PRIORITY.index(deck_ranks[i]) + 4 == RANK_PRIORITY.index(
            deck_ranks[i + 4]
        ):
            straight_starting_ranks.append(deck_ranks[i])
    for starting_rank in straight_starting_ranks:
        rank_index = RANK_PRIORITY.index(starting_rank)
        card1 = [card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index]
        card2 = [
            card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index + 1
        ]
        card3 = [
            card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index + 2
        ]
        card4 = [
            card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index + 3
        ]
        card5 = [
            card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index + 4
        ]

        # list comprehension reversed to preserve value order of straights (higher last card = better straight)
        straights.extend(
            [
                (
                    Playable(PLAYABLE_PRIORITY[7], [c1, c2, c3, c4, c5])
                    if c1[1] == c2[1] == c3[1] == c4[1] == c5[1]
                    else Playable(PLAYABLE_PRIORITY[3], [c1, c2, c3, c4, c5])
                )
                for c5 in card5
                for c4 in card4
                for c3 in card3
                for c2 in card2
                for c1 in card1
            ]
        )

    return straights


def get_flushes(deck: List[str]) -> List[Playable]:
    flushes = []
    # count suits, if any >=5 use combinations
    deck_suits = [card[1] for card in deck]
    valid_suits = [suit for suit in SUIT_PRIORITY if deck_suits.count(suit) >= 5]
    for suit in valid_suits:
        combs = combinations([card for card in deck if card[1] == suit], 5)
        for comb in combs:
            if RANK_PRIORITY.index(comb[0][0]) + 4 != RANK_PRIORITY.index(comb[4][0]):
                # skip straight flushes
                flushes.append(Playable(PLAYABLE_PRIORITY[4], list(comb)))

    return flushes


def get_full_houses(deck: List[str]) -> List[Playable]:
    full_houses = []
    deck_ranks = [card[0] for card in deck]

    # only care about ranks with 2 or more cards
    rank_counts = [
        [rank, deck_ranks.count(rank)]
        for rank in RANK_PRIORITY
        if deck_ranks.count(rank) >= 2
    ]
    for rank1, count1 in rank_counts:
        if count1 >= 3:
            for rank2 in rank_counts:
                if rank1 != rank2:
                    combs1 = list(
                        combinations([card for card in deck if card[0] == rank1], 3)
                    )
                    combs2 = list(
                        combinations([card for card in deck if card[0] == rank2], 2)
                    )
                    for comb1 in combs1:
                        for comb2 in combs2:
                            full_houses.append(
                                Playable(
                                    PLAYABLE_PRIORITY[5],
                                    # put triplet at end of list
                                    list(comb2) + list(comb1),
                                )
                            )
    return full_houses


def get_four_of_a_kinds(deck: List[str]) -> List[Playable]:
    four_of_a_kinds = []
    deck_ranks = [card[0] for card in deck]
    rank_counts = [[rank, deck_ranks.count(rank)] for rank in RANK_PRIORITY]
    for rank, count in rank_counts:
        if count == 4:
            for other_card in deck:
                if other_card[0] != rank:
                    four_of_a_kinds.append(
                        Playable(
                            PLAYABLE_PRIORITY[6],
                            [card for card in deck if card[0] == rank] + [other_card],
                        )
                    )

    return four_of_a_kinds


def get_five_card_hands(deck: List[str]) -> List[Playable]:
    five_card_hands = []

    # straights
    five_card_hands.extend(get_straights(deck))

    # flushes
    five_card_hands.extend(get_flushes(deck))

    # full houses
    five_card_hands.extend(get_full_houses(deck))

    # four of a kind plus any filler card
    five_card_hands.extend(get_four_of_a_kinds(deck))

    # straight flush handled in straight & flush functions

    return five_card_hands


def get_valid_plays(
    deck: List[str], previous_play: Optional[Playable] = None
) -> List[Playable]:
    # plays must have same number of cards as previous play
    if previous_play is not None:
        required_length = len(previous_play.cards)
        match required_length:
            case 1:
                return [
                    Playable(PLAYABLE_PRIORITY[0], [card])
                    for card in deck
                    if card_cmp(card, previous_play.cards[0]) > 0
                ]
            case 2:
                # identify pairs in hand that are higher than previous play
                pairs = get_pairs(deck)
                # pairs only compare the higher card of the two to determine which is higher
                # i.e. 7D + 7S beats 7C + 7H
                return [pair for pair in pairs if play_cmp(pair, previous_play) > 0]
            case 3:
                # identify triplets in hand that are higher than previous play
                triplets = get_triplets(deck)
                # cannot compare triplets of the same rank so just compare first card of each
                return [
                    triplet
                    for triplet in triplets
                    if play_cmp(triplet, previous_play) > 0
                ]
            case 5:
                fives = get_five_card_hands(deck)
                # identify 5-card combinations in hand that are higher than previous play
                # use separate comparator for 5-card combinations
                return [five for five in fives if play_cmp(five, previous_play) > 0]

        return []
    else:
        plays = []
        for card in deck:
            plays.append(Playable(PLAYABLE_PRIORITY[0], [card]))
        plays.extend(get_pairs(deck))
        plays.extend(get_triplets(deck))
        plays.extend(get_five_card_hands(deck))
        return plays
