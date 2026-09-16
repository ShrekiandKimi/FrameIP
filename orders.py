"""Функции для создания и обработки заказов сервиса доставки еды."""

DISCOUNT_THRESHOLD = 1000
DISCOUNT_RATE = 0.1
DELIVERY_COST = 150

COURIERS = ["Алексей Сидоров", "Мария Кузнецова", "Дмитрий Волков"]


def calculate_order_total(dishes: dict[int, dict], items: dict[int, int]) -> float:
    """Подсчитать стоимость заказа по выбранным блюдам и количеству."""
    total = 0.0
    for dish_id, quantity in items.items():
        dish = dishes.get(dish_id)
        if dish is None:
            raise KeyError(f"Блюдо с id={dish_id} не найдено")
        total += dish["price"] * quantity
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


def is_courier_busy(orders: list[dict], courier_name: str) -> bool:
    """Проверить, занят ли курьер доставкой другого активного заказа."""
    return any(
        order["courier"] == courier_name and order["status"] != "доставлен"
        for order in orders
    )


def assign_courier(orders: list[dict]) -> str | None:
    """Найти свободного курьера среди списка курьеров сервиса."""
    for courier_name in COURIERS:
        if not is_courier_busy(orders, courier_name):
            return courier_name
    return None


def get_order_status(courier: str | None) -> str:
    """Вернуть текстовый статус заказа в зависимости от назначения курьера."""
    if courier:
        return "заказ передан курьеру"
    return "ожидает назначения курьера"


def create_order(
    orders: list[dict],
    dishes: dict[int, dict],
    client_name: str,
    items: dict[int, int],
) -> dict:
    """Создать новый заказ и добавить его в список orders."""
    total = calculate_order_total(dishes, items)
    discounted_total = apply_discount(total)
    delivery_cost = get_delivery_cost(discounted_total)
    courier = assign_courier(orders)

    order_id = max((order["id"] for order in orders), default=0) + 1
    order = {
        "id": order_id,
        "client_name": client_name,
        "items": items,
        "total": discounted_total + delivery_cost,
        "courier": courier,
        "status": "в обработке" if courier else "ожидает курьера",
    }
    orders.append(order)
    return order


def cancel_order(orders: list[dict], order_id: int) -> bool:
    """Отменить заказ по идентификатору. Вернуть True при успехе."""
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "отменён"
            order["courier"] = None
            return True
    return False


def get_unique_clients(orders: list[dict]) -> set[str]:
    """Вернуть множество уникальных имён клиентов, оформивших заказы."""
    return {order["client_name"] for order in orders}


def get_total_revenue(orders: list[dict]) -> float:
    """Подсчитать суммарную выручку по всем незаменённым заказам."""
    return sum(
        order["total"] for order in orders if order["status"] != "отменён"
    )
