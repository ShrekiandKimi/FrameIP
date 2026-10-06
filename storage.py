"""Функции сохранения и загрузки объектов проекта в формате JSON."""

import json

from models import Client, Dish, Order
from models.clients import find_client_by_id
from models.couriers import COURIERS, Courier


def load_dishes(filename: str) -> list[Dish]:
    """Загрузить блюда из JSON-файла и создать объекты Dish.

    При отсутствии файла или повреждённых данных возвращает
    пустой список вместо аварийного завершения программы.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            raw_dishes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return [Dish.from_data(item) for item in raw_dishes]


def save_dishes(filename: str, dishes: list[Dish]) -> None:
    """Сохранить объекты Dish в JSON-файл."""
    raw_dishes = [
        {"id": dish.id, "name": dish.name, "price": dish.price} for dish in dishes
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_dishes, file, ensure_ascii=False, indent=2)


def load_clients(filename: str) -> list[Client]:
    """Загрузить клиентов из JSON-файла и создать объекты Client.

    При отсутствии файла или повреждённых данных возвращает
    пустой список вместо аварийного завершения программы.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            raw_clients = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return [Client.from_data(item) for item in raw_clients]


def save_clients(filename: str, clients: list[Client]) -> None:
    """Сохранить объекты Client в JSON-файл."""
    raw_clients = [{"id": client.id, "name": client.name} for client in clients]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_clients, file, ensure_ascii=False, indent=2)


def _find_courier_by_id(courier_id: int | None) -> Courier | None:
    """Найти курьера по идентификатору среди фиксированного списка COURIERS."""
    if courier_id is None:
        return None
    for courier in COURIERS:
        if courier.id == courier_id:
            return courier
    return None


def load_orders(filename: str, clients: list[Client]) -> list[Order]:
    """Загрузить заказы из JSON-файла, восстановив связи с Client и Courier.

    При отсутствии файла, повреждённых данных или отсутствии связанного
    клиента запись пропускается вместо аварийного завершения программы.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            raw_orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    orders: list[Order] = []
    for data in raw_orders:
        client = find_client_by_id(clients, data["client_id"])
        if client is None:
            continue
        items = {int(dish_id): qty for dish_id, qty in data["items"].items()}
        order = Order(
            order_id=data["id"],
            client=client,
            items=items,
            total=data["total"],
            courier=_find_courier_by_id(data["courier_id"]),
            status=data["status"],
        )
        orders.append(order)
    return orders


def save_orders(filename: str, orders: list[Order]) -> None:
    """Сохранить объекты Order в JSON-файл (со ссылками по id)."""
    raw_orders = [
        {
            "id": order.id,
            "client_id": order.client.id,
            "items": order.items,
            "total": order.total,
            "courier_id": order.courier.id if order.courier else None,
            "status": order.status,
        }
        for order in orders
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_orders, file, ensure_ascii=False, indent=2)
