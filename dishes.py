"""Функции для работы с меню (блюдами) сервиса доставки еды."""


def add_dish(dishes: dict[int, dict], name: str, price: float) -> None:
    """Добавить блюдо в словарь dishes."""
    dish_id = max(dishes.keys(), default=0) + 1
    dishes[dish_id] = {"name": name, "price": price}


def find_dish(dishes: dict[int, dict], query: str) -> dict[int, dict]:
    """Найти блюда, в названии которых встречается подстрока query."""
    query = query.lower()
    return {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if query in dish["name"].lower()
    }


def check_dish_price(
    dishes: dict[int, dict], dish_id: int, max_price: float
) -> bool:
    """Проверить, что цена блюда не превышает max_price."""
    dish = dishes.get(dish_id)
    if dish is None:
        raise KeyError(f"Блюдо с id={dish_id} не найдено")
    return dish["price"] <= max_price


def filter_dishes_by_price(
    dishes: dict[int, dict], max_price: float
) -> dict[int, dict]:
    """Отобрать блюда, цена которых не превышает max_price."""
    return {
        dish_id: dish
        for dish_id, dish in dishes.items()
        if dish["price"] <= max_price
    }


def sort_dishes(dishes: dict[int, dict]) -> list[tuple[int, dict]]:
    """Вернуть блюда, отсортированные по цене (по возрастанию)."""
    return sorted(dishes.items(), key=lambda item: item[1]["price"])
