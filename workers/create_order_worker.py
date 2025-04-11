from pydantic import BaseModel
from loguru import logger
import json
import uuid
import time

from workers.base import RabbitMQConnection
from database.db import insert_order


class OrderModel(BaseModel):
    id: str
    created_at: str
    client_id: int


def create_order(order_data):
    order_id = str(uuid.uuid4())
    json_order = json.loads(order_data)

    new_order = OrderModel(
        id=order_id,
        created_at=json_order["created_at"],
        client_id=json_order["client_id"],
    )

    result = insert_order(order_data=new_order)
    if result["success"] == False:
        return result

    message = {"order_id": order_id, "items": json_order["order_item_list"]}

    for _ in range(3):
        try:
            connection = RabbitMQConnection(queue="create_order_item_queue")
            connection.publish(message=message)
            connection.close()
            break
        except Exception as e:
            logger.warning(f"Retrying to publish message: {e}")
            time.sleep(1)

    return {"success": True, "order_id": order_id}

