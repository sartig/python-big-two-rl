from classes.game import Game
from utils.constants import PLAYER_COUNT


def main() -> None:
    # create game
    game = Game(PLAYER_COUNT)
    game.start_new_game()

    while True:
        print("Current player: {}".format(game.current_player_index + 1))
        print("Current player's hand: {}".format(game.get_current_player().hand))
        play_options = game.get_current_player().get_play_options(
            game.last_played_set, game.is_first_turn
        )
        print("Play options:")
        for idx, play_option in enumerate(play_options):
            print("{}) {}".format(idx + 1, play_option))
        if not game.is_first_turn and game.last_played_set is not None:
            print("p) Pass")
        print("q) Quit game")
        selected = input("Enter selection: ")
        if selected == "q":
            return
        if selected == "p" and not game.is_first_turn:
            game.next_player()
            continue
        if (
            selected.isnumeric()
            and int(selected) > 0
            and int(selected) <= len(play_options)
        ):
            played_set = play_options[int(selected) - 1]
            game.get_current_player().play_cards(played_set)
            if game.did_player_win():
                print("Player {} wins!".format(game.current_player_index + 1))
                return
            game.next_player(played_set)
        else:
            print("Invalid selection")


if __name__ == "__main__":
    main()
