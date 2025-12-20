from flask import Blueprint, render_template, request, redirect, url_for, session
from models import get_products, add_order, apply_promo_discount, get_user_orders, add_to_wishlist, remove_from_wishlist, get_user_wishlist

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop():
    return render_template('shop.html')

@shop_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    products = get_products()
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        cart = session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += 1
        else:
            cart[str(product_id)] = {
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': 1
            }
        session['cart'] = cart
    return redirect(url_for('shop.shop'))

@shop_bp.route('/cart')
def cart():
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    promo_code = session.get('promo_code', '')
    discount = 0
    discounted_total = total
    promo_error = None

    if promo_code:
        discounted_total, discount, promo_error = apply_promo_discount(total, promo_code)
        if promo_error:
            session.pop('promo_code', None)  # Remove invalid code from session

    return render_template('cart.html', cart=cart, total=total, discounted_total=discounted_total,
                         discount=discount, promo_code=promo_code, promo_error=promo_error)

@shop_bp.route('/apply_promo', methods=['POST'])
def apply_promo():
    promo_code = request.form.get('promo_code', '').strip()
    if promo_code:
        session['promo_code'] = promo_code
    else:
        session.pop('promo_code', None)
    return redirect(url_for('shop.cart'))

@shop_bp.route('/remove_promo')
def remove_promo():
    session.pop('promo_code', None)
    return redirect(url_for('shop.cart'))

@shop_bp.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', {})
    email = request.form['email']
    address = request.form['address']

    # Calculate total with potential promo discount
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    promo_code = session.get('promo_code', '')
    final_total = total
    if promo_code:
        discounted_total, _, _ = apply_promo_discount(total, promo_code)
        final_total = discounted_total

    add_order(email, address, cart, final_total)  # Need to update add_order to accept total
    session['cart'] = {}
    session.pop('promo_code', None)  # Clear promo code after checkout
    return redirect(url_for('shop.shop'))


@shop_bp.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    orders = get_user_orders(user_id)
    wishlist = get_user_wishlist(user_id)
    return render_template('account.html', orders=orders, wishlist=wishlist)


@shop_bp.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist_route(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    add_to_wishlist(session['user_id'], product_id)
    return redirect(request.referrer or url_for('shop.shop'))


@shop_bp.route('/remove_from_wishlist/<int:product_id>')
def remove_from_wishlist_route(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    remove_from_wishlist(session['user_id'], product_id)
    return redirect(url_for('shop.account'))
