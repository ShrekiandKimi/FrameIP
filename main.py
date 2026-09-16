"""Точка запуска сервиса доставки готовой еды."""

import sys

from dishes import (
    add_dish,
    filter_dishes_by_price,
    find_dish,
    sort_dishes,
)
from orders import (
    cancel_order,
    create_order,
    get_order_status,
    get_total_revenue,
    get_unique_clients,
)
from storage import load_dishes, load_orders, save_dishes, save_orders
from utils import input_float, input_int

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

DISHES_FILE = "data/dishes.json"
ORDERS_FILE = "data/orders.json"


def show_dishes(dishes: dict[int, dict]) -> None:
    """Вывести список блюд меню."""
    if not dishes:
        print("Меню пусто.")
        return
    for dish_id, dish in sort_dishes(dishes):
        print(f"{dish_id}. {dish['name']} — {dish['price']} руб.")


def show_orders(orders: list[dict]) -> None:
    """Вывести список заказов."""
    if not orders:
        print("Заказов пока нет.")
        return
    for order in orders:
        print(
            f"Заказ №{order['id']} ({order['client_name']}): "
            f"{order['total']} руб., курьер: {order['courier']}, "
            f"статус: {order['status']}"
        )


def show_statistics(orders: list[dict]) -> None:
    """Вывести краткую статистику по заказам."""
    print(f"Всего заказов: {len(orders)}")
    print(f"Уникальных клиентов: {len(get_unique_clients(orders))}")
    print(f"Суммарная выручка: {get_total_revenue(orders)} руб.")


def order_dishes_menu(dishes: dict[int, dict]) -> dict[int, int]:
    """Опросить пользователя о составе заказа и вернуть словарь items."""
    items: dict[int, int] = {}
    while True:
        dish_id = input_int("ID блюда (0 — закончить выбор): ")
        if dish_id == 0:
            break
        if dish_id not in dishes:
            print("Блюдо с таким ID не найдено.")
            continue
        quantity = input_int("Количество: ")
        items[dish_id] = items.get(dish_id, 0) + quantity
    return items


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    dishes = load_dishes(DISHES_FILE)
    orders = load_orders(ORDERS_FILE)

    if not dishes:
        add_dish(dishes, "Пицца Маргарита", 590.0)
        add_dish(dishes, "Ролл Калифорния", 450.0)
        add_dish(dishes, "Салат Цезарь", 320.0)

    menu = """
=== Сервис доставки готовой еды ===
1. Показать меню
2. Найти блюдо по названию
3. Показать блюда дешевле суммы
4. Оформить заказ
5. Отменить заказ
6. Показать заказы
7. Показать статистику
0. Выход
"""

    while True:
        print(menu)
        choice = input("Выберите действие: ")

        if choice == "1":
            show_dishes(dishes)
        elif choice == "2":
            query = input("Название блюда (или часть): ")
            show_dishes(find_dish(dishes, query))
        elif choice == "3":
            max_price = input_float("Максимальная цена: ")
            show_dishes(filter_dishes_by_price(dishes, max_price))
        elif choice == "4":
            client_name = input("Имя клиента: ")
            items = order_dishes_menu(dishes)
            if not items:
                print("Заказ не может быть пустым.")
                continue
            try:
                order = create_order(orders, dishes, client_name, items)
            except KeyError as error:
                print(f"Ошибка при оформлении заказа: {error}")
                continue
            print(f"Заказ №{order['id']} оформлен.")
            print(get_order_status(order["courier"]))
        elif choice == "5":
            order_id = input_int("ID заказа для отмены: ")
            if cancel_order(orders, order_id):
                print("Заказ отменён.")
            else:
                print("Заказ с таким ID не найден.")
        elif choice == "6":
            show_orders(orders)
        elif choice == "7":
            show_statistics(orders)
        elif choice == "0":
            save_dishes(DISHES_FILE, dishes)
            save_orders(ORDERS_FILE, orders)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
