from models import get_db_connection, init_db

def seed_products():
    init_db()  # Спочатку ініціалізуємо базу даних
    conn = get_db_connection()
    products = [
        ('Elden Ring', 2499, 'https://picsum.photos/seed/eldenring/400/300'),
        ('Baldur\'s Gate 3', 1999, 'https://picsum.photos/seed/baldursgate3/400/300'),
        ('Palworld', 399, 'https://picsum.photos/seed/palworld/400/300'),
        ('Cyberpunk 2077', 1299, 'https://picsum.photos/seed/cyberpunk2077/400/300'),
        ('Hogwarts Legacy', 1999, 'https://picsum.photos/seed/hogwartslegacy/400/300'),
        ('Counter-Strike 2', 0, 'https://picsum.photos/seed/cs2/400/300'),
        ('DOTA 2', 0, 'https://picsum.photos/seed/dota2/400/300'),
        ('The Witcher 3', 999, 'https://picsum.photos/seed/witcher3/400/300'),
        ('Starfield', 2999, 'https://picsum.photos/seed/starfield/400/300'),
        ('Call of Duty: Modern Warfare III', 3999, 'https://picsum.photos/seed/codmw3/400/300'),
        ('Dragon\'s Dogma 2', 2499, 'https://picsum.photos/seed/dragonsdogma2/400/300'),
        ('Final Fantasy VII Rebirth', 2699, 'https://picsum.photos/seed/ff7rebirth/400/300'),
    ]
    
    conn.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', products)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_products()
    print("Тестові продукти додано до бази даних.")
