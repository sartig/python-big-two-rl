from typing import Sequence

from classes.card_set import CardSet
from classes.deck import Deck
from classes.player import Player
from utils.comparison import sort_cards


class Game:
    def __init__(self, player_list: Sequence[Player]) -> None:
        self.deck = Deck()
        self.players = player_list
        self._player_count = len(player_list)
        self.history = []
        self.round_number = 0

    def start_new_game(self) -> None:
        """
        Starts a new game by resetting all attributes. The deck is suffled and cards are
        dealt equally to each player. The player with the 3 of diamonds in their hand
        is set as the current player.
        """
        self.deck.reset()
        self.is_first_turn = True
        self.start_new_round()
        player_hands = self.deck.shuffle_and_deal(self._player_count)
        self.current_player_index = -1
        for idx, player_hand in enumerate(player_hands):
            sort_cards(player_hand)
            self.players[idx].hand = player_hand
            # 3d is always the first card in a sorted hand so time complexity is actually O(1)
            if "3d" in player_hand:
                self.current_player_index = idx

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def start_new_round(self) -> None:
        self.last_played_set = None
        self.last_played_player = None
        self.last_played_set_player = None
        self.round_number += 1

    # return true if a new round was started
    def next_player(self, played_set: CardSet = CardSet("pass", [])) -> bool:
        """
        Updates the current player index and checks if a new round should be started.

        Args:
            played_set (CardSet, optional): The card set played by the current player. Defaults to CardSet("pass", []).

        Returns:
            bool: True if a new round was started, False otherwise.
        """
        self.history.append((self.round_number, self.current_player_index, played_set))
        self.is_first_turn = False
        if played_set.hand_type != "pass":
            self.last_played_set = played_set
            self.last_played_set_player = self.current_player_index
        self.last_played_player = self.current_player_index
        self.current_player_index = (self.current_player_index + 1) % self._player_count

        # if all other players have all passed, start a new round
        if self.current_player_index == self.last_played_set_player:
            self.start_new_round()
            return True
        return False

    def did_player_win(self, played_set: CardSet) -> bool:
        if len(self.get_current_player().hand) == 0:
            self.history.append(
                (self.round_number, self.current_player_index, played_set)
            )
            self.history.append(
                (self.round_number, self.current_player_index, CardSet("win", []))
            )
            return True
        return False

    def print_history(self) -> None:
        prev_round = -1
        print("Game history:")
        for idx in range(len(self.history)):
            curr_round, curr_player, curr_play = self.history[idx]
            if curr_round != prev_round:
                if prev_round != -1:
                    print("Player {} wins the round!\n".format(curr_player + 1))
                print("Round {}:".format(curr_round))
                print(
                    "Player {} ({}) starts with {}".format(
                        curr_player + 1,
                        self.players[curr_player].player_type(),
                        curr_play,
                    )
                )
            elif curr_play.hand_type == "pass":
                print(
                    "Player {} ({}) passes".format(
                        curr_player + 1,
                        self.players[curr_player].player_type(),
                    )
                )
            elif curr_play.hand_type == "win":
                print(
                    "Player {} ({}) wins the game!".format(
                        curr_player + 1,
                        self.players[curr_player].player_type(),
                    )
                )
            else:
                print(
                    "Player {} ({}) plays {}".format(
                        curr_player + 1,
                        self.players[curr_player].player_type(),
                        curr_play,
                    )
                )

            prev_round = curr_round
