from classes.game import Game
from classes.player import HumanPlayer, RandomAIPlayer


def main() -> None:
    # create game
    players = [
        HumanPlayer(),
        RandomAIPlayer(),
        RandomAIPlayer(),
        RandomAIPlayer(),
    ]
    game = Game(players)
    game.start_new_game()

    while True:
        print(
            "Current player: {} ({})".format(
                game.current_player_index + 1,
                game.get_current_player().__class__.__name__,
            ),
        )

        print("Last played set: {}".format(game.last_played_set))
        # if type(game.get_current_player) is HumanPlayer:
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
        if game.did_player_win():
            print("Player {} wins!".format(game.current_player_index + 1))
            return
        game.next_player(played_set)


if __name__ == "__main__":
    main()
