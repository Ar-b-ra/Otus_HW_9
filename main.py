import os
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties, Basic

from resolver.message_resolver import MessageResolver
from utility.custom_logger import root_logger


def callback(
    ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes
):
    root_logger.trace(
        f"Received message: {body = },\n"
        f"{ch = },\n"
        f"{method = },\n"
        f"{properties = },"
    )
    # Обработка полученного сообщения
    message = body.decode("utf-8")
    resolver.resolve(message)


if __name__ == "__main__":
    # Создание подключения к RabbitMQ
    rabbit_host = os.environ.get("RABBIT_HOST", "localhost")
    rabbit_port = int(os.environ.get("RABBIT_PORT", 5672))
    rabbit_queue = os.environ.get("RABBIT_QUEUE", "my_queue")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host, port=rabbit_port)
    )
    channel = connection.channel()

    # Создание очереди для получения сообщений
    channel.queue_declare(queue=rabbit_queue)
    resolver = MessageResolver()
    # Установка callback функции для обработки полученных сообщений
    channel.basic_consume(
        queue=rabbit_queue, on_message_callback=callback, auto_ack=True
    )
    # Запуск бесконечного цикла ожидания сообщений
    print("Waiting for messages...")
    channel.start_consuming()
