from pydantic import BaseModel
from loguru import logger
import json

from workers.base import RabbitMQConnection
from database.db import insert_order_item


class OrderItemModel(BaseModel):
    product_id: int
    quantity: int
    price: float


def callback(ch, method, properties, body):
    data = json.loads(body.decode())
    order_items = data["items"]

    for item in order_items:
        logger.info(f"Processing item - {item}")
        new_order_item = OrderItemModel(
            product_id=item["id"], quantity=item["quantity"], price=item["price"]
        )

        insert_order_item(data["order_id"], new_order_item)
    try:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Erro processing: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def consume_messages():
    connection = RabbitMQConnection(queue="create_order_item_queue")
    connection.consume(callback=callback)

