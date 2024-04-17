import random
from typing import List

from constants import RANK_PRIORITY, SUIT_PRIORITY


class Playable:
    def __init__(self, hand_type: str, cards: List[str]) -> None:
        self.hand_type = hand_type
        self.cards = cards

    def __str__(self) -> str:
        return f"{self.hand_type}: {self.cards}"


class Deck:
    def __init__(self) -> None:
        self.reset()

    def deal(self, player_count: int) -> List[List[str]]:
        random.shuffle(self.cards)
        player_decks = []
        for i in range(player_count):
            player_decks.append(
                self.cards[
                    i * len(self.cards) // player_count : (i + 1)
                    * len(self.cards)
                    // player_count
                ]
            )
        return player_decks

    def reset(self) -> None:
        self.cards = []
        for rank in RANK_PRIORITY:
            for suit in SUIT_PRIORITY:
                self.cards.append(rank + suit)
