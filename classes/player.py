from typing import List

from classes.playable import Playable
from game_logic import get_valid_plays


class Player:
    def __init__(self) -> None:
        self.hand = []

    def set_hand(self, hand: List[str]) -> None:
        self.hand = hand

    def play_cards(self, cards: List[str]) -> None:
        self.hand = [card for card in self.hand if card not in cards]

    def get_play_options(self) -> List[Playable]:
        return get_valid_plays(self.hand)
