"""Функции сохранения и загрузки данных проекта в формате JSON."""

import json


def load_dishes(filename: str) -> dict[int, dict]:
    """Загрузить блюда из JSON-файла.

    При отсутствии файла или повреждённых данных возвращает
    пустой словарь вместо аварийного завершения программы.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            raw_dishes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return {dish["id"]: {"name": dish["name"], "price": dish["price"]}
            for dish in raw_dishes}


def save_dishes(filename: str, dishes: dict[int, dict]) -> None:
    """Сохранить блюда в JSON-файл."""
    raw_dishes = [
        {"id": dish_id, "name": dish["name"], "price": dish["price"]}
        for dish_id, dish in dishes.items()
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(raw_dishes, file, ensure_ascii=False, indent=2)


def load_orders(filename: str) -> list[dict]:
    """Загрузить заказы из JSON-файла.

    При отсутствии файла или повреждённых данных возвращает
    пустой список вместо аварийного завершения программы.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            orders = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    for order in orders:
        order["items"] = {int(k): v for k, v in order["items"].items()}
    return orders


def save_orders(filename: str, orders: list[dict]) -> None:
    """Сохранить заказы в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=2)
