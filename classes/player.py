import random
from abc import ABC, abstractmethod
from time import sleep
from typing import List, Optional

from classes.card_set import CardSet
from utils.game_logic import get_valid_plays


class Player(ABC):
    def __init__(self) -> None:
        self.hand = []
        self.play_options = None

    def _play_cards(self, cards: CardSet) -> None:
        self.hand = [card for card in self.hand if card not in cards.cards]
        # clear play options cache
        self.play_options = None

    def play_card_set_by_index(self, index: int) -> CardSet:
        played_set = self.get_play_options()[index]
        self._play_cards(played_set)
        return played_set

    def get_play_options(
        self, previous_play: Optional[CardSet] = None, is_starting_hand: bool = False
    ) -> List[CardSet]:
        if self.play_options is not None:
            # return play options cache
            return self.play_options

        valid_plays = get_valid_plays(self.hand, previous_play, is_starting_hand)
        if previous_play is not None:
            valid_plays.append(CardSet("pass", []))
        self.play_options = valid_plays
        return valid_plays

    @abstractmethod
    def get_play_choice(self) -> int:
        pass

    @abstractmethod
    def player_type(self) -> str:
        pass


class HumanPlayer(Player):
    def get_play_choice(self) -> int:
        while True:
            selected = input("Enter selection: ")
            if selected.lower() == "q":
                return -1
            if (
                selected.isnumeric()
                and int(selected) > 0
                and self.play_options
                and int(selected) <= len(self.play_options)
            ):
                return int(selected) - 1
            else:
                print("Invalid selection")

    def player_type(self) -> str:
        return "Human"


class RandomAIPlayer(Player):
    def get_play_choice(self) -> int:
        sleep(1)
        if self.play_options:
            if len(self.play_options) == 1:
                return 0
            return random.randint(0, len(self.play_options) - 2)

        return -1

    def player_type(self) -> str:
        return "AI (random)"


class LowestAIPlayer(Player):
    def get_play_choice(self) -> int:
        if self.play_options:
            return 0
        return -1

    def player_type(self) -> str:
        return "AI (plays lowest)"
