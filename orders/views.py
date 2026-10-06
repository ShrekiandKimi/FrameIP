from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models import Order
from models.dishes import find_dish_by_id
from models.orders import assign_courier, find_order_by_id
from storage import load_clients, load_dishes, load_orders

DISHES_FILE = str(settings.DATA_DIR / "dishes.json")
CLIENTS_FILE = str(settings.DATA_DIR / "clients.json")
ORDERS_FILE = str(settings.DATA_DIR / "orders.json")

STATUS_BADGES = {
    "в обработке": "bg-success",
    "ожидает курьера": "bg-warning text-dark",
    "отменён": "bg-secondary",
}


def _badge(order: Order) -> str:
    """Вернуть HTML-бейдж со статусом заказа."""
    css_class = STATUS_BADGES.get(order.status, "bg-light text-dark")
    return f'<span class="badge {css_class}">{escape(order.status)}</span>'


def _load_orders() -> list[Order]:
    """Загрузить заказы вместе со связанными клиентами и курьерами."""
    return load_orders(ORDERS_FILE, load_clients(CLIENTS_FILE))


def orders(request: HttpRequest) -> HttpResponse:
    """Страница /orders/: список заказов и наличие свободного курьера."""
    orders_list = _load_orders()
    items = ""
    for order in orders_list:
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/orders/{order.id}/">
                Заказ №{order.id} – {escape(order.client.name)}
            </a>
            {_badge(order)}
        </li>
        """
    if not items:
        items = '<li class="list-group-item">Заказов пока нет.</li>'

    courier = assign_courier(orders_list)
    if courier is None:
        courier_info = '<span class="badge bg-danger">нет свободных курьеров</span>'
    else:
        courier_info = (
            f'<span class="badge bg-success">{escape(courier.name)}</span>'
        )
    content = f"""
    <h1>Заказы</h1>
    <p>Свободный курьер для нового заказа: {courier_info}</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Доставка еды – заказы", content))


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Страница /orders/<id>/: карточка заказа; 404, если заказ не найден."""
    order = find_order_by_id(_load_orders(), order_id)
    if order is None:
        content = """
        <h1 class="text-danger">Заказ не найден</h1>
        <a href="/orders/" class="btn btn-outline-secondary">
            ← к списку заказов
        </a>
        """
        return HttpResponse(page("Заказ не найден", content), status=404)

    dishes_list = load_dishes(DISHES_FILE)
    positions = ""
    for dish_id, quantity in order.items.items():
        dish = find_dish_by_id(dishes_list, dish_id)
        name = escape(dish.name) if dish else f"блюдо №{dish_id}"
        positions += f"<li>{name} × {quantity}</li>"

    courier_name = escape(order.courier.name) if order.courier else "не назначен"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Заказ №{order.id}</h5>
            <p class="card-text">Клиент: {escape(order.client.name)}</p>
            <p class="card-text">Курьер: {courier_name}</p>
            <p class="card-text">Состав заказа:</p>
            <ul>{positions}</ul>
            <p class="card-text">Итого к оплате: {order.total} руб.</p>
            <p class="card-text">Статус: {_badge(order)}</p>
            <a href="/orders/" class="btn btn-outline-secondary">
                ← к списку заказов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Заказ №{order.id}", content), status=200)
