from datetime import datetime
from psycopg2 import pool
import psycopg2

from contextlib import contextmanager


db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10, host="localhost", database="ecommerce", user="admin", password="admin"
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
                        INSERT INTO "order" (id, created_at, user_id)
                        VALUES (%s, %s, %s)
                    """,
                    (order_data.id, order_data.created_at, order_data.user_id),
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
                            user_id as USER_ID,
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
                            "user_id": result[2],
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
                            oi.id AS ORDER_ITEM_ID,
                            oi.order_id AS ORDER_ID,
                            oi.product_id AS PRODUCT_ID,
                            oi.quantity as QUANTITY,
                            oi.unit_price as PRICE,
                            p.name as PRODUCT_NAME,
                            p.description as PRODUCT_DESCRIPTION,
                            p.sku as PRODUCT_SKU
                        FROM order_item oi
                        JOIN product p ON oi.product_id = p.id
                        WHERE oi.order_id = '{order_id}'
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
                            "product": {
                                "name": result[5],
                                "description": result[6],
                                "sku": result[7],
                            },
                        }
                    )

        return {"success": True, "data": data}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}


def insert_user(user_data):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO "user" (username, password, firstname, lastname, address, role)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        user_data.username,
                        user_data.password,
                        user_data.firstname,
                        user_data.lastname,
                        user_data.address,
                        user_data.role,
                    ),
                )
                conn.commit()
        return {"success": True, "msg": "User created successfully!"}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}


def fetch_a_user(username):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                        SELECT * FROM "user" 
                        WHERE username = '{username}'
                    """
                )

                result = cursor.fetchall()
                if result:
                    return {
                        "id": result[0][0],
                        "username": result[0][1],
                        "password": result[0][2],
                        "firstname": result[0][3],
                        "lastname": result[0][4],
                        "address": result[0][5],
                        "created_at": str(result[0][6]),
                        "role": result[0][7],
                    }
                return None
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}


def insert_product(product_data):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO product (sku, name, description, price)
                        VALUES (%s, %s, %s, %s)
                    """,
                    (
                        product_data.sku,
                        product_data.name,
                        product_data.description,
                        product_data.price,
                    ),
                )
                conn.commit()
        return {"success": True, "msg": "User created successfully!"}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}


def fetch_products(product_sku=None):
    data = []
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = """ SELECT * FROM product """
                if product_sku:
                    query = f""" SELECT * FROM product where sku = '{product_sku}' """
                cursor.execute(query)

                results = cursor.fetchall()
                for result in results:
                    data.append(
                        {
                            "id": result[0],
                            "sku": result[1],
                            "name": result[2],
                            "description": result[3],
                            "price": result[4],
                            "created_at": result[5],
                            "updated_at": result[6],
                        }
                    )
        return {"success": True, "data": data}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}


def insert_stock(stock_data):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO stock (product_id, quantity)
                        VALUES (%s, %s)
                        ON CONFLICT (product_id)
                        DO UPDATE SET
                            quantity = EXCLUDED.quantity,
                            updated_at = %s
                    """,
                    (stock_data.product_id, stock_data.quantity, datetime.now()),
                )
                conn.commit()
        return {"success": True, "msg": "Stock created/updated successfully!"}
    except psycopg2.Error as e:
        return {"success": False, "error": str(e)}

