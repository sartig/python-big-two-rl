from typing import List, Optional

from classes.playable import Playable
from game_logic import get_valid_plays


class Player:
    def __init__(self) -> None:
        self.hand = []

    def set_hand(self, hand: List[str]) -> None:
        self.hand = hand

    def play_cards(self, cards: List[str]) -> None:
        self.hand = [card for card in self.hand if card not in cards]

    def get_play_options(
        self, previous_play: Optional[Playable] = None, is_starting_hand: bool = False
    ) -> List[Playable]:
        return get_valid_plays(self.hand, previous_play, is_starting_hand)
