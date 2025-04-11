from typing import Callable
from loguru import logger
import pika
import json

import pika.exceptions


class RabbitMQConnection:
    def __init__(self, host="localhost", queue="default"):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        logger.info("Connecting with RabbitMQ...")
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)
            self.channel.confirm_delivery()
        except Exception as e:
            raise logger.error(f"Failed to connect to RabbitMQ... - {e}")

    def publish(self, message: dict):
        if not self.channel:
            self.connect()

        logger.info(f"Publishing message - {json.dumps(message)}")

        try:
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2),
                mandatory=True,
            )
        except pika.exceptions.UnroutableError as e:
            logger.error(f"Failed to publish message: {e}")

    def consume(self, callback: Callable):
        if not self.channel:
            self.connect()

        self.channel.basic_qos(prefetch_count=5)
        self.channel.basic_consume(queue=self.queue, on_message_callback=callback)
        logger.info(f"Consuming orders from queue - {self.queue}")
        self.channel.start_consuming()

    def close(self):
        if self.connection:
            self.connection.close()

