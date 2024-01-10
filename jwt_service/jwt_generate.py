import jwt


# Генерация JWT токена
def generate_jwt_token(player_id, secret_key):
    payload = {"player_id": player_id}
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


# Проверка JWT токена
def verify_jwt_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        player_id = payload.get("player_id")
        return player_id
    except jwt.exceptions.InvalidTokenError:
        return None
