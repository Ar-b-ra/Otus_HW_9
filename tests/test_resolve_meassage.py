import unittest

from game_session_manager import GameSessionManager


class TestResolveMessage(unittest.TestCase):

    def setUp(self):
        self.obj = GameSessionManager()
        self.message = {
            "type": "create_session",
            "gamers_id": [1, 2, 3],
            "player_id": 2,
            "session_id": 789,
            "user_id": 987,
            "command_id": 654
        }

    def test_create_session(self):
        result = self.obj.resolve_message(self.message)
        self.assertEqual(result, 1)

    def test_check_rules(self):
        self.obj.create_session(self.message["gamers_id"])
        self.assertFalse(self.obj.is_user_participant(self.message["player_id"], self.message["session_id"]))
        self.assertTrue(self.obj.is_user_participant(self.message["player_id"], 1))
        self.assertTrue(self.obj.is_allowed_command(self.message["user_id"], self.message["command_id"]))
        result = self.obj.resolve_message(self.message)
        self.assertTrue(result)

    def tearDown(self):
        self.obj._sessions = {}


if __name__ == "__main__":
    unittest.main()