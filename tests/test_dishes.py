from dishes import (
    add_dish,
    check_dish_price,
    filter_dishes_by_price,
    find_dish,
    sort_dishes,
)


def test_add_dish():
    dishes = {}
    add_dish(dishes, "Пицца Маргарита", 590.0)
    assert len(dishes) == 1


def test_find_dish():
    dishes = {}
    add_dish(dishes, "Пицца Маргарита", 590.0)
    assert find_dish(dishes, "пицца")


def test_check_dish_price():
    dishes = {}
    add_dish(dishes, "Салат Цезарь", 320.0)
    assert check_dish_price(dishes, 1, 350.0)
    assert not check_dish_price(dishes, 1, 300.0)


def test_filter_dishes_by_price():
    dishes = {}
    add_dish(dishes, "Салат Цезарь", 320.0)
    add_dish(dishes, "Пицца Маргарита", 590.0)
    cheap_dishes = filter_dishes_by_price(dishes, 400.0)
    assert len(cheap_dishes) == 1


def test_sort_dishes():
    dishes = {}
    add_dish(dishes, "Пицца Маргарита", 590.0)
    add_dish(dishes, "Салат Цезарь", 320.0)
    sorted_dishes = sort_dishes(dishes)
    assert sorted_dishes[0][1]["name"] == "Салат Цезарь"
