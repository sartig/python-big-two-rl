from typing import List, Optional

from classes.card_set import CardSet
from utils.game_logic import get_valid_plays


class Player:
    def __init__(self) -> None:
        self.hand = []

    def play_cards(self, cards: CardSet) -> None:
        self.hand = [card for card in self.hand if card not in cards.cards]

    def get_play_options(
        self, previous_play: Optional[CardSet] = None, is_starting_hand: bool = False
    ) -> List[CardSet]:
        return get_valid_plays(self.hand, previous_play, is_starting_hand)
