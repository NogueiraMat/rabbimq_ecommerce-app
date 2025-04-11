import psycopg2
from contextlib import contextmanager

db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 
    10,
    host="localhost",
    database="ecommerce",
    user="admin",
    password="admin"
)

@contextmanager
def get_db_connection():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

def insert_order(order_data):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO "order" (id, created_at, client_id)
                        VALUES (%s, %s, %s)
                    """,
                    (order_data.id, order_data.created_at, order_data.client_id),
                )
                conn.commit()
        return {"success": True, "message": "Order inserted successfully."}

    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}

def insert_order_item(order_id: str, order_item):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO order_item (order_id, product_id, quantity, unit_price)
                        VALUES (%s, %s, %s, %s)
                    """,
                    (
                        order_id,
                        order_item.product_id,
                        order_item.quantity,
                        order_item.price,
                    ),
                )
                conn.commit()
        return {"success": True, "msg": "Order item inserted successfully!"}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}

def fetch_order():
    data = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        SELECT 
                            id as ID,
                            created_at as CREATED_AT,
                            client_id as CLIENT_ID,
                            status as STATUS
                        FROM "order";
                    """
                )

                results = cursor.fetchall()

                for result in results:
                    data.append(
                        {
                            "id": result[0],
                            "created_at": str(result[1]),
                            "client_id": result[2],
                            "status": result[3],
                        }
                    )
        return {"success": True, "data": data}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}

def fetch_order_item(order_id: str):
    data = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT 
                            id as ORDER_ITEM_ID,
                            order_id as ORDER_ID,
                            product_id as PRODUCT_ID,
                            quantity as QUANTITY,
                            unit_price as PRICE
                        FROM order_item 
                        WHERE order_id = '{order_id}'
                    """
                )

                results = cursor.fetchall()

                for result in results:
                    data.append(
                        {
                            "id": result[0],
                            "order_id": result[1],
                            "product_id": result[2],
                            "quantity": result[3],
                            "unit_price": result[4],
                        }
                    )

        return {"success": True, "data": data}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}
