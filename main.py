import json
import os
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties, Basic

from game_session_manager import GameSessionManager
from utility.custom_logger import root_logger

SECRET_KEY = "secret"  # Секретный ключ для генерации JWT токена. В рамках д/з будет находиться здесь
# Создание менеджера игровых сессий
game_session_manager = GameSessionManager()
# Определение заголовков
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer my_token'
}


def jwt_callback(
        ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    root_logger.debug(
        f"Received message: {body = },\n"
        f"{ch = },\n"
        f"{method = },\n"
        f"{properties = },"
    )
    # Декодирование полученного сообщения
    message = json.loads(body.decode("utf-8"))

    # Извлечение необходимых данных из сообщения
    game_id = message["game_id"]
    player_id = message["player_id"]
    secret_key = SECRET_KEY

    # Генерация JWT токена
    payload = {"game_id": game_id,
               "player_id": player_id}
    token = game_session_manager.generate_jwt_token(payload, secret_key)

    answer_body = json.dumps({"token": token})

    # Публикация JWT токена в RabbitMQ
    chanel.basic_publish(
        exchange='',
        routing_key=token_answer_queue,
        body=answer_body
    )


def game_session_callback(
        ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    full_body = json.loads(body.decode("utf-8"))
    token_to_check = full_body.get("token", "")
    result = game_session_manager.verify_jwt_token(token_to_check, SECRET_KEY)
    if result:
        full_body.pop("token")
        chanel.basic_publish(
            exchange='',
            routing_key=token_answer_queue,
            body=game_session_manager.resolve_message(json.loads(full_body))
        )


if __name__ == "__main__":

    # Выставление значений подключений к RabbitMQ
    rabbit_host = os.environ.get("RABBIT_HOST", "localhost")
    rabbit_port = int(os.environ.get("RABBIT_PORT", 5672))

    # Создание очереди запроса JWT токенов
    jwt_queue = os.environ.get("TOKEN_QUEUE", "jwt_queue")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, port=rabbit_port)
    )
    chanel = connection.channel()
    chanel.queue_declare(queue=jwt_queue)
    chanel.basic_consume(
        queue=jwt_queue, on_message_callback=jwt_callback, auto_ack=True
    )

    # Создание очереди отправки JWT токенов
    token_answer_queue = os.environ.get("TOKEN_ANSWER_QUEUE", "jwt_answer_queue")
    chanel.queue_declare(queue=token_answer_queue)

    # Создание очереди работы с игровой сессией. Именно в неё отправляются команды управления вместе с JWT токеном
    game_queue = os.environ.get("GAME_SESSION_QUEUE", "game_session_queue")
    chanel.queue_declare(queue=game_queue)

    chanel.basic_consume(
        queue=game_queue, on_message_callback=game_session_callback, auto_ack=True
    )

    # Создание очереди отправки результатов выполнения команды (например, ошибки проверки JWT токена)
    game_answer_queue = os.environ.get("GAME_SESSION_ANSWER_QUEUE", "game_session_answer_queue")  # Ответ на команду
    chanel.queue_declare(queue=game_answer_queue)

    # Запуск бесконечного цикла ожидания сообщений
    print("Waiting for messages...")
    chanel.start_consuming()
