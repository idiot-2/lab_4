import sqlite3
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional
from werkzeug.security import generate_password_hash, check_password_hash


def get_db_connection() -> sqlite3.Connection:
    # Use absolute path to the database file located next to this models.py
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, image TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, address TEXT, total_price REAL, status TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY (order_id) REFERENCES orders (id), FOREIGN KEY (product_id) REFERENCES products (id))')
    # Users table for registration/authentication
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password_hash TEXT)')
    # Promo codes table
    conn.execute('CREATE TABLE IF NOT EXISTS promo_codes (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, discount_percent REAL, is_active BOOLEAN DEFAULT 1, created_at TEXT)')
    # Reviews table
    conn.execute('CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, game_title TEXT, rating INTEGER, message TEXT, created_at TEXT)')
    # Wishlist table
    conn.execute('CREATE TABLE IF NOT EXISTS wishlist (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, product_id INTEGER, FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (product_id) REFERENCES products (id))')
    conn.commit()
    conn.close()


def get_products() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return [dict(p) for p in products]


def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_product(name: str, price: float, image: Optional[str] = None) -> int:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', (name, price, image))
    conn.commit()
    product_id = cur.lastrowid
    conn.close()
    return product_id


def update_product(product_id: int, name: Optional[str] = None, price: Optional[float] = None, image: Optional[str] = None) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    if not cur.fetchone():
        conn.close()
        return False
    cur.execute('UPDATE products SET name = ?, price = ?, image = ? WHERE id = ?',
                (name, price, image, product_id))
    conn.commit()
    conn.close()
    return True


def delete_product(product_id: int) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    if not cur.fetchone():
        conn.close()
        return False
    cur.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return True


def add_order(email: str, address: str, cart: Dict[str, Dict[str, Any]], final_total: float = None) -> None:
    conn = get_db_connection()
    total_price = final_total if final_total is not None else sum(item['price'] * item['quantity'] for item in cart.values())
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (email, address, total_price, status, date) VALUES (?, ?, ?, ?, ?)',
                (email, address, total_price, 'New', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    order_id = cur.lastrowid
    for item in cart.values():
        cur.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (order_id, item['id'], item['quantity']))
    conn.commit()
    conn.close()


def get_orders() -> List[Any]:
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return orders


def get_order_details(order_id: int) -> Tuple[Optional[Any], List[Any]]:
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    items = conn.execute('SELECT oi.quantity, p.name, p.price FROM order_items oi JOIN products p ON oi.product_id = p.id WHERE oi.order_id = ?', (order_id,)).fetchall()
    conn.close()
    return order, items


def update_order_status(order_id: int, status: str) -> None:
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()


def delete_order(order_id: int) -> None:
    conn = get_db_connection()
    conn.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()


# --- User helpers ---
def create_user(username: str, email: str, password: str) -> int:
    conn = get_db_connection()
    cur = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cur.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash))
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        user_id = 0
    conn.close()
    return user_id


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def verify_user(username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username_or_email, username_or_email)).fetchone()
    conn.close()
    if row and check_password_hash(row['password_hash'], password):
        return dict(row)
    return None


# --- Promo code functions ---
def create_promo_code(code: str, discount_percent: float) -> bool:
    """Create a new promo code."""
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO promo_codes (code, discount_percent, created_at) VALUES (?, ?, ?)',
                    (code.upper(), discount_percent, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Code already exists
    finally:
        conn.close()


def get_promo_code(code: str) -> Optional[Dict[str, Any]]:
    """Get promo code details if active."""
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM promo_codes WHERE code = ? AND is_active = 1', (code.upper(),)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_promo_codes() -> List[Dict[str, Any]]:
    """Get all promo codes for admin."""
    conn = get_db_connection()
    codes = conn.execute('SELECT * FROM promo_codes ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(code) for code in codes]


def update_promo_code_status(code_id: int, is_active: bool) -> bool:
    """Activate or deactivate a promo code."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM promo_codes WHERE id = ?', (code_id,))
    if not cur.fetchone():
        conn.close()
        return False
    conn.execute('UPDATE promo_codes SET is_active = ? WHERE id = ?', (is_active, code_id))
    conn.commit()
    conn.close()
    return True


def delete_promo_code(code_id: int) -> bool:
    """Delete a promo code."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM promo_codes WHERE id = ?', (code_id,))
    if not cur.fetchone():
        conn.close()
        return False
    conn.execute('DELETE FROM promo_codes WHERE id = ?', (code_id,))
    conn.commit()
    conn.close()
    return True


def apply_promo_discount(total: float, promo_code: str) -> Tuple[float, float, Optional[str]]:
    """
    Apply promo code discount to total.
    Returns: (discounted_total, discount_amount, error_message)
    """
    promo = get_promo_code(promo_code)
    if not promo:
        return total, 0, "Недійсний промокод"

    discount_amount = total * (promo['discount_percent'] / 100)
    discounted_total = total - discount_amount

    return discounted_total, discount_amount, None


def get_reviews() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    reviews = conn.execute('SELECT * FROM reviews ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(r) for r in reviews]


def add_review(name: str, game_title: str, rating: int, message: str) -> bool:
    if not (1 <= rating <= 5):
        return False
    conn = get_db_connection()
    conn.execute('INSERT INTO reviews (name, game_title, rating, message, created_at) VALUES (?, ?, ?, ?, ?)',
                 (name, game_title, rating, message, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return True


def get_user_orders(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders WHERE email IN (SELECT email FROM users WHERE id = ?)', (user_id,)).fetchall()
    conn.close()
    return [dict(o) for o in orders]


def add_to_wishlist(user_id: int, product_id: int) -> bool:
    conn = get_db_connection()
    # Check if already in wishlist
    existing = conn.execute('SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?', (user_id, product_id)).fetchone()
    if existing:
        conn.close()
        return False  # Already in wishlist
    conn.execute('INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
    conn.commit()
    conn.close()
    return True


def remove_from_wishlist(user_id: int, product_id: int) -> bool:
    conn = get_db_connection()
    conn.execute('DELETE FROM wishlist WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    conn.commit()
    conn.close()
    return True


def get_user_wishlist(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    wishlist = conn.execute('''
        SELECT p.* FROM products p
        JOIN wishlist w ON p.id = w.product_id
        WHERE w.user_id = ?
    ''', (user_id,)).fetchall()
    conn.close()
    return [dict(p) for p in wishlist]


def get_total_orders() -> int:
    conn = get_db_connection()
    result = conn.execute('SELECT COUNT(*) as count FROM orders').fetchone()
    conn.close()
    return result['count']


def get_total_revenue() -> float:
    conn = get_db_connection()
    result = conn.execute('SELECT SUM(total_price) as revenue FROM orders').fetchone()
    conn.close()
    return result['revenue'] or 0


def get_total_products() -> int:
    conn = get_db_connection()
    result = conn.execute('SELECT COUNT(*) as count FROM products').fetchone()
    conn.close()
    return result['count']


def get_total_reviews() -> int:
    conn = get_db_connection()
    result = conn.execute('SELECT COUNT(*) as count FROM reviews').fetchone()
    conn.close()
    return result['count']
