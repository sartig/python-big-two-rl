from classes.deck import Deck
from classes.player import Player
from utils import sort_cards


class Game:
    def __init__(self, player_count: int) -> None:
        self.deck = Deck()
        self.players = []
        self.player_count = player_count
        for _ in range(player_count):
            self.players.append(Player())

    def start_new_game(self) -> None:
        self.deck.reset()
        self.player_hands = self.deck.deal(self.player_count)
        self.current_player_index = -1
        for idx, player_hand in enumerate(self.player_hands):
            sort_cards(player_hand)
            if player_hand[0] == "3d":
                self.current_player_index = idx
