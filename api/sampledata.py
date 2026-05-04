from .dependencies.database import SessionLocal
from .models.customers import Customer
from .models.menu_items import MenuItem
from .models.orders import Order
from .models.order_details import OrderDetail
from .models.payments import Payment
from .models.promotions import Promotion
from .models.resources import Resource
from .models.ratings import Rating

def data():
    db = SessionLocal()

    if db.query(Customer).first():
        db.close()
        return

    print("Adding Sample data")
    c1 = Customer(name="John", email="John@gmail.com", phone="1231231234", address="9201 University City Blvd., Charlotte, NC 28223-0001")
    c2 = Customer(name="Luke", email="Luke@gmail.com", phone="2342342345", address="9201 University City Blvd., Charlotte, NC 28223-0001")
    db.add_all([c1, c2])
    db.commit()

    m1 = MenuItem(item_name="Burger", price=12, calories=850, category="Food")
    m2 = MenuItem(item_name="Wrap", price=10, calories=650, category="Food")
    db.add_all([m1, m2])
    db.commit()

    r1 = Resource(resource_name="Buns", amount=50, unit="Pack of 8", cost_per_unit=5)
    r2 = Resource(resource_name="Chicken", amount=80, unit="lbs", cost_per_unit=4)
    db.add_all([r1, r2])
    db.commit()

    o1 = Order(customer_id=c1.id, tracking_number="2312", status="Out for delivery", total_price=26, order_type="Delivery")
    o2 = Order(customer_id=c2.id, tracking_number="2313", status="Ready for pickup", total_price=22, order_type="Pickup")
    db.add_all([o1, o2])
    db.commit()

    or1 = OrderDetail(order_id=o1.id, menu_item_id=m1.id, quantity=2, price=24)
    or2 = OrderDetail(order_id=o2.id, menu_item_id=m2.id, quantity=2, price=20)
    db.add_all([or1, or2])
    db.commit()

    p1 = Payment(order_id=o1.id, payment_type="credit card", amount="26", transaction_status="completed")
    db.add(p1)
    db.commit()

    promo = Promotion(code="FirstORDER", discount=20, is_active=True)
    db.add(promo)
    db.commit()

    r1 = Rating(customer_id=c1.id, review_text="Great Food", score=5)
    r2 = Rating(customer_id=c2.id, review_text="Food was alright", score=3)
    db.add_all([r1, r2])
    db.commit()

    db.close()
    print("Done with adding sample data")