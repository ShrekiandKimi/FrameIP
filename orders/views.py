from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models import Order
from models.dishes import find_dish_by_id
from models.orders import assign_courier, find_order_by_id
from storage import load_clients, load_dishes, load_orders

DISHES_FILE = str(settings.DATA_DIR / "dishes.json")
CLIENTS_FILE = str(settings.DATA_DIR / "clients.json")
ORDERS_FILE = str(settings.DATA_DIR / "orders.json")


def _load_orders() -> list[Order]:
    """Загрузить заказы вместе со связанными клиентами и курьерами."""
    return load_orders(ORDERS_FILE, load_clients(CLIENTS_FILE))


def orders(request: HttpRequest) -> HttpResponse:
    """Страница /orders/: список заказов и наличие свободного курьера."""
    orders_list = _load_orders()

    context = {
        "orders": orders_list,
        "free_courier": assign_courier(orders_list),
    }
    return render(request, "orders/order_list.html", context)


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Страница /orders/<id>/: карточка заказа; 404, если заказ не найден."""
    order = find_order_by_id(_load_orders(), order_id)

    positions = []
    if order is not None:
        dishes_list = load_dishes(DISHES_FILE)
        for dish_id, quantity in order.items.items():
            dish = find_dish_by_id(dishes_list, dish_id)
            positions.append(
                {
                    "name": dish.name if dish else f"блюдо №{dish_id}",
                    "quantity": quantity,
                }
            )

    context = {
        "order": order,
        "positions": positions,
    }
    return render(
        request,
        "orders/order_detail.html",
        context,
        status=404 if order is None else 200,
    )
