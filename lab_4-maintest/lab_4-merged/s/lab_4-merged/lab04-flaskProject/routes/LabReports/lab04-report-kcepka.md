# Звіт з лабораторної роботи 4

## Реалізація бази даних для вебпроєкту

### Інформація про команду
- Назва команди:

- Учасники:
  - Терещук Дмитро (роль: Front-end dev.)
  - Антонюк Андрій (роль: Support dev.)
  - Корець Ярослав (роль: DB dev.)

## Завдання

### Обрана предметна область

Магазин ключів ігор Steam

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [+] Рівень 1: Створено базу даних SQLite з таблицею для відгуків, реалізовано базові CRUD операції, створено адмін-панель для перегляду та видалення відгуків, додано функціональність магазину з таблицями для товарів та замовлень
- [+] Рівень 2: Створено додаткову таблицю, релевантну предметній області, реалізовано роботу з новою таблицею через адмін-панель, інтегровано функціональність у застосунок

## Хід виконання роботи

### Підготовка середовища розробки

Опишіть процес налаштування:

- Версія Python: 3.14
- Встановлені бібліотеки: Flask, SQLite3
- Інші використані інструменти та розширення: -

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

```
project/
├── app.py
├── templates/
│   ├── about.html
│   ├── admin.html
│   ├── base.html
│   └── ...
├── routes/
│   ├── __pycache__
│   ├── __init__.py
│   └── admin.py
│   └── ...
└── LabReports/
    └── lab03-report-id.md
    └── lab04-report-id.md
```
### Проектування бази даних

#### Схема бази даних

Опишіть структуру вашої бази даних:

```
Таблиця "feedback":
id (INTEGER PRIMARY KEY AUTOINCREMENT)
name (TEXT)
email (TEXT)
message (TEXT)


Таблиця "products":
id (INTEGER PRIMARY KEY AUTOINCREMENT)
name (TEXT)
price (REAL)
image (TEXT)

Таблиця "orders":
id (INTEGER PRIMARY KEY AUTOINCREMENT)
email (TEXT)
address (TEXT)
total_price (REAL)
status (TEXT)
date (TEXT)

Таблиця "users":
id (INTEGER PRIMARY KEY AUTOINCREMENT)
username (TEXT UNIQUE)
email (TEXT UNIQUE)
password_hash (TEXT)
```



### Опис реалізованої функціональності

#### Система відгуків

Відгуки подаються на сторінці Зворотнього зв'язку і відображаються у адмін панелі

#### Магазин

Через сторінку Магазин можна додати товари до кошика де можна оформити покупку. Вона буде відображатися в адмін панелі

#### Адміністративна панель

Через адмін-панель можна керувати статусом покупок, видаляти їх та видаляти/читати відгуки

#### Додаткова функціональність (якщо реалізовано)



## Ключові фрагменти коду

### Ініціалізація бази даних

Наведіть код створення таблиць у файлі `models.py`:

```python
import sqlite3

def init_db() -> None:
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, message TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, image TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, address TEXT, total_price REAL, status TEXT, date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER, quantity INTEGER, FOREIGN KEY (order_id) REFERENCES orders (id), FOREIGN KEY (product_id) REFERENCES products (id))')
    # Таблиця користувачів
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password_hash TEXT)')
    conn.commit()
    conn.close()
```

### CRUD операції

Наведіть приклади реалізації CRUD операцій:

#### Створення (Create)

```python
def add_product(name: str, price: float, image: str) -> None:
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO products (name, price, image) VALUES (?, ?, ?)',
        (name, price, image)
    )
    conn.commit()
    conn.close()

```

#### Читання (Read)

```python
def get_products() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return [dict(p) for p in products]

```

#### Оновлення (Update)

```python
def update_product(product_id: int, name: str, price: float, image: str) -> None:
    conn = get_db_connection()
    conn.execute(
        'UPDATE products SET name = ?, price = ?, image = ? WHERE id = ?',
        (name, price, image, product_id)
    )
    conn.commit()
    conn.close()

```

#### Видалення (Delete)

```python
def delete_product(product_id: int) -> None:
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

```

### Маршрутизація

Наведіть приклади маршрутів для роботи з базою даних:

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if not username or not email or not password:
            error = 'Всі поля обов\'язкові.'
        elif password != confirm:
            error = 'Паролі не співпадають.'
        else:
            user_id = create_user(username.strip(), email.strip(), password)
            if user_id:
                session['username'] = username.strip()
                session['user_id'] = user_id
                return redirect(url_for('home'))
            else:
                error = 'Користувач з таким ім\'ям або email вже існує.'
    return render_template('register.html', error=error)
```

### Робота зі зв'язками між таблицями

Наведіть приклад запиту з використанням JOIN для отримання пов'язаних даних:

```python
def get_feedback_with_users():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            f.id,
            f.message,
            f.created_at,
            u.username,
            u.email
        FROM feedback f
        JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC;
    """)

    data = cur.fetchall()
    conn.close()
    return data
```

## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

- Корець Ярослав: опис виконаних завдань (CRUD операції, тестування, документація)
- Антонюк Андрій: опис виконаних завдань (Проектування БД, тестування, створення шаблонів)
- Терещук Дмитро: опис виконаних завдань (маршрутизація адмін-панель)

## Скріншоти

Додайте скріншоти основних функцій вашого вебзастосунку:

### Форма зворотного зв'язку

![Форма зворотного зв'язку](https://drive.google.com/file/d/1c8SnXQlZR46gbf-9lG-aRE3H_cF9trIT/view?usp=drive_link)

### Каталог товарів

![Каталог товарів](https://drive.google.com/file/d/1O726wr2i6NnnKKzA8U9o_JGFTTTQ7b8F/view?usp=drive_link)

### Адміністративна панель

![Адмін-панель](https://drive.google.com/file/d/1qcNsOTo3RZklJI0zEQKS12aXZ-6brfDM/view?usp=drive_link)

### Управління замовленнями

![Управління замовленнями](https://drive.google.com/file/d/13nCjpdPDl--iKJppUfapqZbciqHuxAcX/view?usp=drive_link)

### Точка.

![Точка.](https://drive.google.com/file/d/1RwO6dO3pFlmBLawWD2Z8odx-yLOoZh8m/view?usp=drive_link)

## Тестування

### Сценарії тестування

Опишіть, які сценарії ви тестували:

1. Додавання нового відгуку та перевірка його відображення в адмін-панелі
2. Створення товару, додавання його до кошика та оформлення замовлення
3. Зміна статусу замовлення через адмін-панель
4. Видалення записів з бази даних
5. Перевірка валідації даних
6. Роботу "точки"


## Висновки

Опишіть:

- Через піт та кров вдалося реалізувати роботу всіх сторінок так, як задумувалося
- Отримали навички роботи з SQLite
- Організовували роботу команди через Телеграм та Діскорд

Очікувана оцінка: 10

Обґрунтування: Рахую що заслуговую на цю оцінку бо ми старалися над роботою з сайтом та засвоїли матеріал. Немало часу було витрачено на вивчення роботи БД, Фласк-у