from flask import Blueprint, jsonify, request
from models import (
    get_products, add_order, get_orders, get_order_details,
    update_order_status, delete_order
)

api_bp = Blueprint('api', __name__, url_prefix="/api")

# -------------------------------
# 1) Отримати всі товари
# -------------------------------
@api_bp.get("/products")
def api_get_products():
    try:
        products = get_products()
        return jsonify({"status": "success", "data": products}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 2) Створити нове замовлення
# -------------------------------
@api_bp.post("/orders")
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
@api_bp.get("/orders")
def api_get_all_orders():
    try:
        orders = [dict(o) for o in get_orders()]
        return jsonify({"status": "success", "data": orders}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# 4) Отримати конкретне замовлення
# -------------------------------
@api_bp.get("/orders/<int:order_id>")
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
@api_bp.put("/orders/<int:order_id>")
def api_update_order(order_id):
    data = request.json
    if "status" not in data:
        return jsonify({"status": "error", "message": "Status required"}), 400

    update_order_status(order_id, data["status"])
    return jsonify({"status": "success", "message": "Status updated"}), 200


# -------------------------------
# 6) Видалити замовлення
# -------------------------------
@api_bp.delete("/orders/<int:order_id>")
def api_delete_order(order_id):
    delete_order(order_id)
    return jsonify({"status": "success", "message": "Order deleted"}), 200
