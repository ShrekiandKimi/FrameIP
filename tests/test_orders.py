from dishes import add_dish
from orders import (
    apply_discount,
    calculate_order_total,
    cancel_order,
    create_order,
    get_delivery_cost,
    get_order_status,
)


def test_calculate_order_total():
    dishes = {}
    add_dish(dishes, "Пицца Маргарита", 590.0)
    assert calculate_order_total(dishes, {1: 2}) == 1180.0


def test_apply_discount():
    assert apply_discount(1180.0) == 1062.0
    assert apply_discount(500.0) == 500.0


def test_get_delivery_cost():
    assert get_delivery_cost(1200.0) == 0
    assert get_delivery_cost(500.0) == 150


def test_create_order_assigns_courier():
    dishes = {}
    add_dish(dishes, "Салат Цезарь", 320.0)
    orders = []
    order = create_order(orders, dishes, "Иван Петров", {1: 1})
    assert order["courier"] is not None
    assert get_order_status(order["courier"]) == "заказ передан курьеру"


def test_cancel_order():
    dishes = {}
    add_dish(dishes, "Салат Цезарь", 320.0)
    orders = []
    order = create_order(orders, dishes, "Иван Петров", {1: 1})
    assert cancel_order(orders, order["id"])
    assert orders[0]["status"] == "отменён"
