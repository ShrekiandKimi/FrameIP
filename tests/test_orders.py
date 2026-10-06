from models.clients import add_client
from models.dishes import add_dish
from models.orders import (
    apply_discount,
    calculate_order_total,
    cancel_order,
    create_order,
    get_delivery_cost,
    get_order_status,
)


def test_calculate_order_total():
    dishes = []
    add_dish(dishes, "Пицца Маргарита", 590.0)
    assert calculate_order_total(dishes, {1: 2}) == 1180.0


def test_apply_discount():
    assert apply_discount(1180.0) == 1062.0
    assert apply_discount(500.0) == 500.0


def test_get_delivery_cost():
    assert get_delivery_cost(1200.0) == 0
    assert get_delivery_cost(500.0) == 150


def test_create_order_assigns_courier():
    dishes = []
    add_dish(dishes, "Салат Цезарь", 320.0)
    clients = []
    client = add_client(clients, "Иван Петров")
    orders = []
    order = create_order(orders, dishes, client, {1: 1})
    assert order.courier is not None
    assert order.client is client
    assert get_order_status(order.courier) == "заказ передан курьеру"


def test_cancel_order_frees_courier():
    dishes = []
    add_dish(dishes, "Салат Цезарь", 320.0)
    clients = []
    client = add_client(clients, "Иван Петров")
    orders = []
    order = create_order(orders, dishes, client, {1: 1})

    assert cancel_order(orders, order.id)
    assert orders[0].status == "отменён"
    assert orders[0].courier is None


def test_fourth_order_waits_for_free_courier():
    dishes = []
    add_dish(dishes, "Салат Цезарь", 320.0)
    clients = []
    client = add_client(clients, "Иван Петров")
    orders = []
    for _ in range(3):
        create_order(orders, dishes, client, {1: 1})

    fourth_order = create_order(orders, dishes, client, {1: 1})

    assert fourth_order.courier is None
    assert fourth_order.status == "ожидает курьера"


def test_cancelled_order_frees_courier_for_new_order():
    dishes = []
    add_dish(dishes, "Салат Цезарь", 320.0)
    clients = []
    client = add_client(clients, "Иван Петров")
    orders = []
    booked_orders = [create_order(orders, dishes, client, {1: 1}) for _ in range(3)]
    waiting_order = create_order(orders, dishes, client, {1: 1})
    assert waiting_order.courier is None

    cancel_order(orders, booked_orders[0].id)
    new_order = create_order(orders, dishes, client, {1: 1})

    assert new_order.courier is not None
