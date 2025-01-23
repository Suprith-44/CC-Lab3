import json
import os
import sqlite3


def connect(path):
    exists = os.path.exists(path)
    conn = sqlite3.connect(path)
    if not exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT DEFAULT '[]',
            cost REAL DEFAULT 0
        )
    ''')
    conn.commit()


def get_cart(username: str) -> list:
    with connect('carts.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM carts WHERE username = ?', (username,))
        cart = cursor.fetchone()
        return dict(cart) if cart else {}


def update_cart(username: str, contents: list[int], cost: float = 0):
    with connect('carts.db') as conn:
        conn.execute('''
            INSERT INTO carts (username, contents, cost)
            VALUES (?, ?, ?)
            ON CONFLICT(username)
            DO UPDATE SET contents = excluded.contents, cost = excluded.cost
        ''', (username, json.dumps(contents), cost))


def add_to_cart(username: str, product_id: int):
    cart = get_cart(username)
    contents = json.loads(cart.get('contents', '[]'))
    contents.append(product_id)
    update_cart(username, contents)


def remove_from_cart(username: str, product_id: int):
    cart = get_cart(username)
    contents = json.loads(cart.get('contents', '[]'))
    if product_id in contents:
        contents.remove(product_id)
        update_cart(username, contents)


def delete_cart(username: str):
    with connect('carts.db') as conn:
        conn.execute('DELETE FROM carts WHERE username = ?', (username,))
