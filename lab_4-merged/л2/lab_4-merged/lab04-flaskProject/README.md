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
### 1. отримати всі товари
- **URL:** `/api/products`
- **Метод:** `GET`
- **Опис:** Дає список всіх продуктів магазину
- **Приклад запиту:**
```json
{
  GET http://localhost:5000/api/products
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Product A",
      "price": 10.0,
      "image": "image1.jpg"
    },
    {
      "id": 2,
      "name": "Product B",
      "price": 15.5,
      "image": "image2.jpg"
    }
  ]
}
```
- **Скріншот з Postman (або Swagger):**
![Опис](https://drive.google.com/file/d/14-yWcFoEf6ZaFkBtWxWbQDSvA2qx91Tt/view?usp=drive_link)

### 2. створити нове замовлення
- **URL:** `/api/orders`
- **Метод:** `POST`
- **Опис:** Створює нове замовлення
- **Приклад запиту:**
```json
{
  POST http://localhost:5000/api/orders
Content-Type: application/json

{
  "email": "user@example.com",
  "address": "123 Main St",
  "cart": {
    "1": {"id": 1, "price": 10.0, "quantity": 2},
    "2": {"id": 2, "price": 15.5, "quantity": 1}
  }
}

}
```
- **Приклад відповіді:**
# 
```json
{
  "status": "success",
  "message": "Order created"
}
```
# 
```json
{
  "status": "error",
  "message": "Missing fields"
}
```
- **Скріншот з Postman (або Swagger):**
![Опис](https://drive.google.com/file/d/1oUqwDGeesyepztHft4x04r84BEzNNMZd/view?usp=drive_link)

### 3. отримати всі замовлення
- **URL:** `/api/orders`
- **Метод:** `GET`
- **Опис:** Дає інформацію по всім створеним замовленням
- **Приклад запиту:**
```json
{
  GET http://localhost:5000/api/orders
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "address": "123 Main St",
      "total_price": 35.5,
      "status": "New",
      "date": "2025-12-10 15:30:00"
    },
    {
      "id": 2,
      "email": "another@example.com",
      "address": "456 Second St",
      "total_price": 50.0,
      "status": "Completed",
      "date": "2025-12-09 11:20:00"
    }
  ]
}
```
- **Скріншот з Postman (або Swagger):**
![Опис](https://drive.google.com/file/d/1CrwTyQFfDMQn8xpJzwu5kSbU61C-FpG3/view?usp=drive_link)

### 4. отримати конкретне замовлення
- **URL:** `/api/orders/<order_id>`
- **Метод:** `GET`
- **Опис:** Дає інформацію про якесь конкретне замовлення
- **Приклад запиту:**
```json
{
  GET http://localhost:5000/api/orders/1
}
```
- **Приклад відповіді:**
# 
```json
{
  "status": "error",
  "message": "Order not found"
}
```
# 
```json
{
  "status": "success",
  "order": {
    "id": 1,
    "email": "user@example.com",
    "address": "123 Main St",
    "total_price": 35.5,
    "status": "New",
    "date": "2025-12-10 15:30:00"
  },
  "items": [
    {
      "quantity": 2,
      "name": "Product A",
      "price": 10.0
    },
    {
      "quantity": 1,
      "name": "Product B",
      "price": 15.5
    }
  ]
}
```
- **Скріншот з Postman (або Swagger):**
![Опис](https://drive.google.com/file/d/130nXeDhvqnaJWY_a2fRBQxz6O3MtuwAV/view?usp=drive_link)

### 5. оновити статус замовлення
- **URL:** `/api/orders/<order_id>`
- **Метод:** `PUT`
- **Опис:** Оновлює статус замовлення
- **Приклад запиту:**
```json
{
  PUT http://localhost:5000/api/orders/1
Content-Type: application/json

{
  "status": "Completed"
}
}
```
- **Приклад відповіді:**
# Успішна відповідь (200 ОК)
```json
{
  "status": "success",
  "message": "Status updated"
}
```
# Помилка (400 Bad Request)
```json
{
  "status": "error",
  "message": "Status required"
}
```
- **Скріншот з Postman (або Swagger):**
![Опис](https://drive.google.com/file/d/1hBFCHW12qAq4pncVByosMU9vyOiwspDf/view?usp=drive_link)

### 6. видалити замовлення
- **URL:** `/api/orders/<order_id>`
- **Метод:** `DELETE`
- **Опис:** Видаляє інфо про замовлення, та саме замовлення
- **Приклад запиту:**
```json
{
  DELETE http://localhost:5000/api/orders/1
}
```
- **Приклад відповіді:**
```json
{
  "status": "success",
  "message": "Order deleted"
}
```
- **Скріншот з Postman (або Swagger):**
![Опис](https://drive.google.com/file/d/1mkGcplR6qQ9pKR0fJUc1-ULkl-BzrQix/view?usp=drive_link)

## Обробка помилок
Список реалізованих кодів помилок:
- `400 Bad Request` - POST /orders без полів email/address/cart
- `404 Not Found` - GET /orders/999
- `500 Internal Server Error` - Наприклад при проблемі з базою даних