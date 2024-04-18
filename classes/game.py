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
        player_hands = self.deck.deal(self.player_count)
        self.current_player_index = -1
        for idx, player_hand in enumerate(player_hands):
            sort_cards(player_hand)
            self.players[idx].set_hand(player_hand)
            # 3d is always the first card in a sorted hand so time complexity is actually O(1)
            if "3d" in player_hand:
                self.current_player_index = idx

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]
