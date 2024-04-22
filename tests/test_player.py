import unittest
from unittest.mock import patch
from classes.player import HumanPlayer
from classes.card_set import CardSet


class TestPlayer(unittest.TestCase):
    def test_play_cards_removes_matching_cards(self):
        player = HumanPlayer()
        player.hand = ["3d", "4h", "7c", "9s"]
        cards = CardSet("single", ["4h"])
        player._play_cards(cards)
        self.assertEqual(player.hand, ["3d", "7c", "9s"])

    def test_play_cards_no_matching_cards(self):
        player = HumanPlayer()
        player.hand = ["3d", "4h", "7c", "9s"]
        cards = CardSet("pair", ["5d", "5c"])
        player._play_cards(cards)
        self.assertEqual(player.hand, ["3d", "4h", "7c", "9s"])

    @patch("classes.player.get_valid_plays")
    def test_get_play_options_with_previous_play(self, get_valid_plays_mock):
        player = HumanPlayer()
        player.hand = ["3d", "4h", "7d", "7c"]
        previous_play = CardSet("pair", ["5d", "5c"])
        expected_return = [CardSet("pair", ["7d", "7c"])]
        get_valid_plays_mock.return_value = expected_return
        play_options = player.get_play_options(previous_play)
        self.assertEqual(play_options, expected_return)
        get_valid_plays_mock.assert_called_once_with(player.hand, previous_play, False)

    @patch("classes.player.get_valid_plays")
    def test_get_play_options_without_previous_play(self, get_valid_plays_mock):
        player = HumanPlayer()
        player.hand = ["3d", "4h", "7c", "9s"]
        expected_return = [
            CardSet("single", ["3d"]),
            CardSet("single", ["4h"]),
            CardSet("single", ["7c"]),
            CardSet("single", ["9s"]),
        ]
        get_valid_plays_mock.return_value = expected_return
        play_options = player.get_play_options()
        self.assertEqual(play_options, expected_return)
        get_valid_plays_mock.assert_called_once_with(player.hand, None, False)

    @patch("classes.player.get_valid_plays")
    def test_get_play_options_with_is_starting_hand(self, get_valid_plays_mock):
        player = HumanPlayer()
        player.hand = ["3d", "4h", "7c", "9s"]
        expected_return = [CardSet("single", ["3d"])]
        get_valid_plays_mock.return_value = expected_return
        play_options = player.get_play_options(None, is_starting_hand=True)
        self.assertEqual(play_options, expected_return)
        get_valid_plays_mock.assert_called_once_with(player.hand, None, True)


if __name__ == "__main__":
    unittest.main()
