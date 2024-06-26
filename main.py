from classes.game import Game
from classes.player import HumanPlayer, LowestAIPlayer, RandomAIPlayer


def main() -> None:
    # create game
    players = [
        HumanPlayer(),
        RandomAIPlayer(),
        RandomAIPlayer(),
        LowestAIPlayer(),
    ]
    game = Game(players)
    game.start_new_game()

    # play game until someone wins or player quits
    while True:
        play_options = game.get_current_player().get_play_options(
            game.last_played_set, game.is_first_turn
        )
        if isinstance(game.get_current_player(), HumanPlayer):
            print("Current player's hand: {}".format(game.get_current_player().hand))
            print("Play options:")
            for idx, play_option in enumerate(play_options):
                print("{}) {}".format(idx + 1, play_option))
            print("q) Quit game")

        index_to_play = game.get_current_player().get_play_choice()
        if index_to_play == -1:
            return
        played_set = game.get_current_player().play_card_set_by_index(index_to_play)
        print(
            "Player {} ({}) played {}".format(
                game.current_player_index + 1,
                game.get_current_player().player_type(),
                played_set,
            )
        )
        # pass played set to function to save history
        if game.did_player_win(played_set):
            print("Player {} wins!\n".format(game.current_player_index + 1))
            break

        if game.next_player(played_set):
            print(
                "\nAll other players passed, starting new round with player {}\n".format(
                    game.current_player_index + 1
                )
            )

    game.print_history()


if __name__ == "__main__":
    main()
