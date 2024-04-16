import random
from functools import cmp_to_key
from itertools import combinations

'''
Cards:
3456789tjqka2

♦♣♥♠

Suits:
Diamonds - d
Clubs - c
Hearts - h
Spades - s


Hands:
single
pair
three-of-a-kind
straight
flush
full house
four of a kind plus one
straight flush

Player's starting hand example:
['3c','5h','5s','7d','8h','9h','tc','qd','qc','qs','ks','ah','2d']

'''

RANK_PRIORITY = '3456789tjqka2'
SUIT_PRIORITY = 'dchs'
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


#TODO: implement 5-card-hand comparator
def five_card_hand_cmp(hand1: list[str], hand2: list[str]) -> int:
    # maybe label all the plays? so instead of a 'play' being ['c1','c1','c3','c4','c5']
    # it could be ['flush',['c1','c2','c3','c4','c5']]
    # extend this generally to all plays? i.e.
    # [['single', ['c1']], ['single', ['c2']], ['single', ['c3']], ['single', ['c4']], ['single', ['c5']], ['pair', ['c1','c6']], ...]
    pass


def sort_deck(deck: list[str]) -> None:
    deck.sort(key=card_cmp_key)

def get_pairs(deck: list[str]) -> list[list[str]]:
    # assumes deck is sorted
    pairs = []
    for i in range(len(deck)-1):
        for j in range(i+1, len(deck)):
            if deck[i][0] == deck[j][0]:
                pairs.append([deck[i], deck[j]])
    return pairs

def get_triplets(deck: list[str]) -> list[list[str]]:
    # assumes deck is sorted
    triplets = []
    card_ranks = [card[0] for card in deck]
    rank_counts = [card_ranks.count(rank) for rank in RANK_PRIORITY]
    valid_ranks = [[rank,count] for rank, count in zip(RANK_PRIORITY, rank_counts) if count >= 3]
    for rank, count in valid_ranks:
        if count == 3:
            triplets.append([card for card in deck if card[0] == rank])
        else: # count must be 4
            combs = combinations([card for card in deck if card[0] == rank], 3)
            for comb in combs:
                triplets.append(list(comb))
    return triplets

def get_straights(deck: list[str]) -> list[list[str]]:
    # straights are in rank order, with 3 being lowest and 2 being highest. lowest = 3-4-5-6-7, highest = J-Q-K-A-2
    straights = []
    deck_ranks = sorted(list(set([card[0] for card in deck])),key = lambda x: RANK_PRIORITY.index(x))
    straight_starting_ranks = []
    for i in range(len(deck_ranks)-4):
        if RANK_PRIORITY.index(deck_ranks[i]) + 4 == RANK_PRIORITY.index(deck_ranks[i+4]):
            straight_starting_ranks.append(deck_ranks[i])
    for starting_rank in straight_starting_ranks:
        rank_index = RANK_PRIORITY.index(starting_rank)
        card1 = [card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index]
        card2 = [card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index+1]
        card3 = [card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index+2]
        card4 = [card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index+3]
        card5 = [card for card in deck if RANK_PRIORITY.index(card[0]) == rank_index+4]

        # list comprehension reversed to preserve value order of straights (higher last card = better straight)
        straights.extend([[c1,c2,c3,c4,c5] for c5 in card5 for c4 in card4 for c3 in card3 for c2 in card2 for c1 in card1])
    
    return straights

def get_flushes(deck:list[str]) -> list[list[str]]:
    flushes = []
    # count suits, if any >=5 use combinations
    deck_suits = [card[1] for card in deck]
    suit_counts = [[suit,deck_suits.count(suit)] for suit in SUIT_PRIORITY]
    # TODO: check for and remove straight flushes (since they will be found by get_straights)
    for suit, suit_count in suit_counts:
        if suit_count >= 5:
            combs = combinations([card for card in deck if card[1] == suit], 5)
            for comb in combs:
                flushes.append(list(comb))

    return flushes

def get_five_card_hands(deck: list[str]) -> list[list[str]]:
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
            

def get_valid_plays(deck: list[str], previous_play: list[str] = None) -> list[list[str]]:
    # plays must have same number of cards as previous play
    if previous_play is not None:
        required_length = len(previous_play)
        match required_length:
            case 1:
                return [card for card in deck if card_cmp(card, previous_play[0])>0]
            case 2:
                # identify pairs in hand that are higher than previous play
                pairs = get_pairs(deck)
                # pairs only compare the higher card of the two to determine which is higher
                # i.e. 7D + 7S beats 7C + 7H
                return [pair for pair in pairs if card_cmp(pair[1], previous_play[1])>0]
            case 3:
                # identify triplets in hand that are higher than previous play
                triplets = get_triplets(deck)
                # cannot compare triplets of the same rank so just compare first card of each
                return [triplet for triplet in triplets if card_cmp(triplet[0], previous_play[0])>0]
            case 5:
                fives = get_five_card_hands(deck)
                # identify 5-card combinations in hand that are higher than previous play
                # use separate comparator for 5-card combinations
                return [five for five in fives if five_card_hand_cmp(five, previous_play)]
    else:
        plays = []
        for card in deck:
            plays.append([card])
        plays.extend(get_pairs(deck))
        plays.extend(get_triplets(deck))
        return plays

def main() -> None:
# create and shuffle deck
    deck = []
    for rank in RANK_PRIORITY:
        for suit in SUIT_PRIORITY:
            deck.append(rank+suit)
    random.shuffle(deck)
    player_decks = []
    for i in range(PLAYER_COUNT):
        player_decks.append(deck[i*len(deck)//PLAYER_COUNT:(i+1)*len(deck)//PLAYER_COUNT])

    for player_deck in player_decks:
        sort_deck(player_deck)
        print('Player {}\'s deck:'.format(player_decks.index(player_deck)+1))
        print(player_deck)
        print('Player {}\'s valid plays:'.format(player_decks.index(player_deck)+1))
        print(get_valid_plays(player_deck))


def test_get_five_card_hands()-> None:
    print(get_five_card_hands(['3s','4s','jd','qs','ks','as','ac','2d','2s']))

if __name__ == '__main__':
    test_get_five_card_hands()