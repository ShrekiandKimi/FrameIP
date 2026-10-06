"""Класс Order и функции работы с коллекцией заказов."""

from .clients import Client
from .couriers import COURIERS, Courier
from .dishes import Dish, find_dish_by_id

DISCOUNT_THRESHOLD = 1000
DISCOUNT_RATE = 0.1
DELIVERY_COST = 150


class Order:
    """Заказ клиента на доставку готовой еды."""

    def __init__(
        self,
        order_id: int,
        client: Client,
        items: dict[int, int],
        total: float,
        courier: Courier | None,
        status: str,
    ) -> None:
        """Создать объект заказа, связанный с клиентом и курьером."""
        self.id = order_id
        self.client = client
        self.items = items
        self.total = total
        self.courier = courier
        self.status = status

    def cancel(self) -> None:
        """Отменить заказ: снять курьера и изменить статус."""
        self.status = "отменён"
        self.courier = None

    def __str__(self) -> str:
        """Вернуть строковое представление заказа."""
        courier_name = self.courier.name if self.courier else "не назначен"
        return (
            f"Заказ №{self.id} ({self.client.name}): "
            f"{self.total} руб., курьер: {courier_name}, "
            f"статус: {self.status}"
        )


def calculate_order_total(dishes: list[Dish], items: dict[int, int]) -> float:
    """Подсчитать стоимость заказа по выбранным блюдам и количеству."""
    total = 0.0
    for dish_id, quantity in items.items():
        dish = find_dish_by_id(dishes, dish_id)
        if dish is None:
            raise KeyError(f"Блюдо с id={dish_id} не найдено")
        total += dish.price * quantity
    return total


def apply_discount(total: float) -> float:
    """Применить скидку к сумме заказа при крупном заказе."""
    if total >= DISCOUNT_THRESHOLD:
        return total - total * DISCOUNT_RATE
    return total


def get_delivery_cost(total: float) -> int:
    """Рассчитать стоимость доставки в зависимости от суммы заказа."""
    if total >= DISCOUNT_THRESHOLD:
        return 0
    return DELIVERY_COST


def is_courier_busy(orders: list[Order], courier: Courier) -> bool:
    """Проверить, занят ли курьер доставкой другого активного заказа."""
    return any(
        order.courier is not None
        and order.courier.id == courier.id
        and order.status != "отменён"
        for order in orders
    )


def assign_courier(orders: list[Order]) -> Courier | None:
    """Найти свободного курьера среди списка курьеров сервиса."""
    for courier in COURIERS:
        if not is_courier_busy(orders, courier):
            return courier
    return None


def get_order_status(courier: Courier | None) -> str:
    """Вернуть текстовый статус заказа в зависимости от назначения курьера."""
    if courier:
        return "заказ передан курьеру"
    return "ожидает назначения курьера"


def create_order(
    orders: list[Order],
    dishes: list[Dish],
    client: Client,
    items: dict[int, int],
) -> Order:
    """Создать новый заказ, связать его с клиентом и курьером."""
    total = calculate_order_total(dishes, items)
    discounted_total = apply_discount(total)
    delivery_cost = get_delivery_cost(discounted_total)
    courier = assign_courier(orders)

    order_id = max((order.id for order in orders), default=0) + 1
    order = Order(
        order_id=order_id,
        client=client,
        items=items,
        total=discounted_total + delivery_cost,
        courier=courier,
        status="в обработке" if courier else "ожидает курьера",
    )
    orders.append(order)
    return order


def find_order_by_id(orders: list[Order], order_id: int) -> Order | None:
    """Найти заказ по идентификатору."""
    for order in orders:
        if order.id == order_id:
            return order
    return None


def cancel_order(orders: list[Order], order_id: int) -> bool:
    """Отменить заказ по идентификатору. Вернуть True при успехе."""
    for order in orders:
        if order.id == order_id:
            order.cancel()
            return True
    return False


def get_unique_clients(orders: list[Order]) -> set[str]:
    """Вернуть множество уникальных имён клиентов, оформивших заказы."""
    return {order.client.name for order in orders}


def get_total_revenue(orders: list[Order]) -> float:
    """Подсчитать суммарную выручку по всем незаменённым заказам."""
    return sum(order.total for order in orders if order.status != "отменён")


def show_orders(orders: list[Order]) -> None:
    """Вывести список заказов."""
    if not orders:
        print("Заказов пока нет.")
        return
    for order in orders:
        print(order)
