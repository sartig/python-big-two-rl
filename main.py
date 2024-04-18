from classes.deck import Deck
from classes.playable import Playable
from classes.game import Game
from constants import PLAYER_COUNT
from game_logic import get_valid_plays
from utils import play_cmp_key, sort_cards


def main() -> None:
    # create deck
    deck = Deck()
    # deal cards
    player_decks = deck.deal(PLAYER_COUNT)
    for idx, player_deck in enumerate(player_decks):
        sort_cards(player_deck)
        print("Player {}'s deck:".format(idx + 1))
        print(player_deck)
        print("Player {}'s valid plays:".format(idx + 1))
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


def test_game() -> None:
    game = Game(PLAYER_COUNT)
    game.start_new_game()
    for index, player_hand in enumerate(game.player_hands):
        print("Player {}'s hand: {}".format(index + 1, player_hand))

    print("Starting player: {}".format(game.current_player_index + 1))


if __name__ == "__main__":
    # test_get_five_card_hands()
    # test_deck()
    test_game()
    # main()
