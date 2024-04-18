from classes.game import Game
from constants import PLAYER_COUNT


def main() -> None:
    # create game
    game = Game(PLAYER_COUNT)
    game.start_new_game()

    # print cards
    for idx, player in enumerate(game.players):
        print("Player {}'s hand: {}".format(idx + 1, player.hand))

    print("\nStarting player: {}".format(game.current_player_index + 1))

    print("Current player's hand: {}".format(game.get_current_player().hand))
    play_options = game.get_current_player().get_play_options(None, True)
    print("Play options:")
    for idx, play_option in enumerate(play_options):
        print("{}) {}".format(idx + 1, play_option))
    print("p) Pass")
    print("q) Quit game")


if __name__ == "__main__":
    main()
