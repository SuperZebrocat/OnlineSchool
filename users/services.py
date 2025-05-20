import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_usd(amount):
    """Конвертирует рубли в доллары."""
    c = CurrencyRates()
    rate = c.get_rate("RUB", "USD")
    return int(amount * rate)


def create_stripe_price(payment):
    """Создание цены в страйпе."""
    product_name = ""
    if payment.course:
        product_name = payment.course.name
    elif payment.lesson:
        product_name = payment.lesson.name

    return stripe.Price.create(currency="rub", unit_amount=payment.amount * 100, product_data={"name": product_name})


def create_stripe_session(price):
    """Создание сессии в страйпе."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
