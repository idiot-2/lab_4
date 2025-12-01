import sqlite3
import sys

db_path = 'db.sqlite'
try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="products"')
    if not cur.fetchone():
        print('NO_TABLE')
        sys.exit(0)
    cur.execute('SELECT COUNT(*) FROM products')
    cnt = cur.fetchone()[0]
    print('COUNT', cnt)
except Exception as e:
    print('ERROR', e)
finally:
    try:
        conn.close()
    except:
        pass
