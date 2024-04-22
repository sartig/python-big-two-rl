import unittest

from classes.card_set import CardSet
from utils.game_logic import (
    _get_five_card_hands,
    _get_flushes,
    _get_four_of_a_kinds,
    _get_full_houses,
    _get_pairs,
    _get_straights,
    _get_triplets,
    get_valid_plays,
)


class TestGameLogic(unittest.TestCase):
    def test_get_pairs(self):
        # if no pairs in hand
        cards = ["3d", "4s"]
        pairs = _get_pairs(cards)
        self.assertEqual(pairs, [])

        # if just pairs in hand
        cards = ["3d", "3s", "4d", "4c"]
        pairs = _get_pairs(cards)
        expected = [CardSet("pair", ["3d", "3s"]), CardSet("pair", ["4d", "4c"])]
        self.assertEqual(pairs, expected)

        # if multiple combinations of pairs in hand
        cards = ["3d", "3h", "3s"]
        pairs = _get_pairs(cards)
        expected = [
            CardSet("pair", ["3d", "3h"]),
            CardSet("pair", ["3d", "3s"]),
            CardSet("pair", ["3h", "3s"]),
        ]
        self.assertEqual(pairs, expected)

    def test_get_triplets(self):
        # if no triplets in hand
        cards = ["3d", "4s"]
        triplets = _get_triplets(cards)
        self.assertEqual(triplets, [])

        # if just triplets in hand
        cards = ["3d", "3h", "3s", "4d", "4c", "4s"]
        triplets = _get_triplets(cards)
        expected = [
            CardSet("triplet", ["3d", "3h", "3s"]),
            CardSet("triplet", ["4d", "4c", "4s"]),
        ]
        self.assertEqual(triplets, expected)

        # if multiple combinations of pairs in hand
        cards = ["3d", "3c", "3h", "3s"]
        triplets = _get_triplets(cards)
        expected = [
            CardSet("triplet", ["3d", "3c", "3h"]),
            CardSet("triplet", ["3d", "3c", "3s"]),
            CardSet("triplet", ["3d", "3h", "3s"]),
            CardSet("triplet", ["3c", "3h", "3s"]),
        ]
        self.assertEqual(triplets, expected)

    def test_get_straights(self):
        # if no straights in hand
        cards = ["3d", "4s"]
        straights = _get_straights(cards)
        self.assertEqual(straights, [])

        # if just straights in hand
        cards = ["3d", "4c", "5s", "6h", "7d"]
        straights = _get_straights(cards)
        expected = [
            CardSet("straight", ["3d", "4c", "5s", "6h", "7d"]),
        ]
        self.assertEqual(straights, expected)

        # if multiple combinations of straights in hand
        cards = ["3d", "3c", "4c", "5s", "6h", "7d"]
        straights = _get_straights(cards)
        expected = [
            CardSet("straight", ["3d", "4c", "5s", "6h", "7d"]),
            CardSet("straight", ["3c", "4c", "5s", "6h", "7d"]),
        ]
        self.assertEqual(straights, expected)

        # if straight flush
        cards = ["3d", "4d", "5d", "6d", "7d"]
        straights = _get_straights(cards)
        expected = [
            CardSet("straightflush", ["3d", "4d", "5d", "6d", "7d"]),
        ]
        self.assertEqual(straights, expected)

    def test_get_flushes(self):
        # if no flushes in hand
        cards = ["3d", "4s"]
        flushes = _get_flushes(cards)
        self.assertEqual(flushes, [])

        # if just flushes in hand
        cards = ["3d", "4d", "5d", "6d", "td"]
        flushes = _get_flushes(cards)
        expected = [
            CardSet("flush", ["3d", "4d", "5d", "6d", "td"]),
        ]
        self.assertEqual(flushes, expected)

        # if multiple combinations of flushes in hand
        cards = ["3d", "4d", "5d", "6d", "8d", "9d"]
        flushes = _get_flushes(cards)
        expected = [
            CardSet("flush", ["3d", "4d", "5d", "6d", "8d"]),
            CardSet("flush", ["3d", "4d", "5d", "6d", "9d"]),
            CardSet("flush", ["3d", "4d", "5d", "8d", "9d"]),
            CardSet("flush", ["3d", "4d", "6d", "8d", "9d"]),
            CardSet("flush", ["3d", "5d", "6d", "8d", "9d"]),
            CardSet("flush", ["4d", "5d", "6d", "8d", "9d"]),
        ]
        self.assertEqual(flushes, expected)

        # ensure straight flushes are ignored
        cards = ["3d", "4d", "5d", "6d", "7d"]
        flushes = _get_flushes(cards)
        expected = []
        self.assertEqual(flushes, expected)

    def test_get_full_houses(self):
        # if no full houses in hand
        cards = ["3d", "4s", "5s", "6s", "7s"]
        full_houses = _get_full_houses(cards)
        self.assertEqual(full_houses, [])

        # if one full house in hand
        cards = ["3d", "3c", "4c", "6d", "6h", "6s"]
        full_houses = _get_full_houses(cards)
        expected = [
            CardSet("fullhouse", ["3d", "3c", "6d", "6h", "6s"]),
        ]
        self.assertEqual(full_houses, expected)

        # if multiple combinations of full houses in hand
        cards = ["3d", "3c", "3s", "6c", "6h", "6s"]
        full_houses = _get_full_houses(cards)
        expected = [
            CardSet("fullhouse", ["6c", "6h", "3d", "3c", "3s"]),
            CardSet("fullhouse", ["6c", "6s", "3d", "3c", "3s"]),
            CardSet("fullhouse", ["6h", "6s", "3d", "3c", "3s"]),
            CardSet("fullhouse", ["3d", "3c", "6c", "6h", "6s"]),
            CardSet("fullhouse", ["3d", "3s", "6c", "6h", "6s"]),
            CardSet("fullhouse", ["3c", "3s", "6c", "6h", "6s"]),
        ]
        self.assertEqual(full_houses, expected)

    def test_get_four_of_a_kinds(self):
        # if no four of a kinds in hand
        cards = ["3d", "4s", "5s", "6s", "7s"]
        four_of_a_kinds = _get_four_of_a_kinds(cards)
        self.assertEqual(four_of_a_kinds, [])

        # if one four of a kind in hand
        cards = ["3d", "3c", "3h", "3s", "6c", "6h", "6s"]
        four_of_a_kinds = _get_four_of_a_kinds(cards)
        expected = [
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "6c"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "6h"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "6s"]),
        ]
        self.assertEqual(four_of_a_kinds, expected)

    def test_get_five_card_hands(self):
        # if no five card hands in hand
        cards = ["3d", "4s", "5s", "6s", "8s"]
        five_card_hands = _get_five_card_hands(cards)
        self.assertEqual(five_card_hands, [])

        # if one five card hand in hand
        cards = ["3d", "3c", "3h", "3s", "6c"]
        five_card_hands = _get_five_card_hands(cards)
        expected = [
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "6c"]),
        ]
        self.assertEqual(five_card_hands, expected)

        # if multiple combinations of five card hands in hand
        cards = ["3d", "3c", "3h", "3s", "6c", "6h", "7d", "8d", "9d", "tc", "kd"]
        five_card_hands = _get_five_card_hands(cards)
        expected = [
            CardSet("straight", ["6c", "7d", "8d", "9d", "tc"]),
            CardSet("straight", ["6h", "7d", "8d", "9d", "tc"]),
            CardSet("flush", ["3d", "7d", "8d", "9d", "kd"]),
            CardSet("fullhouse", ["6c", "6h", "3d", "3c", "3h"]),
            CardSet("fullhouse", ["6c", "6h", "3d", "3c", "3s"]),
            CardSet("fullhouse", ["6c", "6h", "3d", "3h", "3s"]),
            CardSet("fullhouse", ["6c", "6h", "3c", "3h", "3s"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "6c"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "6h"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "7d"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "8d"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "9d"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "tc"]),
            CardSet("fourofakind", ["3d", "3c", "3h", "3s", "kd"]),
        ]
        self.assertEqual(five_card_hands, expected)

    def test_get_valid_plays_no_previous_is_starting_hand(self):
        cards = ["3d", "5s", "6s", "7s", "8s"]
        valid_plays = get_valid_plays(cards, is_starting_hand=True)
        expected = [CardSet("single", ["3d"])]
        self.assertEqual(valid_plays, expected)

    def test_get_valid_plays_no_previous_not_starting_hand(self):
        cards = ["3d", "5s", "6s", "7s", "8d", "8s"]
        valid_plays = get_valid_plays(cards, is_starting_hand=False)
        expected = [
            CardSet("single", ["3d"]),
            CardSet("single", ["5s"]),
            CardSet("single", ["6s"]),
            CardSet("single", ["7s"]),
            CardSet("single", ["8d"]),
            CardSet("single", ["8s"]),
            CardSet("pair", ["8d", "8s"]),
        ]
        self.assertEqual(valid_plays, expected)

    def test_get_valid_plays_with_previous(self):
        cards = ["3c", "3s", "8d", "8h"]
        valid_plays = get_valid_plays(cards, CardSet("pair", ["4d", "4h"]))
        expected = [CardSet("pair", ["8d", "8h"])]
        self.assertEqual(valid_plays, expected)


if __name__ == "__main__":
    unittest.main()
