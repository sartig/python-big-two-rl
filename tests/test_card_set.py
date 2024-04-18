import unittest
from classes.card_set import CardSet


class TestCardSet(unittest.TestCase):
    def test_str_representation(self):
        hand_type = "single"
        cards = ["3d"]
        card_set = CardSet(hand_type, cards)
        self.assertEqual(str(card_set), "single: ['3d']")

    def test_equality(self):
        hand_type = "single"
        cards = ["3d"]
        card_set1 = CardSet(hand_type, cards)
        card_set2 = CardSet(hand_type, cards)
        self.assertEqual(card_set1, card_set2)


if __name__ == "__main__":
    unittest.main()
