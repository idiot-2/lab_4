from flask import Blueprint, jsonify, request
from flasgger import swag_from
from models import (
    get_products, get_product_by_id, create_product, update_product, delete_product,
    add_order, get_orders, get_order_details, update_order_status, delete_order,
    get_reviews, add_review
)
import re

api_v2_bp = Blueprint('api_v2', __name__, url_prefix="/api/v2")

@api_v2_bp.get("/products")
@swag_from({
    'tags': ['Products v2'],
    'responses': {200: {'description': 'List of products'}}
})
def api_get_products_v2():
    try:
        products = get_products()

        # параметры из GET-запроса
        q = request.args.get("q", "").lower()
        min_price = request.args.get("min_price")
        max_price = request.args.get("max_price")
        use_price_filter = request.args.get("use_price_filter", "1")  # по умолчанию включен

        # защита от отрицательных значений
        try:
            min_price = int(min_price) if min_price and int(min_price) >= 0 else None
        except (ValueError, TypeError):
            min_price = None
        try:
            max_price = int(max_price) if max_price and int(max_price) >= 0 else None
        except (ValueError, TypeError):
            max_price = None

        # фильтрация
        filtered = []
        for p in products:
            if q and q not in p['name'].lower():
                continue
            if use_price_filter == "1":
                if min_price is not None and p['price'] < min_price:
                    continue
                if max_price is not None and p['price'] > max_price:
                    continue
            filtered.append(p)

        for p in filtered:
            p["description"] = f"Product {p['name']} costs {p['price']} units."
        return jsonify({"status": "success", "data": filtered}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 1.2) Отримати товар за ID
# -------------------------------
@api_v2_bp.get("/products/<int:product_id>")
def api_get_product_v2(product_id):
    product = get_product_by_id(product_id)
    if product:
        product["description"] = f"Product {product['name']} costs {product['price']} units."
        return jsonify({"status": "success", "product": product}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


# -------------------------------
# 1.3) Створити новий товар (валідація)
# -------------------------------
@api_v2_bp.post("/products")
def api_create_product_v2():
    data = request.json
    if not data or "name" not in data or "price" not in data:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"status": "error", "message": "Name must be a non-empty string"}), 400

    if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
        return jsonify({"status": "error", "message": "Price must be positive"}), 400

    product_id = create_product(data["name"], data["price"], data.get("image"))
    return jsonify({"status": "success", "message": "Product created", "id": product_id}), 201


# -------------------------------
# 1.4) Оновити товар (валідація)
# -------------------------------
@api_v2_bp.put("/products/<int:product_id>")
def api_update_product_v2(product_id):
    data = request.json
    if "price" in data and (not isinstance(data["price"], (int, float)) or data["price"] <= 0):
        return jsonify({"status": "error", "message": "Price must be positive"}), 400

    updated = update_product(product_id, data.get("name"), data.get("price"), data.get("image"))
    if updated:
        return jsonify({"status": "success", "message": "Product updated"}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


# -------------------------------
# 1.5) Видалити товар
# -------------------------------
@api_v2_bp.delete("/products/<int:product_id>")
def api_delete_product_v2(product_id):
    deleted = delete_product(product_id)
    if deleted:
        return jsonify({"status": "success", "message": "Product deleted"}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


# -------------------------------
# 2) Створити нове замовлення (валідація email)
# -------------------------------
@api_v2_bp.post("/orders")
def api_create_order_v2():
    data = request.json
    required_fields = ["email", "address", "cart"]

    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({"status": "error", "message": "Invalid email format"}), 400

    try:
        add_order(data["email"], data["address"], data["cart"])
        return jsonify({"status": "success", "message": "Order created"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 3) Отримати всі замовлення
# -------------------------------
@api_v2_bp.get("/orders")
def api_get_all_orders_v2():
    orders = [dict(o) for o in get_orders()]
    return jsonify({"status": "success", "data": orders}), 200


# -------------------------------
# 4) Отримати конкретне замовлення
# -------------------------------
@api_v2_bp.get("/orders/<int:order_id>")
def api_get_order_v2(order_id):
    order, items = get_order_details(order_id)
    if not order:
        return jsonify({"status": "error", "message": "Order not found"}), 404
    return jsonify({
        "status": "success",
        "order": dict(order),
        "items": [dict(i) for i in items]
    }), 200


# -------------------------------
# 5) Оновити статус замовлення
# -------------------------------
@api_v2_bp.put("/orders/<int:order_id>")
def api_update_order_v2(order_id):
    data = request.json
    if "status" not in data:
        return jsonify({"status": "error", "message": "Status required"}), 400
    update_order_status(order_id, data["status"])
    return jsonify({"status": "success", "message": "Status updated"}), 200


# -------------------------------
# 6) Видалити замовлення
# -------------------------------
@api_v2_bp.delete("/orders/<int:order_id>")
def api_delete_order_v2(order_id):
    delete_order(order_id)
    return jsonify({"status": "success", "message": "Order deleted"}), 200



# -------------------------------
# 7) Реєстрація користувача (валідація email + пароль)
# -------------------------------
@api_v2_bp.post("/register")
def api_register_user_v2():
    data = request.json

    if not data or "email" not in data or "password" not in data:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    email = data["email"]
    password = data["password"]

    # Валідація email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"status": "error", "message": "Invalid email format"}), 400

    # Валідація пароля
    if len(password) < 6:
        return jsonify({"status": "error", "message": "Password too short"}), 400

    # Тут можна зберегти користувача в базу (поки просто успіх)
    return jsonify({"status": "success", "message": "User registered"}), 201


# -------------------------------
# 8) Логін користувача (перевірка email + пароль)
# -------------------------------
@api_v2_bp.post("/login")
def api_login_user_v2():
    data = request.json

    if not data or "email" not in data or "password" not in data:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    email = data["email"]
    password = data["password"]

    # Тут має бути перевірка з базою даних
    # Для прикладу — простий хардкод:
    if email == "user@example.com" and password == "test123":
        return jsonify({"status": "success", "message": "Login successful"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401


# -------------------------------
# Reviews API
# -------------------------------
@api_v2_bp.get("/reviews")
def api_get_reviews():
    reviews = get_reviews()
    return jsonify({"status": "success", "data": reviews}), 200


@api_v2_bp.post("/reviews")
def api_add_review():
    data = request.json
    if not data or "name" not in data or "game_title" not in data or "rating" not in data or "message" not in data:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if not isinstance(data["rating"], int) or not (1 <= data["rating"] <= 5):
        return jsonify({"status": "error", "message": "Rating must be integer 1-5"}), 400

    success = add_review(data["name"], data["game_title"], data["rating"], data["message"])
    if success:
        return jsonify({"status": "success", "message": "Review added"}), 201
    else:
        return jsonify({"status": "error", "message": "Invalid rating"}), 400


