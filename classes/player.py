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
        """
        Removes the played cards from the player's hand and clears the play options cache.

        If the player elects to pass their turn the cards argument will be a CardSet
        object with an empty list of cards.

        Args:
            cards (CardSet): The card set that was played.
        """
        self.hand = [card for card in self.hand if card not in cards.cards]
        # clear play options cache
        self.play_options = None

    def play_card_set_by_index(self, index: int) -> CardSet:
        """
        Plays a card set by its index. For a player passing their turn (when this option
        is available) this index is -1.

        Args:
            index (int): The index of the card set to be played.

        Returns:
            CardSet: The card set that was played.
        """
        played_set = self.get_play_options()[index]
        self._play_cards(played_set)
        return played_set

    def get_play_options(
        self, previous_play: Optional[CardSet] = None, is_starting_hand: bool = False
    ) -> List[CardSet]:
        """
        Returns a list of valid card sets that the player can play.

        Args:
            previous_play (Optional[CardSet], optional): The card set that was last played

            is_starting_hand (bool, optional): Whether the player is starting their game.

        Returns:
            List[CardSet]: A list of valid card sets that the player can play.
        """
        if self.play_options is not None:
            # return play options cache
            return self.play_options

        valid_plays = get_valid_plays(self.hand, previous_play, is_starting_hand)
        self.play_options = valid_plays
        return valid_plays

    @abstractmethod
    def get_play_choice(self) -> int:
        """
        An abstract method that should be implemented by any class that inherits from the Player class.
        It takes no parameters and returns an integer that represents the index of the card set that
        the player wants to play. The player can pass their turn by returning -1.
        """
        pass

    @abstractmethod
    def player_type(self) -> str:
        """
        An abstract method that should be implemented by any class that inherits from the Player class.
        It takes no parameters and returns a string representing the type of player.
        """
        pass


class HumanPlayer(Player):
    def get_play_choice(self) -> int:
        """
        Get the user's choice of play from the available options.

        This function prompts the user to enter a selection and validates the input. It
        continuously asks for input until a valid selection is made. The valid selections
        are the indices of the play options available to the player (input is one-indexed). The function returns
        the index of the selected play option.

        This function also allows the user to quit the game by entering "q".

        Returns:
            int: The index of the selected play option. Returns -1 if the user chooses
                to pass their turn.
        """
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
        """
        Returns a random choice from the available options. Will only pass if that is the only option available.
        """
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
        """
        Always returns the lowest card set from the available options. Will only pass if that is the only option available.
        """
        if self.play_options:
            return 0
        return -1

    def player_type(self) -> str:
        return "AI (plays lowest)"
