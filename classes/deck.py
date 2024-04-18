import random
from typing import List

from constants import RANK_PRIORITY, SUIT_PRIORITY


class Deck:
    def __init__(self) -> None:
        self.reset()

    def deal(self, player_count: int) -> List[List[str]]:
        random.shuffle(self.cards)
        player_decks = []
        for i in range(player_count):
            player_decks.append(
                self.cards[
                    i * (len(self.cards) // player_count) : (i + 1)
                    * (len(self.cards) // player_count)
                ]
            )
        return player_decks

    def reset(self) -> None:
        self.cards = [card + suit for card in RANK_PRIORITY for suit in SUIT_PRIORITY]
