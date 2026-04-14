from . import (
    orders,
    order_details,
    menu_items,
    resources,
    customers,
    ratings,
    payments,
    promotions
)

from ..dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)

    customers.Base.metadata.create_all(engine)
    ratings.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    promotions.Base.metadata.create_all(engine)