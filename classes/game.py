from typing import Optional
from classes.card_set import CardSet
from classes.deck import Deck
from classes.player import Player
from utils import sort_cards


class Game:
    def __init__(self, player_count: int) -> None:
        self.deck = Deck()
        self.player_count = player_count
        self.players = [Player() for _ in range(self.player_count)]

    def start_new_game(self) -> None:
        self.deck.reset()
        self.is_first_turn = True
        self.last_played_set = None
        player_hands = self.deck.deal(self.player_count)
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

    def next_player(self, played_set: Optional[CardSet] = None) -> None:
        self.is_first_turn = False
        if played_set is not None:
            self.last_played_set = played_set
            self.last_played_set_player = self.current_player_index
        self.last_played_player = self.current_player_index
        self.current_player_index = (self.current_player_index + 1) % self.player_count

        # if all other players have all passed, start a new round
        if self.current_player_index == self.last_played_set_player:
            print("\nAll other players passed, starting new round")
            self.start_new_round()

    def did_player_win(self) -> bool:
        return len(self.get_current_player().hand) == 0
