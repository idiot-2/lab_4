import sqlite3

mapping = {
    'Elden Ring': 'https://picsum.photos/seed/eldenring/400/300',
    "Baldur's Gate 3": 'https://picsum.photos/seed/baldursgate3/400/300',
    'Palworld': 'https://picsum.photos/seed/palworld/400/300',
    'Cyberpunk 2077': 'https://picsum.photos/seed/cyberpunk2077/400/300',
    'Hogwarts Legacy': 'https://picsum.photos/seed/hogwartslegacy/400/300',
    'Counter-Strike 2': 'https://picsum.photos/seed/cs2/400/300',
    'DOTA 2': 'https://picsum.photos/seed/dota2/400/300',
    'The Witcher 3': 'https://picsum.photos/seed/witcher3/400/300',
    'Starfield': 'https://picsum.photos/seed/starfield/400/300',
    'Call of Duty: Modern Warfare III': 'https://picsum.photos/seed/codmw3/400/300',
    "Dragon's Dogma 2": 'https://picsum.photos/seed/dragonsdogma2/400/300',
    'Final Fantasy VII Rebirth': 'https://picsum.photos/seed/ff7rebirth/400/300',
}

def update():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    updated = 0
    for name, url in mapping.items():
        cur.execute('UPDATE products SET image = ? WHERE name = ?', (url, name))
        updated += cur.rowcount
    conn.commit()
    conn.close()
    print(f'Updated images for {updated} rows')

if __name__ == '__main__':
    update()
