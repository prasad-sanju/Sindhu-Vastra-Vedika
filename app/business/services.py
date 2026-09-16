from app.data.repositories import ProductRepository, UserRepository, OrderRepository
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class ProductService:
    @staticmethod
    def list_products(category=None):
        return ProductRepository.all(category)

    @staticmethod
    def get_product(product_id):
        return ProductRepository.get(product_id)

class AuthService:
    @staticmethod
    def register(name, email, password):
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters')
        if UserRepository.find_by_email(email):
            raise ValueError('Email already registered')
        return UserRepository.create(name, email, generate_password_hash(password))

    @staticmethod
    def authenticate(email, password):
        user = UserRepository.find_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

class OrderService:
    @staticmethod
    def checkout(user_id, cart):
        if not cart:
            raise ValueError('Cart is empty')
        items, total = [], 0.0
        for product_id, quantity in cart.items():
            product = ProductRepository.get(int(product_id))
            if not product:
                raise ValueError('Product not found')
            if product.stock < quantity:
                raise ValueError(f'Insufficient stock for {product.name}')
            total += product.price * quantity
            items.append({'product_id': product.id, 'quantity': quantity, 'unit_price': product.price})
        for product_id, quantity in cart.items():
            ProductRepository.get(int(product_id)).stock -= quantity
        return OrderRepository.create(user_id, total, items)
