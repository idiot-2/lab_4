from flask import Blueprint, render_template, redirect, url_for, request
from models import get_db_connection, get_orders, get_order_details, update_order_status, delete_order, get_all_promo_codes, create_promo_code, update_promo_code_status, delete_promo_code, create_product, get_products, get_reviews, get_total_orders, get_total_revenue, get_total_products, get_total_reviews

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin():
    conn = get_db_connection()
    feedback = conn.execute('SELECT * FROM feedback').fetchall()
    conn.close()
    orders = get_orders()
    promo_codes = get_all_promo_codes()
    products = get_products()
    reviews = get_reviews()
    stats = {
        'total_orders': get_total_orders(),
        'total_revenue': get_total_revenue(),
        'total_products': get_total_products(),
        'total_reviews': get_total_reviews()
    }
    return render_template('admin.html', feedback=feedback, orders=orders, promo_codes=promo_codes, products=products, reviews=reviews, stats=stats)

@admin_bp.route('/admin/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM feedback WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/order/<int:order_id>')
def order_details(order_id):
    order, items = get_order_details(order_id)
    return render_template('order_details.html', order=order, items=items)

@admin_bp.route('/admin/update_order_status/<int:order_id>', methods=['POST'])
def update_order(order_id):
    status = request.form['status']
    update_order_status(order_id, status)
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/delete_order/<int:order_id>', methods=['POST'])
def delete_order_route(order_id):
    delete_order(order_id)
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/create_promo', methods=['POST'])
def create_promo():
    code = request.form['code'].strip()
    discount_percent = float(request.form['discount_percent'])
    if create_promo_code(code, discount_percent):
        return redirect(url_for('admin.admin'))
    else:
        # Handle error - code already exists
        return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/toggle_promo/<int:code_id>', methods=['POST'])
def toggle_promo(code_id):
    is_active = request.form.get('is_active') == '1'
    update_promo_code_status(code_id, is_active)
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/delete_promo/<int:code_id>', methods=['POST'])
def delete_promo(code_id):
    delete_promo_code(code_id)
    return redirect(url_for('admin.admin'))

@admin_bp.route('/admin/create_product', methods=['POST'])
def create_product_route():
    name = request.form.get('name')
    price = request.form.get('price')
    image = request.form.get('image', '')
    if name and price:
        try:
            price = float(price)
            create_product(name, price, image)
        except ValueError:
            pass
    return redirect(url_for('admin.admin'))
