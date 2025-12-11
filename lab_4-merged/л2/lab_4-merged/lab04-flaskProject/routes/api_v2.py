from flask import Blueprint, jsonify, request
from flasgger import swag_from
from models import (
    get_products, get_product_by_id, create_product, update_product, delete_product,
    add_order, get_orders, get_order_details, update_order_status, delete_order
)
import re

api_v2_bp = Blueprint('api_v2', __name__, url_prefix="/api/v2")

# -------------------------------
# 1.1) Отримати всі товари (з description)
# -------------------------------
@api_v2_bp.get("/products")
@swag_from({
    'tags': ['Products v2'],
    'responses': {200: {'description': 'List of products'}}
})
def api_get_products_v2():
    products = get_products()
    for p in products:
        p["description"] = f"Product {p['name']} costs {p['price']} units."
    return jsonify({"status": "success", "data": products}), 200


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



