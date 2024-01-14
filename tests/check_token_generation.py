import unittest

from game_session_manager import GameSessionManager


class TestVerifyJwtToken(unittest.TestCase):
    def setUp(self):
        self.my_class = GameSessionManager()
        self.secret_key = "secret_key"
        self.payload = {"game_id": 1,
                        "player_id": 1}
        self.my_class.create_session([1, 2, 3])
        self.token = self.my_class.generate_jwt_token(self.payload, self.secret_key)

    def test_valid_token(self):
        result = self.my_class.verify_jwt_token(self.token, self.secret_key)
        self.assertTrue(result)
        self.assertIn(self.token, self.my_class._tokens)

    def test_invalid_token(self):
        self.my_class._tokens = ["valid_token"]
        result = self.my_class.verify_jwt_token("invalid_token", self.secret_key)
        self.assertFalse(result)

    def test_invalid_secret_key(self):

        result = self.my_class.verify_jwt_token(self.token, "invalid_secret_key")
        self.assertFalse(result)

    def test_invalid_token_and_secret_key(self):
        token = "invalid_token"
        result = self.my_class.verify_jwt_token(token, "invalid_secret_key")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
