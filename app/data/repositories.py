from app import db
from app.data.models import Product, User, Order, OrderItem

class ProductRepository:
    @staticmethod
    def all(category=None):
        q = Product.query
        if category:
            q = q.filter_by(category=category)
        return q.order_by(Product.id.desc()).all()

    @staticmethod
    def get(product_id):
        return db.session.get(Product, product_id)

class UserRepository:
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email.lower()).first()

    @staticmethod
    def create(name, email, password_hash):
        user = User(name=name, email=email.lower(), password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

class OrderRepository:
    @staticmethod
    def create(user_id, total, items):
        order = Order(user_id=user_id, total=total)
        db.session.add(order)
        db.session.flush()
        for item in items:
            db.session.add(OrderItem(order_id=order.id, **item))
        db.session.commit()
        return order

    @staticmethod
    def for_user(user_id):
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
