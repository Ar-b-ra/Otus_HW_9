import unittest

from game_session_manager import GameSessionManager


class TestGetSession(unittest.TestCase):
    def test_get_session_returns_value(self):
        # Test that the function returns the session value when it exists
        session_id = 1
        session_value = "session_data"
        obj = GameSessionManager()
        obj._sessions = {session_id: session_value}
        self.assertEqual(obj.get_session(session_id), session_value)

    def test_get_session_returns_none(self):
        # Test that the function returns None when the session does not exist
        session_id = 1
        obj = GameSessionManager()
        obj._sessions = {}
        self.assertIsNone(obj.get_session(session_id))


if __name__ == '__main__':
    unittest.main()
