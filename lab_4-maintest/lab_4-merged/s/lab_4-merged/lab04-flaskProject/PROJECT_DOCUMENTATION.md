# Комплексна документація проєкту: Магазин ключів Steam

## 1. Огляд проєкту

### 1.1. Назва та автори
- **Назва проєкту:** Магазин ключів Steam
- **Автори:**
  - Антонюк Андрій
  - Корець Ярослав
  - Терещук Дмитро

### 1.2. Опис
Проєкт реалізує вебзастосунок для онлайн-магазину продажу ключів до відеоігор на платформі Steam. Застосунок включає:
- RESTful API для управління товарами та замовленнями
- Вебінтерфейс для користувачів (магазин, реєстрація, вхід)
- Адмінпанель для управління замовленнями та відгуками
- Систему тестування (unit та integration тести)
- Контейнеризацію з Docker

### 1.3. Технології
- **Backend:** Python 3.11+, Flask, Flask-Blueprint, SQLite
- **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
- **API документація:** Flasgger (Swagger UI)
- **Тестування:** pytest, pytest-flask, pytest-cov
- **Контейнеризація:** Docker, Docker Compose
- **Інструменти:** Git, Postman (для тестування API)

## 2. Архітектура системи

### 2.1. Структура файлів
```
lab04-flaskProject/
├── app.py                 # Головний файл додатку
├── models.py              # Моделі даних та функції БД
├── seed_data.py           # Ініціалізація тестових даних
├── requirements.txt       # Залежності Python
├── Dockerfile             # Конфігурація Docker образу
├── docker-compose.yml     # Конфігурація Docker Compose
├── .dockerignore          # Виключення файлів для Docker
├── .env                   # Змінні середовища
├── tests/                 # Тестові файли
│   ├── conftest.py        # Фікстури для тестів
│   ├── test_models.py     # Unit тести моделей
│   └── test_routes.py     # Integration тести маршрутів
├── routes/                # Blueprint'и для маршрутів
│   ├── __init__.py
│   ├── admin.py           # Адмінпанель
│   ├── api_v1.py          # API версія 1
│   ├── api_v2.py          # API версія 2
│   ├── dot.py             # Додаткові маршрути
│   ├── errors.py          # Обробка помилок
│   ├── feedback.py        # Зворотній зв'язок
│   └── shop.py            # Магазин
├── templates/             # HTML шаблони
│   ├── base.html          # Базовий шаблон
│   ├── home.html          # Головна сторінка
│   ├── login.html         # Вхід
│   ├── register.html      # Реєстрація
│   ├── shop.html          # Магазин
│   ├── admin.html         # Адмінпанель
│   └── ...
└── static/                # Статичні файли (CSS, JS, зображення)
```

### 2.2. Архітектурні компоненти
- **Flask App:** Головний додаток з Blueprint'ами
- **Database Layer:** SQLite з моделями (products, orders, users, feedback)
- **API Layer:** RESTful API з версіями v1 та v2
- **Web Layer:** HTML шаблони з Tailwind CSS
- **Testing Layer:** Автоматизовані тести з покриттям
- **Deployment Layer:** Docker контейнеризація

## 3. API документація

### 3.1. Загальна інформація
- **Base URL:** http://localhost:5000
- **Authentication:** Session-based для вебінтерфейсу
- **Response Format:** JSON
- **API Versions:** v1 (basic), v2 (extended)

### 3.2. Endpoints

#### Products API
- **GET /api/v1/products** - Отримати всі товари
- **GET /api/v1/products/:id** - Отримати товар за ID
- **POST /api/v1/products** - Створити новий товар
- **PUT /api/v1/products/:id** - Оновити товар
- **DELETE /api/v1/products/:id** - Видалити товар

#### Orders API
- **GET /api/v1/orders** - Отримати всі замовлення
- **GET /api/v1/orders/:id** - Отримати замовлення за ID
- **POST /api/v1/orders** - Створити замовлення
- **PUT /api/v1/orders/:id/status** - Оновити статус замовлення
- **DELETE /api/v1/orders/:id** - Видалити замовлення

#### Users API (v2)
- **POST /api/v2/users** - Реєстрація користувача
- **POST /api/v2/auth/login** - Авторизація

### 3.3. Приклади запитів

#### Створення товару
```bash
POST /api/v1/products
Content-Type: application/json

{
  "name": "Counter-Strike 2",
  "price": 0.0,
  "image": "cs2.jpg"
}
```

#### Створення замовлення
```bash
POST /api/v1/orders
Content-Type: application/json

{
  "email": "user@example.com",
  "address": "Test Address",
  "cart": {
    "1": {"id": 1, "price": 10.0, "quantity": 2}
  }
}
```

## 4. Інструкції користувача

### 4.1. Встановлення та запуск

#### Локальний запуск
1. **Передумови:**
   - Python 3.11+
   - pip
   - Git

2. **Клонування репозиторію:**
   ```bash
   git clone <repository-url>
   cd lab04-flaskProject
   ```

3. **Встановлення залежностей:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Запуск додатку:**
   ```bash
   python app.py
   # або
   flask run
   ```

5. **Доступ:**
   - Вебінтерфейс: http://localhost:5000
   - API документація: http://localhost:5000/apidocs

#### Запуск у Docker
1. **Передумови:**
   - Docker
   - Docker Compose

2. **Запуск:**
   ```bash
   docker-compose up --build
   ```

3. **Доступ:**
   - Вебінтерфейс: http://localhost:5000
   - API документація: http://localhost:5000/apidocs

### 4.2. Використання вебінтерфейсу

#### Реєстрація та вхід
1. Перейдіть на головну сторінку
2. Натисніть "Реєстрація" або "Вхід"
3. Заповніть форму та підтвердіть

#### Покупка товарів
1. Перейдіть до "Магазину"
2. Додайте товари до кошика
3. Перейдіть до оформлення замовлення
4. Заповніть дані доставки
5. Підтвердіть замовлення

#### Адмінпанель
1. Увійдіть як адміністратор
2. Перегляньте замовлення та відгуки
3. Змініть статус замовлень
4. Керуйте відгуками

### 4.3. Тестування API
Використовуйте Postman або curl для тестування API:

```bash
# Отримати всі товари
curl http://localhost:5000/api/v1/products

# Створити товар
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Game","price":15.99}'
```

## 5. Технічна документація

### 5.1. Моделі даних

#### Products
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    image TEXT
);
```

#### Orders
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    address TEXT,
    total_price REAL,
    status TEXT,
    date TEXT
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);
```

#### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT
);
```

#### Feedback
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
);
```

### 5.2. Конфігурація

#### Змінні середовища (.env)
```
FLASK_ENV=development
FLASK_APP=app.py
FLASK_RUN_HOST=0.0.0.0
DATABASE=db.sqlite  # для тестів перевизначається
TESTING=1           # для тестів
```

#### Docker конфігурація
- **Multi-stage build:** Зменшує розмір образу
- **Health check:** Перевіряє /health ендпоінт
- **Volume:** ./db.sqlite:/app/db.sqlite для збереження БД

### 5.3. Тестування

#### Запуск тестів
```bash
# Локально
python run_tests.py

# Або pytest
pytest --cov=models --cov=routes --cov-report=html tests/
```

#### Структура тестів
- **Unit тести:** test_models.py (21 тест)
- **Integration тести:** test_routes.py (21 тест)
- **Покриття:** 64%
- **Фікстури:** conftest.py (тимчасові БД для тестів)

## 6. Розгортання

### 6.1. Production deployment
1. Налаштуйте змінні середовища для production
2. Використовуйте WSGI сервер (gunicorn)
3. Налаштуйте reverse proxy (nginx)
4. Використовуйте PostgreSQL замість SQLite

### 6.2. Масштабування
- Використовуйте Docker Swarm або Kubernetes
- Розділіть API та вебінтерфейс
- Додайте кешування (Redis)
- Використовуйте CDN для статичних файлів

## 7. Внесок у розробку

### 7.1. Процес розробки
1. Створіть issue для нової функціональності
2. Створіть branch від main
3. Напишіть код та тести
4. Запустіть тести локально
5. Створіть Pull Request

### 7.2. Кодстайл
- Використовуйте PEP 8
- Пишіть docstrings для функцій
- Додавайте типізацію (type hints)
- Покривайте код тестами

## 8. Troubleshooting

### 8.1. Поширені проблеми
- **Помилка підключення до БД:** Перевірте права доступу до db.sqlite
- **Тести не проходять:** Перевірте наявність всіх залежностей
- **Docker не запускається:** Перевірте порти 5000

### 8.2. Логи
- Flask логи: у консолі при запуску
- Docker логи: `docker-compose logs`
- Тест логи: у виводі pytest

## 9. Ліцензія
Проект розроблено в навчальних цілях. Всі права захищені.