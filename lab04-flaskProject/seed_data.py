from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    products = [
        ('Elden Ring', 2499, '/api/placeholder/200/200'),
        ('Baldur\'s Gate 3', 1999, '/api/placeholder/200/200'),
        ('Palworld', 399, '/api/placeholder/200/200'),
        ('Cyberpunk 2077', 1299, '/api/placeholder/200/200'),
        ('Hogwarts Legacy', 1999, '/api/placeholder/200/200'),
        ('Counter-Strike 2', 0, '/api/placeholder/200/200'),
        ('DOTA 2', 0, '/api/placeholder/200/200'),
        ('The Witcher 3', 999, '/api/placeholder/200/200'),
        ('Starfield', 2999, '/api/placeholder/200/200'),
        ('Call of Duty: Modern Warfare III', 3999, '/api/placeholder/200/200'),
        ('Dragon\'s Dogma 2', 2499, '/api/placeholder/200/200'),
        ('Final Fantasy VII Rebirth', 2699, '/api/placeholder/200/200'),
    ]
    
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Тестові продукти додано до бази даних.")