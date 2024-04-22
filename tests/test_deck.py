import unittest

from classes.deck import Deck
from utils.constants import RANK_PRIORITY, SUIT_PRIORITY


class TestDeck(unittest.TestCase):
    def test_deal_empty_cards(self):
        deck = Deck()
        deck.cards = []
        player_count = 4
        player_decks = deck.shuffle_and_deal(player_count)

        self.assertEqual(player_decks, [[] for _ in range(player_count)])

    def test_deal_equal_cards(self):
        deck = Deck()
        deck.cards = ["3d", "3c", "3h", "3s", "4d", "4c"]
        player_count = 3
        player_decks = deck.shuffle_and_deal(player_count)

        self.assertEqual(len(player_decks), player_count)
        self.assertTrue(all(len(player_deck) == 2 for player_deck in player_decks))

    def test_deal_unequal_cards(self):
        deck = Deck()
        deck.cards = ["3d", "3c", "3h", "3s", "4d", "4c"]
        player_count = 4
        player_decks = deck.shuffle_and_deal(player_count)
        self.assertEqual(len(player_decks), player_count)
        self.assertTrue(all(len(player_deck) == 1 for player_deck in player_decks))

    def test_reset(self):
        deck = Deck()
        deck.reset()
        self.assertEqual(len(deck.cards), len(RANK_PRIORITY) * len(SUIT_PRIORITY))
        self.assertTrue(
            all(
                card + suit in deck.cards
                for card in RANK_PRIORITY
                for suit in SUIT_PRIORITY
            )
        )


if __name__ == "__main__":
    unittest.main()
