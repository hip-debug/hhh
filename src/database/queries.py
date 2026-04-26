import psycopg2


def get_orders_with_products(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM orders
    JOIN users ON orders.user_id = users.id
    WHERE orders.user_id = %s""", (user_id,))
    products = cursor.fetchall()
    cursor.close()
    return products


def get_user_order_history(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM orders
        INNER JOIN order_items ON order_items.order_id = orders.id
        INNER JOIN products ON order_items.product_id = products.id
        WHERE orders.user_id = %s
        ORDER BY orders.created_at DESC""", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as e:
        print(f"Ошибка получения истории заказов: {e}")
        return []


def get_order_statistics(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, COUNT(*), SUM(total) FROM orders GROUP BY user_id")
        order_statistics = cursor.fetchall()
        cursor.close()
        return order_statistics
    except psycopg2.Error as e:
        print(f"Ошибка получения статистики: {e}")
        return []


def get_top_products(conn, limit=5):
    try:
        cursor = conn.cursor()
        cursor.execute("""SELECT product_id, SUM(quantity) FROM order_items
        GROUP BY product_id ORDER BY SUM(quantity) DESC LIMIT %s""", (limit,))
        products = cursor.fetchall()
        cursor.close()
        return products
    except psycopg2.Error as e:
        print(f"Ошибка получения топ товаров: {e}")
        return []
