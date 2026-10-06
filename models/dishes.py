"""Класс Dish и функции работы с коллекцией блюд меню."""


class Dish:
    """Блюдо меню сервиса доставки готовой еды."""

    def __init__(self, dish_id: int, name: str, price: float) -> None:
        """Создать объект блюда."""
        self.id = dish_id
        self.name = name
        self.price = price

    def is_affordable(self, max_price: float) -> bool:
        """Проверить, что цена блюда не превышает max_price."""
        return self.price <= max_price

    def matches(self, query: str) -> bool:
        """Проверить вхождение подстроки query в название блюда."""
        return query.lower() in self.name.lower()

    @staticmethod
    def validate_price(price: float) -> bool:
        """Проверить корректность цены блюда."""
        return price > 0

    @classmethod
    def from_data(cls, data: dict) -> "Dish":
        """Создать блюдо из словаря данных (например, из JSON)."""
        return cls(data["id"], data["name"], data["price"])

    def __str__(self) -> str:
        """Вернуть строковое представление блюда."""
        return f"{self.name} — {self.price} руб."


def add_dish(dishes: list[Dish], name: str, price: float) -> Dish:
    """Создать блюдо и добавить его в коллекцию dishes."""
    if not Dish.validate_price(price):
        raise ValueError("Цена блюда должна быть положительной")
    dish_id = max((dish.id for dish in dishes), default=0) + 1
    dish = Dish(dish_id, name, price)
    dishes.append(dish)
    return dish


def find_dish_by_id(dishes: list[Dish], dish_id: int) -> Dish | None:
    """Найти блюдо по идентификатору."""
    for dish in dishes:
        if dish.id == dish_id:
            return dish
    return None


def find_dish(dishes: list[Dish], query: str) -> list[Dish]:
    """Найти блюда, в названии которых встречается подстрока query."""
    return [dish for dish in dishes if dish.matches(query)]


def filter_dishes_by_price(dishes: list[Dish], max_price: float) -> list[Dish]:
    """Отобрать блюда, цена которых не превышает max_price."""
    return [dish for dish in dishes if dish.is_affordable(max_price)]


def sort_dishes(dishes: list[Dish]) -> list[Dish]:
    """Вернуть блюда, отсортированные по цене (по возрастанию)."""
    return sorted(dishes, key=lambda dish: dish.price)


def show_dishes(dishes: list[Dish]) -> None:
    """Вывести список блюд меню."""
    if not dishes:
        print("Меню пусто.")
        return
    for dish in sort_dishes(dishes):
        print(f"{dish.id}. {dish}")
