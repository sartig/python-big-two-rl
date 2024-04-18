from typing import List


class Playable:
    def __init__(self, hand_type: str, cards: List[str]) -> None:
        self.hand_type = hand_type
        self.cards = cards

    def __str__(self) -> str:
        return f"{self.hand_type}: {self.cards}"
