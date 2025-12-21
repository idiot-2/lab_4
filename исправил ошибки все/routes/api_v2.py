from flask import Blueprint, jsonify, request, session
from flasgger import swag_from
from models import (
    get_products, get_product_by_id, create_product, update_product, delete_product,
    add_order, get_orders, get_order_details, update_order_status, delete_order,
    get_reviews, add_review, get_db_connection
)
import re

api_v2_bp = Blueprint('api_v2', __name__, url_prefix="/api/v2")

# -------------------------------
# 1.1) Отримати всі товари (з перевіркою обраного)
# -------------------------------
@api_v2_bp.get("/products")
@swag_from({
    'tags': ['Products v2'],
    'responses': {200: {'description': 'List of products with wishlist status'}}
})
def api_get_products_v2():
    try:
        user_id = session.get('user_id') # Получаем ID из сессии 2025
        
        conn = get_db_connection()
        # Запрос проверяет, добавлен ли товар в wishlist текущим пользователем
        query = '''
            SELECT p.*, 
            CASE WHEN w.id IS NOT NULL THEN 1 ELSE 0 END as is_wishlisted
            FROM products p
            LEFT JOIN wishlist w ON p.id = w.product_id AND w.user_id = ?
        '''
        products_raw = conn.execute(query, (user_id,)).fetchall()
        conn.close()
        
        products = [dict(p) for p in products_raw]

        # Параметры из GET-запроса для фильтрации
        q = request.args.get("q", "").lower()
        min_price = request.args.get("min_price")
        max_price = request.args.get("max_price")
        use_price_filter = request.args.get("use_price_filter", "1")

        filtered = []
        for p in products:
            # Поиск по имени
            if q and q not in p['name'].lower():
                continue
            
            # Фильтр по цене
            if use_price_filter == "1":
                try:
                    price = float(p['price'])
                    if min_price and price < float(min_price): continue
                    if max_price and price > float(max_price): continue
                except (ValueError, TypeError):
                    pass

            # Добавляем динамическое описание (как в вашем оригинальном коде)
            p["description"] = f"Product {p['name']} costs {p['price']} units."
            filtered.append(p)

        return jsonify({"status": "success", "data": filtered}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 1.2) Перемикач обраного (Toggle Wishlist)
# -------------------------------
@api_v2_bp.post("/wishlist/toggle")
def api_toggle_wishlist():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    data = request.json
    product_id = data.get("product_id")
    if not product_id:
        return jsonify({"status": "error", "message": "Product ID missing"}), 400

    conn = get_db_connection()
    # Проверяем, есть ли уже товар в избранном у этого юзера
    exists = conn.execute('SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?', 
                         (user_id, product_id)).fetchone()
    
    if exists:
        conn.execute('DELETE FROM wishlist WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        added = False
    else:
        conn.execute('INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
        added = True
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "added": added}), 200


# -------------------------------
# 1.3) Отримати товар за ID
# -------------------------------
@api_v2_bp.get("/products/<int:product_id>")
def api_get_product_v2(product_id):
    product = get_product_by_id(product_id)
    if product:
        product = dict(product)
        product["description"] = f"Product {product['name']} costs {product['price']} units."
        return jsonify({"status": "success", "product": product}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


# -------------------------------
# 1.4) Створити/Оновити/Видалити товар
# -------------------------------
@api_v2_bp.post("/products")
def api_create_product_v2():
    data = request.json
    if not data or "name" not in data or "price" not in data:
        return jsonify({"status": "error", "message": "Missing fields"}), 400
    product_id = create_product(data["name"], data["price"], data.get("image"))
    return jsonify({"status": "success", "id": product_id}), 201

@api_v2_bp.put("/products/<int:product_id>")
def api_update_product_v2(product_id):
    data = request.json
    updated = update_product(product_id, data.get("name"), data.get("price"), data.get("image"))
    if updated:
        return jsonify({"status": "success", "message": "Updated"}), 200
    return jsonify({"status": "error", "message": "Not found"}), 404

@api_v2_bp.delete("/products/<int:product_id>")
def api_delete_product_v2(product_id):
    if delete_product(product_id):
        return jsonify({"status": "success", "message": "Deleted"}), 200
    return jsonify({"status": "error", "message": "Not found"}), 404


# -------------------------------
# 2) Замовлення
# -------------------------------
@api_v2_bp.post("/orders")
def api_create_order_v2():
    data = request.json
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data.get("email", "")):
        return jsonify({"status": "error", "message": "Invalid email"}), 400
    try:
        add_order(data["email"], data["address"], data["cart"])
        return jsonify({"status": "success", "message": "Order created"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_v2_bp.get("/orders")
def api_get_all_orders_v2():
    orders = [dict(o) for o in get_orders()]
    return jsonify({"status": "success", "data": orders}), 200

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
# 3) Користувачі (Заглушки вашої логіки)
# -------------------------------
@api_v2_bp.post("/register")
def api_register_user_v2():
    return jsonify({"status": "success", "message": "Validation passed"}), 201

@api_v2_bp.post("/login")
def api_login_user_v2():
    return jsonify({"status": "success", "message": "Login logic checked"}), 200


# -------------------------------
# 4) Відгуки
# -------------------------------
@api_v2_bp.get("/reviews")
def api_get_reviews_v2():
    reviews = [dict(r) for r in get_reviews()]
    return jsonify({"status": "success", "data": reviews}), 200

@api_v2_bp.post("/reviews")
def api_add_review_v2():
    data = request.json
    add_review(data["name"], data["game_title"], data["rating"], data["message"])
    return jsonify({"status": "success", "message": "Review added"}), 201
