import unittest
from unittest.mock import MagicMock

from classes.card_set import CardSet
from classes.deck import Deck
from classes.game import Game
from classes.player import HumanPlayer, Player


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.player_count = 4
        self.game = Game([HumanPlayer() for _ in range(4)])

    def test_initialize(self):
        # assert deck is initialised
        self.assertIsInstance(self.game.deck, Deck)
        # assert correct player count
        self.assertEqual(self.game.player_count, self.player_count)
        # assert correct num of players in array
        self.assertEqual(len(self.game.players), self.player_count)
        # assert players all instanced
        self.assertTrue(all(isinstance(player, Player) for player in self.game.players))

    def test_start_new_game(self):
        mock_deck = MagicMock()
        mock_deck.deal.return_value = [["3c"], ["3d"], ["3h"], ["3s"]]
        self.game.deck = mock_deck
        self.game.start_new_game()
        mock_deck.reset.assert_called_once()
        self.assertTrue(self.game.is_first_turn)
        self.assertIsNone(self.game.last_played_set)
        self.assertTrue(all(len(player.hand) == 1 for player in self.game.players))
        self.assertEqual(self.game.current_player_index, 1)

    def test_start_new_round(self):
        self.game.start_new_game()
        self.game.start_new_round()
        self.assertIsNone(self.game.last_played_set)
        self.assertIsNone(self.game.last_played_set_player)

    def test_next_player_is_first_turn(self):
        self.game.last_played_set_player = 1
        self.game.current_player_index = 0
        self.game.is_first_turn = True
        self.game.next_player()
        self.assertFalse(self.game.is_first_turn)

    ## work through from here :)
    def test_next_player_with_played_set(self):
        self.game.last_played_set_player = 1
        self.game.current_player_index = 0
        played_set = MagicMock(type=CardSet)
        self.game.next_player(played_set)
        self.assertEqual(self.game.last_played_set, played_set)
        self.assertEqual(self.game.last_played_set_player, 0)

    def test_next_player_without_played_set(self):
        self.game.last_played_set_player = 2
        self.game.current_player_index = 0
        self.game.next_player()
        self.assertEqual(self.game.current_player_index, 1)
        self.assertEqual(self.game.last_played_set_player, 2)

    def test_next_player_all_other_players_passed(self):
        self.game.current_player_index = 1
        self.game.last_played_set_player = 2
        self.game.start_new_round = MagicMock()
        self.game.next_player()
        self.assertEqual(self.game.current_player_index, 2)
        self.assertFalse(self.game.is_first_turn)
        self.game.start_new_round.assert_called_once()

    def test_did_player_win(self):
        self.game.current_player_index = 0
        for player in self.game.players:
            player.hand = ["3c"]
        self.assertFalse(self.game.did_player_win())
        self.game.players[0].hand = []
        self.assertTrue(self.game.did_player_win())
