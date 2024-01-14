import jwt


class GameSessionManager:
    def __init__(self):
        self._sessions = {}
        self._tokens: dict = {}

    def resolve_message(self, message: dict):
        if message.get("type") == "create_session":
            return self.create_session(message["gamers_id"])
        elif message.get("type") == "check_rules":
            return self.is_user_participant(message["player_id"],
                                            message["session_id"]) and self.is_allowed_command(
                message["user_id"],
                message["command_id"]
            )

    def get_session(self, session_id):
        return self._sessions.get(session_id)

    def create_session(self, gamers_id: list) -> int:
        """
        Создание игровой сессии.
        """
        session_id = len(self._sessions) + 1  # требует правки, в рамках д/з принято решение не усложнять
        self._sessions[session_id] = gamers_id
        return session_id

    def is_user_participant(self, player_id, session_id):
        # Проверяем, является ли пользователь участником указанного танкового боя

        return player_id in self._sessions.get(session_id, [])

    def is_allowed_command(self, user_id, command_id):
        return True  # в рамках д/з принято решение не прорабатывать логику.

    # Генерация JWT токена
    def generate_jwt_token(self, payload: dict, secret_key) -> str:
        if self.is_user_participant(payload["player_id"], payload["game_id"]):
            token = jwt.encode(payload, secret_key, algorithm="HS256")
            self._tokens[token] = payload
            return token

    # Проверка JWT токена
    def verify_jwt_token(self, token, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload and token in self._tokens
        except jwt.exceptions.InvalidTokenError:
            return None

    def remove_jwt_token(self, token):
        self._tokens.pop(token)

    def remove_session(self, session_id):
        self._sessions.pop(session_id)
