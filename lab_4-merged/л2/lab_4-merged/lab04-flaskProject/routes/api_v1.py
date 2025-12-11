from flask import Blueprint, jsonify, request
from flasgger import swag_from
from models import (
    get_products, get_product_by_id, create_product, update_product, delete_product,
    add_order, get_orders, get_order_details, update_order_status, delete_order
)

api_v1_bp = Blueprint('api_v1', __name__, url_prefix="/api/v1")

# -------------------------------
# 1.1) Отримати всі товари
# -------------------------------
@api_v1_bp.get("/products")
@swag_from({
    'tags': ['Products'],
    'responses': {
        200: {'description': 'A list of products'},
        500: {'description': 'Server error'}
    }
})
def api_get_products():
    try:
        products = get_products()
        return jsonify({"status": "success", "data": products}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 1.2) Отримати товар за ID
# -------------------------------
@api_v1_bp.get("/products/<int:product_id>")
def api_get_product(product_id):
    product = get_product_by_id(product_id)
    if product:
        return jsonify({"status": "success", "product": product}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


# -------------------------------
# 1.3) Створити новий товар
# -------------------------------
@api_v1_bp.post("/products")
def api_create_product():
    data = request.json
    if not data or "name" not in data or "price" not in data:
        return jsonify({"status": "error", "message": "Invalid input"}), 400
    product_id = create_product(data["name"], data["price"], data.get("image"))
    return jsonify({"status": "success", "message": "Product created", "id": product_id}), 201


# -------------------------------
# 1.4) Оновити товар
# -------------------------------
@api_v1_bp.put("/products/<int:product_id>")
def api_update_product(product_id):
    data = request.json
    updated = update_product(product_id, data.get("name"), data.get("price"), data.get("image"))
    if updated:
        return jsonify({"status": "success", "message": "Product updated"}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404


# -------------------------------
# 1.5) Видалити товар
# -------------------------------
@api_v1_bp.delete("/products/<int:product_id>")
def api_delete_product(product_id):
    deleted = delete_product(product_id)
    if deleted:
        return jsonify({"status": "success", "message": "Product deleted"}), 200
    return jsonify({"status": "error", "message": "Product not found"}), 404




# -------------------------------
# 2) Створити нове замовлення
# -------------------------------
@api_v1_bp.post("/orders")
@swag_from({
        'tags': ['Orders'],
        'requestBody': {
                'content': {
                        'application/json': {
                                'schema': {
                                        'type': 'object',
                                        'required': ['email', 'address', 'cart'],
                                        'properties': {
                                                'email': {'type': 'string'},
                                                'address': {'type': 'string'},
                                                'cart': {'type': 'array'}
                                        }
                                }
                        }
                }
        },
        'responses': {201: {'description': 'Order created'}, 400: {'description': 'Missing fields'}}
})
def api_create_order():
        data = request.json
        required_fields = ["email", "address", "cart"]

        if not all(field in data for field in required_fields):
                return jsonify({"status": "error", "message": "Missing fields"}), 400

        try:
                add_order(data["email"], data["address"], data["cart"])
                return jsonify({"status": "success", "message": "Order created"}), 201
        except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 3) Отримати всі замовлення
# -------------------------------
@api_v1_bp.get("/orders")
@swag_from({
        'tags': ['Orders'],
        'responses': {200: {'description': 'List of orders'}, 500: {'description': 'Server error'}}
})
def api_get_all_orders():
        try:
                orders = [dict(o) for o in get_orders()]
                return jsonify({"status": "success", "data": orders}), 200
        except Exception as e:
                return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 4) Отримати конкретне замовлення
# -------------------------------
@api_v1_bp.get("/orders/<int:order_id>")
@swag_from({
        'tags': ['Orders'],
        'parameters': [
                {'name': 'order_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}
        ],
        'responses': {200: {'description': 'Order details'}, 404: {'description': 'Order not found'}}
})
def api_get_order(order_id):
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
@api_v1_bp.put("/orders/<int:order_id>")
@swag_from({
        'tags': ['Orders'],
        'parameters': [
                {'name': 'order_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}
        ],
        'requestBody': {
                'content': {'application/json': {'schema': {'type': 'object', 'properties': {'status': {'type': 'string'}}}}}
        },
        'responses': {200: {'description': 'Status updated'}, 400: {'description': 'Status required'}}
})
def api_update_order(order_id):
        data = request.json
        if "status" not in data:
                return jsonify({"status": "error", "message": "Status required"}), 400

        update_order_status(order_id, data["status"])
        return jsonify({"status": "success", "message": "Status updated"}), 200


# -------------------------------
# 6) Видалити замовлення
# -------------------------------
@api_v1_bp.delete("/orders/<int:order_id>")
@swag_from({
        'tags': ['Orders'],
        'parameters': [
                {'name': 'order_id', 'in': 'path', 'required': True, 'schema': {'type': 'integer'}}
        ],
        'responses': {200: {'description': 'Order deleted'}}
})
def api_delete_order(order_id):
        delete_order(order_id)
        return jsonify({"status": "success", "message": "Order deleted"}), 200
