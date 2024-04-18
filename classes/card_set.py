from typing import List


class CardSet:
    def __init__(self, hand_type: str, cards: List[str]) -> None:
        self.hand_type = hand_type
        self.cards = cards

    def __str__(self) -> str:
        return f"{self.hand_type}: {self.cards}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CardSet):
            return False
        return self.hand_type == other.hand_type and self.cards == other.cards

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
