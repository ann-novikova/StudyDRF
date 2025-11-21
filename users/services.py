import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создает курс в stripe"""
    name = getattr(course, "name", str(course))
    return stripe.Product.create(name=name)


def create_stripe_price(amount, product, currency="rub"):
    """Создает цену на курс в stripe"""
    unit_amount = int(float(amount) * 100)

    product_id = getattr(product, "id", None)
    if product_id:
        return stripe.Price.create(
            currency=currency,
            unit_amount=unit_amount,
            product=product_id,
        )

    return stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount,
        product_data={"name": getattr(product, "name", str(product))},
    )


def create_session(price):
    """Создает сессию на оплату курса в stripe"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/study/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def change_get_status(session_id):
    """Создает статус оплаты в stripe"""

    return stripe.checkout.Session.retrieve(session_id).get("payment_status")
