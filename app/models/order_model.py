from app.config.db import get_db
from psycopg2 import errors

def create_order(user_id, items):
    conn = get_db()
    cur = conn.cursor()

    total = sum(i["quantity"] * i["price"] for i in items)

    cur.execute(
        "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING *",
        (user_id, total)
    )
    order = cur.fetchone()

    for i in items:
        cur.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order["id"], i["product_id"], i["quantity"], i["price"]))

    conn.commit()
    cur.close()
    conn.close()

    return order

def get_orders_by_user(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders WHERE user_id=%s", (user_id,))
    orders = cur.fetchall()

    cur.close()
    conn.close()
    return orders

def get_order_detail(order_id, user_id, is_admin):
    conn = get_db()
    cur = conn.cursor()

    if is_admin:
        cur.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
    else:
        cur.execute("SELECT * FROM orders WHERE id=%s AND user_id=%s", (order_id, user_id))

    order = cur.fetchone()

    if not order:
        return None

    cur.execute("SELECT * FROM order_items WHERE order_id=%s", (order_id,))
    items = cur.fetchall()

    cur.close()
    conn.close()

    return {"order": order, "items": items}

def update_order_status(order_id, status):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE orders
            SET status=%s, updated_at=NOW()
            WHERE id=%s
            RETURNING *
        """, (status, order_id))

        order = cur.fetchone()
        conn.commit()

        return order

    except errors.CheckViolation:
        conn.rollback()
        return {"error": "Invalid status value"}

    except Exception:
        conn.rollback()
        return {"error": "Database error"}

    finally:
        cur.close()
        conn.close()