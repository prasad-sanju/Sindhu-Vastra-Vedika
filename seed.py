from app import create_app, db
from app.data.models import Product

app = create_app()
products = [
 ('Banarasi Silk Saree','Women','Elegant traditional silk saree.',5499,20),
 ('Cotton Anarkali Dress','Women','Comfortable cotton ethnic dress.',2199,30),
 ('Festive Lehenga Set','Girls','Festive lehenga for girls.',2899,25),
 ('Girls Traditional Frock','Girls','Stylish traditional frock.',1599,35),
 ('Designer Kurti','Women','Contemporary everyday kurti.',1299,40),
 ('Pattu Pavada Set','Girls','Traditional pattu pavada set.',2399,20),
]
with app.app_context():
    if Product.query.count() == 0:
        for n,c,d,p,s in products: db.session.add(Product(name=n,category=c,description=d,price=p,stock=s))
        db.session.commit()
        print('Seed data inserted')
    else: print('Products already exist')
