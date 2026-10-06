import pytest

from models.dishes import (
    add_dish,
    filter_dishes_by_price,
    find_dish,
    sort_dishes,
)


def test_add_dish():
    dishes = []
    dish = add_dish(dishes, "Пицца Маргарита", 590.0)
    assert len(dishes) == 1
    assert dish.id == 1


def test_dish_is_affordable():
    dishes = []
    add_dish(dishes, "Салат Цезарь", 320.0)
    assert dishes[0].is_affordable(350.0)
    assert not dishes[0].is_affordable(300.0)


def test_find_dish():
    dishes = []
    add_dish(dishes, "Пицца Маргарита", 590.0)
    assert find_dish(dishes, "пицца")


def test_filter_dishes_by_price():
    dishes = []
    add_dish(dishes, "Салат Цезарь", 320.0)
    add_dish(dishes, "Пицца Маргарита", 590.0)
    cheap_dishes = filter_dishes_by_price(dishes, 400.0)
    assert len(cheap_dishes) == 1


def test_sort_dishes():
    dishes = []
    add_dish(dishes, "Пицца Маргарита", 590.0)
    add_dish(dishes, "Салат Цезарь", 320.0)
    sorted_dishes = sort_dishes(dishes)
    assert sorted_dishes[0].name == "Салат Цезарь"


def test_add_dish_rejects_non_positive_price():
    dishes = []
    with pytest.raises(ValueError):
        add_dish(dishes, "Бесплатное блюдо", 0)
