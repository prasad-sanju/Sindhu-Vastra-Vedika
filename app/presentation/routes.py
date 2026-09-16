from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from app.business.services import ProductService, OrderService
from app.data.repositories import OrderRepository

main_bp = Blueprint('main', __name__)

@main_bp.get('/')
def home():
    category = request.args.get('category')
    return render_template('index.html', products=ProductService.list_products(category), category=category)

@main_bp.get('/product/<int:product_id>')
def product_detail(product_id):
    product = ProductService.get_product(product_id)
    return render_template('product.html', product=product) if product else ('Product not found', 404)

@main_bp.get('/cart')
def cart():
    products, total = [], 0
    for product_id, quantity in session.get('cart', {}).items():
        product = ProductService.get_product(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            products.append((product, quantity, subtotal))
    return render_template('cart.html', products=products, total=total)

@main_bp.post('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    product = ProductService.get_product(product_id)
    if not product:
        return 'Product not found', 404
    cart = session.get('cart', {})
    key = str(product_id)
    new_qty = cart.get(key, 0) + 1
    if new_qty > product.stock:
        flash('Insufficient stock')
    else:
        cart[key] = new_qty
        session['cart'] = cart
        flash('Product added to cart')
    return redirect(request.referrer or url_for('main.home'))

@main_bp.post('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('main.cart'))

@main_bp.post('/checkout')
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    try:
        OrderService.checkout(session['user_id'], session.get('cart', {}))
        session['cart'] = {}
        flash('Order placed successfully')
    except ValueError as exc:
        flash(str(exc))
    return redirect(url_for('main.orders'))

@main_bp.get('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('orders.html', orders=OrderRepository.for_user(session['user_id']))

@main_bp.get('/health')
def health():
    return jsonify(status='healthy')
