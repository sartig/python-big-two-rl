import random
from typing import List

from utils.constants import RANK_PRIORITY, SUIT_PRIORITY


class Deck:
    def __init__(self) -> None:
        self.reset()

    def shuffle_and_deal(self, player_count: int) -> List[List[str]]:
        """
        Deal cards equally to each player.

        Shuffles the cards and distributes them equally to each player. The number of cards dealt to each player is determined by the number of cards in the deck divided by the number of players.

        Args:
            player_count (int): Number of players to deal cards to.

        Returns:
            List[List[str]]: List of cards dealt to each player.
        """
        random.shuffle(self.cards)
        return [
            self.cards[
                i * (len(self.cards) // player_count) : (i + 1)
                * (len(self.cards) // player_count)
            ]
            for i in range(player_count)
        ]

    def reset(self) -> None:
        """
        Resets the deck's cards to be ordered by rank and suit (with 2 being the highest).
        """
        self.cards = [card + suit for card in RANK_PRIORITY for suit in SUIT_PRIORITY]
