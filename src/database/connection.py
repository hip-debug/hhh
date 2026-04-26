import psycopg2
import psycopg2.extras as extras


def connect_to_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="qzwxecrvtb15A",
            dbname="sfmshop")
        conn.set_client_encoding('UTF8')
        return conn
    except psycopg2.Error as e:
        print(e)
        return None


def add_product(conn, name: str, price: float, quantity: int):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name,price,quantity) VALUES (%s, %s,%s)", (name, price, quantity))
    conn.commit()
    cursor.close()


def get_all_products(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * from products")
    products = cursor.fetchall()
    cursor.close()
    return products


def update_product_price(conn, product_id: int, new_price: float):
    cursor = conn.cursor()
    cursor.execute("UPDATE products set price =%s where id=%s", (new_price, product_id))
    conn.commit()
    cursor.close()


def create_user(conn, name, email):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
            (name, email)
        )
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return user_id
    except psycopg2.Error as e:
        print(f"Ошибка при создании пользователя: {e}")
        conn.rollback()
        return None


def get_user_by_id(conn, user_id):
    try:
        cur = conn.cursor(cursor_factory=extras.RealDictCursor)
        cur.execute(
            "SELECT id, name, email FROM users WHERE id = %s",
            (user_id,)
        )
        user = cur.fetchone()
        cur.close()
        if user:
            return dict(user)
        return None
    except psycopg2.Error as e:
        print(f"Ошибка при поиске пользователя: {e}")
        return None


def create_order(conn, user_id, total):
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING id",
            (user_id, total)
        )
        order_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return order_id
    except psycopg2.Error as e:
        print(f"Ошибка при создании заказа: {e}")
        conn.rollback()
        return None


def get_user_orders(conn, user_id):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, user_id, total, created_at FROM orders WHERE user_id = %s ORDER BY id",
            (user_id,)
        )
        orders = cur.fetchall()
        cur.close()
        return orders
    except psycopg2.Error as e:
        print(f"Ошибка получения заказов: {e}")
        return []


def delete_order(conn, order_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        result = cur.rowcount
        conn.commit()
        cur.close()
        return result
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Ошибка удаления заказа: {e}. Удалено 0 строк")
        return None
