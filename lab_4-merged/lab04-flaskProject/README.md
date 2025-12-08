# Лабораторна робота №5: Розробка RESTful API

## Інформація про проєкт
- **Назва проєкту:** Магазин ключів Steam
- **Автори:** 
Антонюк Андрій
Корець Ярослав
Терещук Дмитро


## Опис проєкту
Проєкт реалізує RESTful API для онлайн-магазину продажу ключів до відеоігор
API дозволяє отримувати список товарів, створювати замовлення, переглядати їх, оновлювати статуси та видаляти замовлення.
Усі дані зберігаються у SQLite, а взаємодія відбувається у форматі JSON

## Технології
Python 3.10+
Flask
Flask Blueprint
SQLite
Werkzeug Security
Postman (для тестування)

## Endpoints API

### 1. Отримати всі товари
- **URL:** `/api/products`
- **Метод:** `GET`
- **Опис:** Повертає список усіх товарів із бази даних
- **Приклад запиту:**
```json
{
  "key": "value"
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Steam Key - GTA V",
      "price": 299.0,
      "image": "gta.jpg"
    }
  ]
}
```

### 2. Створити нове замовлення
- **URL:** `/api/orders`
- **Метод:** `POST`
- **Опис:** Створює нове замовлення
- **Приклад запиту:**
```json
{
  "email": "test@example.com",
  "address": "Kyiv, Ukraine",
  "cart": {
    "1": {"id": 1, "quantity": 2, "price": 200},
    "2": {"id": 2, "quantity": 1, "price": 350}
  }
}

```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "message": "Order created"
}
```

### 3. Отримати всі замовлення
- **URL:** `/api/orders`
- **Метод:** `GET`
- **Опис:** Повертає повний список замовлень
- **Приклад запиту:**
```json
{
  "key": "value"
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "email": "test@example.com",
      "address": "Kyiv",
      "total_price": 750.0,
      "status": "New",
      "date": "2025-02-01 12:00:00"
    }
  ]
}
```

### 4. Отримати конкретне замовлення
- **URL:** `/api/orders/<order_id>`
- **Метод:** `GET`
- **Опис:** Повертає інформацію про замовлення та список товарів у ньому
- **Приклад запиту:**
```json
{
  "key": "value"
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "order": {
    "id": 1,
    "email": "test@example.com",
    "address": "Kyiv",
    "total_price": 750,
    "status": "New",
    "date": "2025-02-01 12:00:00"
  },
  "items": [
    {
      "quantity": 2,
      "name": "GTA V",
      "price": 299
    }
  ]
}
```

### 5. Оновити статус замовлення
- **URL:** `/api/orders/<order_id>`
- **Метод:** `PUT`
- **Опис:** Оновлює статус замовлення
- **Приклад запиту:**
```json
{"status": "Paid"}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "message": "Status updated"
}
```

### 6. Видалити замовлення
- **URL:** `/api/orders/<order_id>`
- **Метод:** `DELETE`
- **Опис:** Видаляє замовлення разом із його товарами
- **Приклад запиту:**
```json
{
  "key": "value"
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "message": "Order deleted"
}
```

## Обробка помилок
Список реалізованих кодів помилок:
- `400 Bad Request` - POST /orders без полів email/address/cart
- `404 Not Found` - GET /orders/999
- `500 Internal Server Error` - Наприклад при проблемі з базою даних