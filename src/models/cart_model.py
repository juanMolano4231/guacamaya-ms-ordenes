from src.config.db import get_db

def get_or_create_cart(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM carts WHERE user_id=%s", (user_id,))
    cart = cur.fetchone()

    if not cart:
        cur.execute(
            "INSERT INTO carts (user_id) VALUES (%s) RETURNING *",
            (user_id,)
        )
        cart = cur.fetchone()
        conn.commit()

    cur.close()
    conn.close()
    return cart

def get_cart_items(cart_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM cart_items WHERE cart_id=%s", (cart_id,))
    items = cur.fetchall()

    cur.close()
    conn.close()
    return items

def add_item(cart_id, product_id, quantity, price):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO cart_items (cart_id, product_id, quantity, price_at_add)
        VALUES (%s, %s, %s, %s)
        RETURNING *
    """, (cart_id, product_id, quantity, price))

    item = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()
    return item

def update_item(item_id, quantity, user_id, is_admin=False):
    conn = get_db()
    cur = conn.cursor()

    if is_admin:
        cur.execute("""
            UPDATE cart_items
            SET quantity=%s
            WHERE id=%s
            RETURNING *
        """, (quantity, item_id))
    else:
        cur.execute("""
            UPDATE cart_items ci
            SET quantity=%s
            FROM carts c
            WHERE ci.cart_id = c.id
              AND ci.id=%s
              AND c.user_id=%s
            RETURNING ci.*
        """, (quantity, item_id, user_id))

    item = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()
    return item

def delete_item(item_id, user_id, is_admin=False):
    conn = get_db()
    cur = conn.cursor()

    if is_admin:
        cur.execute("DELETE FROM cart_items WHERE id=%s RETURNING *", (item_id,))
    else:
        cur.execute("""
            DELETE FROM cart_items ci
            USING carts c
            WHERE ci.cart_id = c.id
              AND ci.id=%s
              AND c.user_id=%s
            RETURNING ci.*
        """, (item_id, user_id))

    deleted = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()
    return deleted

def get_total(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(quantity * price_at_add) AS total
        FROM cart_items ci
        JOIN carts c ON ci.cart_id = c.id
        WHERE c.user_id=%s
    """, (user_id,))

    total = cur.fetchone()

    cur.close()
    conn.close()
    return total

def get_all_carts():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM carts")
    carts = cur.fetchall()

    cur.close()
    conn.close()
    return carts

def delete_cart(user_id, is_admin=False, cart_id=None):
    conn = get_db()
    cur = conn.cursor()

    if is_admin and cart_id:
        cur.execute("""
            DELETE FROM carts
            WHERE id=%s
            RETURNING *
        """, (cart_id,))
    else:
        cur.execute("""
            DELETE FROM carts
            WHERE user_id=%s
            RETURNING *
        """, (user_id,))

    deleted = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()
    return deleted