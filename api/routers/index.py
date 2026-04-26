from . import orders, order_details, menu, promotions, ratings, analytics


def load_routes(app):
    app.include_router(menu.router)
    app.include_router(promotions.router)
    app.include_router(orders.router)
    app.include_router(order_details.router)
    app.include_router(ratings.router)
    app.include_router(analytics.router)