import random
from functools import cmp_to_key
from itertools import combinations

RANK_PRIORITY = "3456789tjqka2"
SUIT_PRIORITY = "dchs"
PLAYABLE_PRIORITY = [
    "single",
    "pair",
    "triplet",
    "straight",
    "flush",
    "fullhouse",
    "fourofakind",
    "straightflush",
]
PLAYER_COUNT = 4


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


def play_cmp(hand1: list[str, list[str]], hand2: list[str, list[str]]) -> int:
    if PLAYABLE_PRIORITY.index(hand1[0]) > PLAYABLE_PRIORITY.index(hand2[0]):
        return 1
    elif PLAYABLE_PRIORITY.index(hand1[0]) < PLAYABLE_PRIORITY.index(hand2[0]):
        return -1
    else:
        if hand1[0] == PLAYABLE_PRIORITY[6]:
            # four-of-a-kind compare first card
            return card_cmp(hand1[1][0], hand2[1][0])
        else:
            # all other cases (single, pair, triplet, straight, flush, full house, straight flush) compare last card
            return card_cmp(hand1[1][-1], hand2[1][-1])


play_cmp_key = cmp_to_key(play_cmp)


def sort_deck(deck: list[str]) -> None:
    deck.sort(key=card_cmp_key)


def get_pairs(deck: list[str]) -> list[str, list[str]]:
    # assumes deck is sorted
    pairs = []
    for i in range(len(deck) - 1):
        for j in range(i + 1, len(deck)):
            if deck[i][0] == deck[j][0]:
                pairs.append([PLAYABLE_PRIORITY[1], [deck[i], deck[j]]])
    return pairs


def get_triplets(deck: list[str]) -> list[str, list[str]]:
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
                [PLAYABLE_PRIORITY[2], [card for card in deck if card[0] == rank]]
            )
        else:  # count must be 4
            combs = combinations([card for card in deck if card[0] == rank], 3)
            for comb in combs:
                triplets.append([PLAYABLE_PRIORITY[2], list(comb)])
    return triplets


def get_straights(deck: list[str]) -> list[str, list[str]]:
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
                    [PLAYABLE_PRIORITY[7], [c1, c2, c3, c4, c5]]
                    if c1[1] == c2[1] == c3[1] == c4[1] == c5[1]
                    else [PLAYABLE_PRIORITY[3], [c1, c2, c3, c4, c5]]
                )
                for c5 in card5
                for c4 in card4
                for c3 in card3
                for c2 in card2
                for c1 in card1
            ]
        )

    return straights


def get_flushes(deck: list[str]) -> list[str, list[str]]:
    flushes = []
    # count suits, if any >=5 use combinations
    deck_suits = [card[1] for card in deck]
    suit_counts = [[suit, deck_suits.count(suit)] for suit in SUIT_PRIORITY]
    for suit, suit_count in suit_counts:
        if suit_count >= 5:
            combs = combinations([card for card in deck if card[1] == suit], 5)
            for comb in combs:
                if RANK_PRIORITY.index(comb[0][0]) + 4 != RANK_PRIORITY.index(
                    comb[4][0]
                ):
                    # skip straight flushes
                    flushes.append([PLAYABLE_PRIORITY[4], list(comb)])

    return flushes


def get_five_card_hands(deck: list[str]) -> list[str, list[str]]:
    five_card_hands = []
    # five card hands, in priority order:
    # straights
    five_card_hands.extend(get_straights(deck))

    # flushes
    five_card_hands.extend(get_flushes(deck))

    # full house
    # count ranks, if any >= 3 use combinations with any >= 2
    # order displayed is pair first, then triplet (for easier comparison)
    # four of a kind plus any filler card
    # count ranks, if any == 4 use with every other card
    # order displayed is 4 of a kind first, then filler
    # straight flush
    # combine straight and flush?
    # should get automatically added by get_straights and get_flushes

    return five_card_hands


def get_valid_plays(
    deck: list[str], previous_play: list[str, list[str]] = None
) -> list[str, list[str]]:
    # plays must have same number of cards as previous play
    if previous_play is not None:
        required_length = len(previous_play[1])
        match required_length:
            case 1:
                return [
                    [PLAYABLE_PRIORITY[0], [card]]
                    for card in deck
                    if card_cmp(card, previous_play[1][0]) > 0
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
    else:
        plays = []
        for card in deck:
            plays.append([PLAYABLE_PRIORITY[0], [card]])
        plays.extend(get_pairs(deck))
        plays.extend(get_triplets(deck))
        plays.extend(get_five_card_hands(deck))
        return plays


def main() -> None:
    # create and shuffle deck
    deck = []
    for rank in RANK_PRIORITY:
        for suit in SUIT_PRIORITY:
            deck.append(rank + suit)
    random.shuffle(deck)
    player_decks = []
    for i in range(PLAYER_COUNT):
        player_decks.append(
            deck[i * len(deck) // PLAYER_COUNT : (i + 1) * len(deck) // PLAYER_COUNT]
        )

    for player_deck in player_decks:
        sort_deck(player_deck)
        print("Player {}'s deck:".format(player_decks.index(player_deck) + 1))
        print(player_deck)
        print("Player {}'s valid plays:".format(player_decks.index(player_deck) + 1))
        print(get_valid_plays(player_deck))


def test_get_five_card_hands() -> None:
    play_options = get_valid_plays(
        ["3d", "3c", "3h", "3s", "4s", "5s", "6s", "7s", "9s"],
        ["straight", ["4c", "5h", "6d", "7c", "8h"]],
    )
    play_options.sort(key=play_cmp_key)
    print(play_options)


if __name__ == "__main__":
    test_get_five_card_hands()
