import json
import os
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties, Basic

from jwt_generate import generate_jwt_token
from utility.custom_logger import root_logger

SECRET_KEY = "secret"  # Секретный ключ для генерации JWT токена. В рамках д/з будет находиться здесь

# Определение заголовков
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer my_token'
}


def callback(
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
    token = generate_jwt_token(payload, secret_key)

    # Публикация JWT токена в RabbitMQ
    _connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    _channel = connection.channel()
    _channel.basic_publish(
        exchange='',
        routing_key='jwt_token_queue',
        body=token
    )
    print(token)
    _connection.close()


# Создание подключения к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

if __name__ == "__main__":
    # Создание подключения к RabbitMQ
    rabbit_host = os.environ.get("RABBIT_HOST", "localhost")
    rabbit_port = int(os.environ.get("RABBIT_PORT", 5672))
    rabbit_queue = os.environ.get("RABBIT_QUEUE", "secret_queue")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, port=rabbit_port)
    )
    channel = connection.channel()

    # Создание очереди для получения сообщений
    channel.queue_declare(queue=rabbit_queue)
    # Установка callback функции для обработки полученных сообщений
    channel.basic_consume(
        queue=rabbit_queue, on_message_callback=callback, auto_ack=True
    )
    # Запуск бесконечного цикла ожидания сообщений
    print("Waiting for messages...")
    channel.start_consuming()
