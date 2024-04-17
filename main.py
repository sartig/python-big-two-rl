from typing import List

from classes import Deck, Playable
from constants import PLAYER_COUNT
from game_logic import get_valid_plays
from utils import card_cmp_key, play_cmp_key


def sort_deck(deck: List[str]) -> None:
    deck.sort(key=card_cmp_key)


def main() -> None:
    # create deck
    deck = Deck()
    # deal cards
    player_decks = deck.deal(PLAYER_COUNT)
    for player_deck in player_decks:
        sort_deck(player_deck)
        print("Player {}'s deck:".format(player_decks.index(player_deck) + 1))
        print(player_deck)
        print("Player {}'s valid plays:".format(player_decks.index(player_deck) + 1))
        if player_deck is not None:
            for play_option in get_valid_plays(player_deck):
                print(play_option)


def test_get_five_card_hands() -> None:
    play_options = get_valid_plays(
        ["3d", "3c", "3h", "3s", "9d", "9c", "9h"],
        Playable("straight", ["4c", "5h", "6d", "7c", "8h"]),
    )
    play_options.sort(key=play_cmp_key)
    for play_option in play_options:
        print(play_option)


if __name__ == "__main__":
    # test_get_five_card_hands()
    main()
